from flask import render_template, url_for, request, g
from app import webapp, dbconnection, num_n
import requests
from werkzeug.utils import secure_filename
from os.path import join, dirname, realpath
from pathlib import Path
import os
import base64
import boto3
import json
import urllib.parse
from botocore.exceptions import ClientError
from app.config import aws_config


@webapp.route('/place', methods=['GET', 'POST'])
def place():
    cities = ['Toronto', "Collingwood", "Beijing", "Shanghai", "Vancouver", "Ottawa", "Chihuahua", "Denver"]
    client = boto3.client('lambda',
                          region_name='us-east-1',
                          aws_access_key_id='AKIAR23VGBXQKQ2JU4ZI',
                          aws_secret_access_key='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')
    city_dict = {}
    for city in cities:
        payload = {
            "address": city
        }
        result = client.invoke(FunctionName="location-geocode",
                               InvocationType='RequestResponse',
                               Payload=json.dumps(payload))
        ranges = result['Payload'].read()
        api_response = json.loads(ranges)
        response_body = api_response['body']
        response = json.loads(response_body)
        city_dict[city] = response["Results"][0]["Place"]["Geometry"]["Point"]

    return render_template("place.html", dict=city_dict)


@webapp.route('/getplace/<place>', methods=['GET', 'POST'])
def getplace(place):
    bucket_name = 'location' + place.lower()
    webapp.logger.warning(bucket_name)
    s3 = boto3.client(
        's3',
        aws_config['region'],
        aws_access_key_id=aws_config['access_key_id'],
        aws_secret_access_key=aws_config['secret_access_key']
    )
    prefix = 'https://' + bucket_name + '.s3.amazonaws.com/'
    urls = {}
    for key in s3.list_objects(Bucket=bucket_name)['Contents']:
        url = prefix + key['Key']
        urls[url] = key['Key']
        webapp.logger.warning(len(urls))
    if len(url) > 0:
        return render_template("location.html", user_image=urls, place=place)
    else:
        return render_template("location.html", result="There's no photo for " + place, place=place)
