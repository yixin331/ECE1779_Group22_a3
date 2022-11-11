from flask import Flask
from app import config
from app.config import aws_config
import requests
import boto3
import time
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()
scheduler.start()

global memcache_mode
global node_ip
global memcache_config

webapp = Flask(__name__)

memcache_mode = {'num_node': 1, 'mode': 'Manual'}
memcache_config = {'capacity': 128, 'policy': 'LRU'}
node_ip = {}

from app import main
from app import node_configure
from app import resize
from app import clear_memcache
from app import delete_all
from app import putImage
from app import getKey
from app import map
from app import remap
# from app import maptest


# TODO: need to call this when creating a new memcache instance
def schedule_cloud_watch(ip, id):
    try:
        node_address = 'http://' + str(ip) + ':5001/putStat'
        webapp.logger.warning(node_address)
        idToSend = {'InstanceId': id}
        response = requests.post(url=node_address, data=idToSend).json()
    except requests.exceptions.ConnectionError as err:
        webapp.logger.warning("Cache loses connection")


def initialize_instance():
    ec2_client = boto3.client(
        'ec2',
        region_name=aws_config['region'],
        aws_access_key_id=aws_config['access_key_id'],
        aws_secret_access_key=aws_config['secret_access_key']
    )
    USERDATA_SCRIPT = '''#!/bin/bash
    cd /home/ubuntu/ECE1779_Group22_a2/A_2/memcache
    pip install flask
    pip install apscheduler
    pip install boto3
    python3 run.py'''
    instances = ec2_client.run_instances(ImageId=config.ami_id, MinCount=1, MaxCount=1,
                                         InstanceType='t2.micro',
                                         UserData=USERDATA_SCRIPT)
    instance_id = instances['Instances'][0]['InstanceId']
    ec2 = boto3.resource('ec2')
    instance = ec2.Instance(instance_id)
    webapp.logger.warning('wait till instance is running')
    instance.wait_until_running()
    instance.reload()
    public_ip = instance.public_ip_address
    webapp.logger.warning(public_ip)
    node_ip[instance_id] = public_ip
    webapp.logger.warning('wait till instance is ready')
    # send node_ip dict to localhost/5003/changeIP
    nodeToSend = {"node": node_ip}
    try:
        response = requests.post(url='http://localhost:5003/changeIP', data=nodeToSend).json()
    except requests.exceptions.ConnectionError as err:
        webapp.logger.warning("Autoscaling loses connection")
    time.sleep(180)
    schedule_cloud_watch(public_ip, instance_id)
    scheduler.add_job(id='monitor_stats', func=monitor_stats, trigger='interval', seconds=60)

initialize_instance()
