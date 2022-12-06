from flask import render_template, url_for, request, g
from app import webapp
import requests
import boto3
from app.config import aws_config, email_config
import zipfile
from datetime import datetime
import io
from email import encoders
from email.mime.base import MIMEBase
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


@webapp.route('/shareTags/<tag>', methods=['GET', 'POST'])
def share(tag):
    ses_client = boto3.client("ses", region_name=aws_config['region'])
    # TODO: add check whether email is ""
    email = request.form.get('email')
    webapp.logger.warning(email)
    # TODO: send verification email, need UI?
    response = ses_client.verify_email_identity(
        EmailAddress=email
    )

    bucket_name = '1779' + tag.lower()
    webapp.logger.warning(bucket_name)
    s3 = boto3.client(
        's3',
        aws_config['region'],
        aws_access_key_id=aws_config['access_key_id'],
        aws_secret_access_key=aws_config['secret_access_key']
    )

    # create zip file
    file_name = '%s-%s.zip' % (tag.lower(), datetime.now())
    webapp.logger.warning(f"Saving into zip {file_name}")
    s = io.BytesIO()
    zf = zipfile.ZipFile(s, 'w')

    for key in s3.list_objects(Bucket=bucket_name)['Contents']:
        data = s3.get_object(Bucket=bucket_name, Key=key['Key'])
        zf.writestr(key['Key'], data.get('Body').read())
    zf.close()

    # create email
    msg = MIMEMultipart()
    msg["Subject"] = "Pictures of " + tag.lower()
    msg["From"] = email_config
    msg["To"] = email
    dest = []
    dest.append(email)
    # Set message body
    body = MIMEText("Here is the pictures of " + tag.lower() + "!", "plain")
    msg.attach(body)

    attachment = MIMEApplication(s.getvalue())
    attachment.add_header("Content-Disposition",
                    "attachment",
                    filename=file_name)
    msg.attach(attachment)

    response = ses_client.send_raw_email(
        Source=msg["From"],
        Destinations=dest,
        RawMessage={"Data": msg.as_string()}
    )

    webapp.logger.warning(response)
    return response
    #
    # if len(urls) > 0:
    #     return render_template("location.html", user_image=urls, place=place)
    # else:
    #     return render_template("location.html", result="There's no photo for " + place, place=place)


@webapp.route('/shareLocations/<location>', methods=['GET', 'POST'])
def share(location):
    ses_client = boto3.client("ses", region_name=aws_config['region'])
    # TODO: add check whether email is ""
    email = request.form.get('email')
    webapp.logger.warning(email)

    bucket_name = '1779' + location.lower()
    webapp.logger.warning(bucket_name)
    s3 = boto3.client(
        's3',
        aws_config['region'],
        aws_access_key_id=aws_config['access_key_id'],
        aws_secret_access_key=aws_config['secret_access_key']
    )

    # create zip file
    file_name = '%s-%s.zip' % (location.lower(), datetime.now())
    webapp.logger.warning(f"Saving into zip {file_name}")
    s = io.BytesIO()
    zf = zipfile.ZipFile(s, 'w')

    for key in s3.list_objects(Bucket=bucket_name)['Contents']:
        data = s3.get_object(Bucket=bucket_name, Key=key['Key'])
        zf.writestr(key['Key'], data.get('Body').read())
    zf.close()

    # create email
    msg = MIMEMultipart()
    msg["Subject"] = "Pictures of " + location.lower()
    msg["From"] = email_config
    msg["To"] = email
    dest = []
    dest.append(email)
    # Set message body
    body = MIMEText("Here is the pictures of " + location.lower() + "!", "plain")
    msg.attach(body)

    attachment = MIMEApplication(s.getvalue())
    attachment.add_header("Content-Disposition",
                    "attachment",
                    filename=file_name)
    msg.attach(attachment)

    response = ses_client.send_raw_email(
        Source=msg["From"],
        Destinations=dest,
        RawMessage={"Data": msg.as_string()}
    )

    webapp.logger.warning(response)
    return response
    #
    # if len(urls) > 0:
    #     return render_template("location.html", user_image=urls, place=place)
    # else:
    #     return render_template("location.html", result="There's no photo for " + place, place=place)


@webapp.route('/verifyEmail', methods=['GET', 'POST'])
def verifyEmail():
    ses_client = boto3.client("ses", region_name=aws_config['region'])
    # TODO: add check whether email is ""
    email = request.form.get('email')
    webapp.logger.warning(email)
    # TODO: send verification email, need UI?
    response = ses_client.verify_email_identity(
        EmailAddress=email
    )

    return response
