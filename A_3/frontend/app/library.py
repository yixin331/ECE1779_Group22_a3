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

@webapp.route('/library', methods=['GET', 'POST'])
def library():
    return render_template("library.html")