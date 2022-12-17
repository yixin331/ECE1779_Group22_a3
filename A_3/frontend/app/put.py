import json
from flask import render_template, url_for, request, g
from app import webapp, dbconnection, num_n
import requests
from werkzeug.utils import secure_filename
from os.path import join, dirname, realpath
from pathlib import Path
import os
import base64
import boto3
from botocore.exceptions import ClientError
from app.config import aws_config


@webapp.teardown_appcontext
def teardown_db(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def create_bucket(bucket_name):
    s3 = boto3.client(
        's3',
        aws_config['region'],
        aws_access_key_id=aws_config['access_key_id'],
        aws_secret_access_key=aws_config['secret_access_key']
    )
    response = s3.list_buckets()
    created = False
    for bucket in response['Buckets']:
        if bucket["Name"] == bucket_name:
            created = True
    if not created:
        try:
            response = s3.create_bucket(Bucket=bucket_name)
            bucket_policy = {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Sid": "PublicRead",
                        "Effect": "Allow",
                        "Principal": "*",
                        "Action": [
                            "s3:GetObject",
                            "s3:GetObjectVersion"
                        ],
                        "Resource": [
                            "arn:aws:s3:::" + bucket_name + "/*"
                        ]
                    }
                ]
            }
            bucket_policy = json.dumps(bucket_policy)
            s3.put_bucket_policy(Bucket=bucket_name, Policy=bucket_policy)
        except ClientError as e:
            webapp.logger.warning("Fail to create a bucket")


@webapp.route('/put', methods=['GET', 'POST'])
def put():
    result = ""
    if request.method == 'POST':
        if 'key' not in request.form:
            return render_template("put.html", result="Please input a valid key")
        key = request.form.get('key')
        # key invalid
        if not (key is not None and len(key) > 0):
            return render_template("put.html", result="Please input a valid key")
        # check file
        if 'file' not in request.files:
            return render_template("put.html", result="Please select a file")
        file = request.files['file']
        filename = secure_filename(file.filename)
        # check extension to be jpeg or png to use image recognition
        ALLOWED_EXTENSIONS = {'png', 'jpeg', 'jpg'}
        # s3 create bucket
        s3 = boto3.client(
            's3',
            aws_config['region'],
            aws_access_key_id=aws_config['access_key_id'],
            aws_secret_access_key=aws_config['secret_access_key']
        )
        bucket_name = '1779a3files'
        create_bucket(bucket_name)
        if file and '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS:
            # For invalidate key, need to delete images in bucket if exists
            image_dict = dbconnection.key_exists(key)
            if image_dict != {}:
                tag = '1779' + image_dict['tag']
                s3.delete_object(Bucket=tag, Key=image_dict['image_path'])
                if image_dict['city'] != 'default':
                    location = 'location' + image_dict['city']
                    s3.delete_object(Bucket=location, Key=image_dict['image_path'])

            extension = filename.rsplit('.', 1)[1].lower()
            s3.put_object(Bucket=bucket_name, Key=key, Body=file)
            file.seek(0, 0)
            # detect label
            client = boto3.client('rekognition')
            response = client.detect_labels(Image={'S3Object': {'Bucket': bucket_name, 'Name': key}})
            label = None
            category_list = ['Buildings and Architecture', 'Popular Landmarks', 'Nature and Outdoors',
                             'Travel and Adventure']
            location_needed = False
            for label_detail in response['Labels']:
                if int(label_detail['Confidence']) > 95:
                    label = str(label_detail['Name'])
                    # run pip install boto3 --upgrade if category can't be retrieved
                    category = label_detail['Categories'][0]['Name']
                    if category in category_list:
                        location_needed = True
                    break
            webapp.logger.warning("Label identified " + label)
            # create corresponding bucket & store
            # make sure the bucket_name is valid
            bucket_name = '1779' + label.lower()
            s3 = boto3.client(
                's3',
                aws_config['region'],
                aws_access_key_id=aws_config['access_key_id'],
                aws_secret_access_key=aws_config['secret_access_key']
            )
            create_bucket(bucket_name)
            s3.put_object(Bucket=bucket_name, Key=key+'.'+extension, Body=file)
            file.seek(0, 0)

            city = request.form.get('city')
            # TODO: if city is empty, get current city using coordinates
            # Store it into location bucket if needed
            if location_needed and len(city) > 0:
                s3 = boto3.client(
                    's3',
                    aws_config['region'],
                    aws_access_key_id=aws_config['access_key_id'],
                    aws_secret_access_key=aws_config['secret_access_key']
                )
                bucket_name = 'location' + city.lower()
                create_bucket(bucket_name)
                s3.put_object(Bucket=bucket_name, Key=key+'.'+extension, Body=file)
            else:
                city = 'default'
            webapp.logger.warning(city)
            dbconnection.put_image(key, key + "." + extension, label.lower(), city.lower())
            file.seek(0, 0)
            # put in cache
            keyToSend = {'key': key}
            fileToSend = {'file': file}
            response = None
            try:
                response = requests.post(url='https://adpqg6brrc.execute-api.us-east-1.amazonaws.com/dev/putImage', data=keyToSend, files=fileToSend).json()
            except requests.exceptions.ConnectionError as err:
                webapp.logger.warning("Manager app loses connection")
            if response is None or response["success"] == "false":
                # file is too large to put into cache -> but it's already in database
                result = "File is uploaded in the database but not in cache"
                return render_template("put.html", result=result)
            result = "Uploaded into cache and database"
            return render_template("put.html", result=result)
        else:
            return render_template("put.html", result="Please select a valid image file")
    else:
        return render_template("put.html")
