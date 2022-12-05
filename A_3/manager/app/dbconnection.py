import boto3
from app.config import aws_config
from app import dbconnection
from boto3.dynamodb.conditions import Key
from datetime import datetime


def initializeDB():
    db = boto3.client(
        'dynamodb',
        aws_config['region'],
        aws_access_key_id=aws_config['access_key_id'],
        aws_secret_access_key=aws_config['secret_access_key']
    )

    try:
        db.delete_table(Table_name='image')
    except db.exceptions.ResourceNotFoundException as err:
        pass

    db.get_waiter('table_not_exists').wait(TableName='image')

    try:
        table = dynamodb.create_table(
            TableName='image',
            KeySchema=[
                {
                    'AttributeName': 'ID',
                    'KeyType': 'HASH'
                }
            ],
            GlobalSecondaryIndexes=[
                {
                    'IndexName': "GetImageIndex",
                    'KeySchema': [
                        {
                            'KeyType': 'HASH',
                            'AttributeName': 'ID'
                        },
                        {
                            'KeyType': 'RANGE',
                            'AttributeName': 'path'
                        }
                    ],
                    'Projection': {
                        'ProjectionType': 'KEYS_ONLY'
                    },
                    'ProvisionedThroughput': {
                        'ReadCapacityUnits': 2,
                        'WriteCapacityUnits': 2
                    }
                },
                {
                    'IndexName': "ListKeysIndex",
                    'KeySchema': [
                        {
                            'KeyType': 'HASH',
                            'AttributeName': 'ID'
                        }
                    ],
                    'Projection': {
                        'ProjectionType': 'KEYS_ONLY'
                    },
                    'ProvisionedThroughput': {
                        'ReadCapacityUnits': 2,
                        'WriteCapacityUnits': 2
                    }
                },
                {
                    'IndexName': "SortIDIndex",
                    'KeySchema': [
                        {
                            'KeyType': 'HASH',
                            'AttributeName': 'ID'
                        },
                        {
                            'KeyType': 'RANGE',
                            'AttributeName': 'last_edited_time'
                        }
                    ],
                    'Projection': {
                        'ProjectionType': 'KEYS_ONLY'
                    },
                    'ProvisionedThroughput': {
                        'ReadCapacityUnits': 2,
                        'WriteCapacityUnits': 2
                    }
                },
                {
                    'IndexName': "ListLocationsIndex",
                    'KeySchema': [
                        {
                            'KeyType': 'HASH',
                            'AttributeName': 'location'
                        }
                    ],
                    'Projection': {
                        'ProjectionType': 'KEYS_ONLY'
                    },
                    'ProvisionedThroughput': {
                        'ReadCapacityUnits': 2,
                        'WriteCapacityUnits': 2
                    }
                },
                {
                    'IndexName': "ListTagsIndex",
                    'KeySchema': [
                        {
                            'KeyType': 'HASH',
                            'AttributeName': 'tag'
                        }
                    ],
                    'Projection': {
                        'ProjectionType': 'KEYS_ONLY'
                    },
                    'ProvisionedThroughput': {
                        'ReadCapacityUnits': 2,
                        'WriteCapacityUnits': 2
                    }
                },
                {
                    'IndexName': "IDEXISTSIndex",
                    'KeySchema': [
                        {
                            'KeyType': 'HASH',
                            'AttributeName': 'ID'
                        }
                    ],
                    'Projection': {
                        'ProjectionType': 'ALL'
                    },
                    'ProvisionedThroughput': {
                        'ReadCapacityUnits': 2,
                        'WriteCapacityUnits': 2
                    }
                }
            ],

            AttributeDefinitions=[
                {
                    'AttributeName': 'ID',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'path',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'location',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'tag',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'last_edited_time',
                    'AttributeType': 'S'
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10
            }
        )
    except db.exceptions.ResourceInUseException as error:
        pass

    db.get_waiter('table_exists').wait(TableName='image')

    try:
        db.delete_table(Table_name='memcache_config')
    except db.exceptions.ResourceNotFoundException as err:
        pass

    db.get_waiter('table_not_exists').wait(TableName='memcache_config')

    try:
        table = dynamodb.create_table(
            TableName='memcache_config',
            KeySchema=[
                {
                    'AttributeName': 'updated_time',
                    'KeyType': 'RANGE'
                }
            ],
            GlobalSecondaryIndexes=[
                {
                    'IndexName': "GetConfigIndex",
                    'KeySchema': [
                        {
                            'KeyType': 'RANGE',
                            'AttributeName': 'updated_time'
                        }
                    ],
                    'Projection': {
                        'ProjectionType': 'ALL'
                    },
                    'ProvisionedThroughput': {
                        'ReadCapacityUnits': 2,
                        'WriteCapacityUnits': 2
                    }
                }
            ],

            AttributeDefinitions=[
                {
                    'AttributeName': 'updated_time',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'capacity',
                    'AttributeType': 'N'
                },
                {
                    'AttributeName': 'policy',
                    'AttributeType': 'S'
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10
            }
        )
    except db.exceptions.ResourceInUseException as error:
        pass

    db.get_waiter('table_exists').wait(TableName='memcache_config')

    put_config(128, 'LRU')

    try:
        db.delete_table(Table_name='memcache_mode')
    except db.exceptions.ResourceNotFoundException as err:
        pass

    db.get_waiter('table_not_exists').wait(TableName='memcache_mode')

    try:
        table = dynamodb.create_table(
            TableName='memcache_mode',
            KeySchema=[
                {
                    'AttributeName': 'updated_time',
                    'KeyType': 'RANGE'
                }
            ],
            GlobalSecondaryIndexes=[
                {
                    'IndexName': "GetModeIndex",
                    'KeySchema': [
                        {
                            'KeyType': 'RANGE',
                            'AttributeName': 'updated_time'
                        }
                    ],
                    'Projection': {
                        'ProjectionType': 'ALL'
                    },
                    'ProvisionedThroughput': {
                        'ReadCapacityUnits': 2,
                        'WriteCapacityUnits': 2
                    }
                }
            ],

            AttributeDefinitions=[
                {
                    'AttributeName': 'updated_time',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'num_node',
                    'AttributeType': 'N'
                },
                {
                    'AttributeName': 'mode',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'max_thr',
                    'AttributeType': 'N'
                },
                {
                    'AttributeName': 'min_thr',
                    'AttributeType': 'N'
                },
                {
                    'AttributeName': 'expand_ratio',
                    'AttributeType': 'N'
                },
                {
                    'AttributeName': 'shrink_ratio',
                    'AttributeType': 'N'
                },
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10
            }
        )
    except db.exceptions.ResourceInUseException as error:
        pass

    db.get_waiter('table_exists').wait(TableName='memcache_mode')

    put_mode(1, 'Manual', 1, 0, 1, 1)


def get_image(key):
    db = boto3.client(
        'dynamodb',
        aws_config['region'],
        aws_access_key_id=aws_config['access_key_id'],
        aws_secret_access_key=aws_config['secret_access_key']
    )

    table = db.Table(tableName='image')

    response = table.query(
        IndexName='GetImageIndex',
        KeyConditionExpression=Key('ID').eq(key),
        ProjectionExpression='path'
    )

    if len(response['Items']) == 0:
        return ""

    return response['Items'][0]['path']


def put_image(key, path, label, city):
    db = boto3.client(
        'dynamodb',
        aws_config['region'],
        aws_access_key_id=aws_config['access_key_id'],
        aws_secret_access_key=aws_config['secret_access_key']
    )

    table = db.Table(tableName='image')

    # invalidate key if key exists
    if key_exists(key) == {}:
        response = table.put_item(
            Item={
                'ID': key,
                'path': path,
                'location': city,
                'tag': label,
                'last_edited_time': datetime.now().isoformat()
            }
        )
    else:
        response = table.update_item(
            Key={
                'ID': key
            },
            UpdateExpression="set path=:p, location=:c, tag=:l, last_edited_time =:t",
            ExpressionAttributeValues={
                ':p': path,
                ':c': city,
                ':l': label,
                ':t': datetime.now().isoformat()
            }
        )


def list_keys():
    db = boto3.client(
        'dynamodb',
        aws_config['region'],
        aws_access_key_id=aws_config['access_key_id'],
        aws_secret_access_key=aws_config['secret_access_key']
    )

    table = db.Table(tableName='image')

    response = table.query(
        IndexName='ListKeysIndex'
    )

    records = []

    for i in response['Items']:
        if i['ID'] not in records:
            records.append(i['ID'])

    return records


def key_exists(key):
    db = boto3.client(
        'dynamodb',
        aws_config['region'],
        aws_access_key_id=aws_config['access_key_id'],
        aws_secret_access_key=aws_config['secret_access_key']
    )

    table = db.Table(tableName='image')

    response = table.query(
        IndexName='IDEXISTSIndex',
        KeyConditionExpression=Key('ID').eq(key)
    )

    if len(response['Items']) == 0:
        return {}

    return response['Items'][0]


def put_config(capacity, policy):
    db = boto3.client(
        'dynamodb',
        aws_config['region'],
        aws_access_key_id=aws_config['access_key_id'],
        aws_secret_access_key=aws_config['secret_access_key']
    )

    table = db.Table(tableName='memcache_config')

    response = table.put_item(
        Item={
            'updated_time': datetime.now().isoformat(),
            'capacity': capacity,
            'policy': policy
        }
    )


def put_mode(num_node, mode, max_thr, min_thr, expand_ratio, shrink_ratio):
    db = boto3.client(
        'dynamodb',
        aws_config['region'],
        aws_access_key_id=aws_config['access_key_id'],
        aws_secret_access_key=aws_config['secret_access_key']
    )

    table = db.Table(tableName='memcache_mode')

    response = table.put_item(
        Item={
            'updated_time': datetime.now().isoformat(),
            'num_node': num_node,
            'mode': mode,
            'max_thr': max_thr,
            'min_thr': min_thr,
            'expand_ratio': expand_ratio,
            'shrink_ratio': shrink_ratio
        }
    )


def clear():
    db = boto3.client(
        'dynamodb',
        aws_config['region'],
        aws_access_key_id=aws_config['access_key_id'],
        aws_secret_access_key=aws_config['secret_access_key']
    )

    table = db.Table(tableName='image')

    scan = table.scan()
    with table.batch_writer() as batch:
        for each in scan['Items']:
            batch.delete_item(
                Key={
                    'ID': each['ID']
                }
            )


def update_image(key):
    db = boto3.client(
        'dynamodb',
        aws_config['region'],
        aws_access_key_id=aws_config['access_key_id'],
        aws_secret_access_key=aws_config['secret_access_key']
    )

    table = db.Table(tableName='image')
    response = table.update_item(
        Key={
            'ID': key
        },
        UpdateExpression="set last_edited_time =:t",
        ExpressionAttributeValues={
            ':t': datetime.now().isoformat()
        }
    )


def sort_by_time(key_list):
    db = boto3.client(
        'dynamodb',
        aws_config['region'],
        aws_access_key_id=aws_config['access_key_id'],
        aws_secret_access_key=aws_config['secret_access_key']
    )

    table = db.Table(tableName='image')

    # ids_to_sort = ', '.join(str(id) for id in key_list)

    response = table.query(
        IndexName='SortIDIndex',
        FilterExpression=Attr('ID').is_in(key_list),
        ScanIndexForward=true
    )
    records = []

    for i in response['Items']:
        if i['ID'] not in records:
            records.append(i['ID'])

    return records


def list_locations():
    db = boto3.client(
        'dynamodb',
        aws_config['region'],
        aws_access_key_id=aws_config['access_key_id'],
        aws_secret_access_key=aws_config['secret_access_key']
    )

    table = db.Table(tableName='image')

    response = table.query(
        IndexName='ListLocationsIndex'
    )

    records = []

    for i in response['Items']:
        if i['location'] != '' and i['location'] not in records:
            records.append(i['location'])

    return records


def list_tags():
    db = boto3.client(
        'dynamodb',
        aws_config['region'],
        aws_access_key_id=aws_config['access_key_id'],
        aws_secret_access_key=aws_config['secret_access_key']
    )

    table = db.Table(tableName='image')

    response = table.query(
        IndexName='ListTagsIndex'
    )

    records = []

    for i in response['Items']:
        if i['tag'] != '' and i['tag'] not in records:
            records.append(i['tag'])

    return records