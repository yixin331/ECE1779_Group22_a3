from flask import render_template, url_for, request, g
from app import webapp, dbconnection,num_n
import requests
from werkzeug.utils import secure_filename
from os.path import join, dirname, realpath
from pathlib import Path
import os
import base64
import boto3
from botocore.exceptions import ClientError
from app.config import aws_config

@webapp.route('/place', methods=['GET', 'POST'])
def place():
    return render_template("place.html")