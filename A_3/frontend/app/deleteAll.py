from flask import request, g, json
from app import webapp,dbconnection
import requests
import boto3
from app.config import aws_config



@webapp.route('/deleteAll', methods=['POST'])
def deleteAll():
    if request.method == 'POST':
        response = None
        s3 = boto3.resource('s3')
        bucket = s3.Bucket('1779a3files')
        bucket.objects.all().delete()
        tags = dbconnection.list_tags()
        for tag in tags:
            bucket_name = '1779' + tag.lower()
            bucket = s3.Bucket(bucket_name)
            bucket.objects.all().delete()
            bucket.delete()
        cities = dbconnection.list_cities()
        for city in cities:
            bucket_name = 'location' + city.lower()
            bucket = s3.Bucket(bucket_name)
            bucket.objects.all().delete()
            bucket.delete()
        value = {"success": "true"}
        response = webapp.response_class(
            response=json.dumps(value),
            status=200,
            mimetype='application/json'
        )
        return response
