from flask import render_template, url_for, request, g
from app import webapp, dbconnection
import requests
from os.path import join, dirname, realpath
from pathlib import Path
import os
import io
import boto3
import base64
from app.config import aws_config


@webapp.teardown_appcontext
def teardown_db(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@webapp.route('/library', methods=['GET', 'POST'])
def library():
    if request.method == 'POST':
        label = request.form.get('key')
        bucket_name = '1779' + label.lower()
        s3 = boto3.client(
            's3',
            aws_config['region'],
            aws_access_key_id=aws_config['access_key_id'],
            aws_secret_access_key=aws_config['secret_access_key']
        )
        # check if bucket exists
        response = s3.list_buckets()
        created = False
        for bucket in response['Buckets']:
            if bucket["Name"] == bucket_name:
                created = True
        if not created:
            return render_template("library.html", result="Please input a valid tag")
        else:
            prefix = 'https://' + bucket_name + '.s3.amazonaws.com/'
            urls = {}
            for key in s3.list_objects(Bucket=bucket_name)['Contents']:
                url = prefix + key['Key']
                urls[url] = key['Key']
            print(urls)
            if len(url) > 0:
                return render_template("library.html", user_image=urls)
            else:
                return render_template("library.html", result="Please input a valid tag", user_image=None)
    else:
        return render_template("library.html", user_image=None)
