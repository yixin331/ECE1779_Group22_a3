from app import webapp
from flask import request, json
import requests


@webapp.route('/getKey', methods=['POST'])
def getKey():
    response = None
    key = request.form.get('key')
    keyToSend = {'key': key}
    try:
        response = requests.post(url='https://adpqg6brrc.execute-api.us-east-1.amazonaws.com/dev/map', data=keyToSend).json()
    except requests.exceptions.ConnectionError as err:
        webapp.logger.warning("Manager app loses connection")

    node_address = 'http://' + response["content"] + ':5001/getKey'
    try:
        response = requests.post(url=node_address, data=request.form).json()
    except requests.exceptions.ConnectionError as err:
        webapp.logger.warning("Cache loses connection")

    return response