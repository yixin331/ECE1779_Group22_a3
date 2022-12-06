import boto3
from app.config import aws_config
from app import webapp
from boto3.dynamodb.conditions import Key, Attr
from datetime import datetime


def initializeDB():
    db = boto3.client(
        'dynamodb',
        region_name=aws_config['region'],
        aws_access_key_id=aws_config['access_key_id'],
        aws_secret_access_key=aws_config['secret_access_key']
    )

    try:
        db.delete_table(TableName='image')
    except db.exceptions.ResourceNotFoundException as err:
        webapp.logger.warning("Table image does not exist")

    db.get_waiter('table_not_exists').wait(TableName='image')

    try:
        table = db.create_table(
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
                            'AttributeName': 'image_path'
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
                    'IndexName': "ListCitiesIndex",
                    'KeySchema': [
                        {
                            'KeyType': 'HASH',
                            'AttributeName': 'city'
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
                    'AttributeName': 'image_path',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'city',
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
        webapp.logger.warning("Table image exists")

    db.get_waiter('table_exists').wait(TableName='image')

    try:
        db.delete_table(TableName='memcache_config')
    except db.exceptions.ResourceNotFoundException as err:
        webapp.logger.warning("Table memcache_config does not exist")

    db.get_waiter('table_not_exists').wait(TableName='memcache_config')

    try:
        table = db.create_table(
            TableName='memcache_config',
            KeySchema=[
                {
                    'AttributeName': 'updated_time',
                    'KeyType': 'HASH'
                }
            ],
            GlobalSecondaryIndexes=[
                {
                    'IndexName': "GetConfigIndex",
                    'KeySchema': [
                        {
                            'KeyType': 'HASH',
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
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10
            }
        )
    except db.exceptions.ResourceInUseException as error:
        webapp.logger.warning("Table memcache_config exists")

    db.get_waiter('table_exists').wait(TableName='memcache_config')

    put_config(128, 'LRU')

    try:
        db.delete_table(TableName='memcache_mode')
    except db.exceptions.ResourceNotFoundException as err:
        webapp.logger.warning("Table memcache_mode does not exist")

    db.get_waiter('table_not_exists').wait(TableName='memcache_mode')

    try:
        table = db.create_table(
            TableName='memcache_mode',
            KeySchema=[
                {
                    'AttributeName': 'updated_time',
                    'KeyType': 'HASH'
                }
            ],
            GlobalSecondaryIndexes=[
                {
                    'IndexName': "GetModeIndex",
                    'KeySchema': [
                        {
                            'KeyType': 'HASH',
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
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10
            }
        )
    except db.exceptions.ResourceInUseException as error:
        webapp.logger.warning("Table memcache_mode exists")

    db.get_waiter('table_exists').wait(TableName='memcache_mode')

    put_mode(1, 'Manual', 1, 0, 1, 1)


def get_image(key):
    session = boto3.Session(
        region_name=aws_config['region'],
        aws_access_key_id=aws_config['access_key_id'],
        aws_secret_access_key=aws_config['secret_access_key']
    )

    db = session.resource('dynamodb')

    table = db.Table('image')

    response = table.query(
        IndexName='GetImageIndex',
        KeyConditionExpression=Key('ID').eq(key)
    )

    if len(response['Items']) == 0:
        return ""

    return response['Items'][0]['image_path']


def put_image(key, path, label, city):
    session = boto3.Session(
        region_name=aws_config['region'],
        aws_access_key_id=aws_config['access_key_id'],
        aws_secret_access_key=aws_config['secret_access_key']
    )

    db = session.resource('dynamodb')

    table = db.Table('image')

    # invalidate key if key exists
    if key_exists(key) == {}:
        response = table.put_item(
            Item={
                'ID': key,
                'image_path': path,
                'city': city,
                'tag': label,
                'last_edited_time': datetime.now().isoformat()
            }
        )
    else:
        response = table.update_item(
            Key={
                'ID': key
            },
            UpdateExpression="set image_path=:p, city=:c, tag=:l, last_edited_time =:t",
            ExpressionAttributeValues={
                ':p': path,
                ':c': city,
                ':l': label,
                ':t': datetime.now().isoformat()
            }
        )


def list_keys():
    session = boto3.Session(
        region_name=aws_config['region'],
        aws_access_key_id=aws_config['access_key_id'],
        aws_secret_access_key=aws_config['secret_access_key']
    )

    db = session.resource('dynamodb')

    table = db.Table('image')
    records = []
    scan = table.scan(IndexName='ListKeysIndex')
    with table.batch_writer() as batch:
        for each in scan['Items']:
            if each['ID'] not in records:
                records.append(each['ID'])

    while 'LastEvaluatedKey' in scan:
        scan = table.scan(
            IndexName='ListKeysIndex',
            ExclusiveStartKey=scan['LastEvaluatedKey']
        )

        with table.batch_writer() as batch:
            for each in scan['Items']:
                if each['ID'] not in records:
                    records.append(each['ID'])
    records.sort()
    return records


def key_exists(key):
    session = boto3.Session(
        region_name=aws_config['region'],
        aws_access_key_id=aws_config['access_key_id'],
        aws_secret_access_key=aws_config['secret_access_key']
    )

    db = session.resource('dynamodb')

    table = db.Table('image')

    response = table.query(
        IndexName='IDEXISTSIndex',
        KeyConditionExpression=Key('ID').eq(key)
    )

    if len(response['Items']) == 0:
        return {}

    return response['Items'][0]


def put_config(capacity, policy):
    session = boto3.Session(
        region_name=aws_config['region'],
        aws_access_key_id=aws_config['access_key_id'],
        aws_secret_access_key=aws_config['secret_access_key']
    )

    db = session.resource('dynamodb')

    table = db.Table('memcache_config')

    response = table.put_item(
        Item={
            'updated_time': datetime.now().isoformat(),
            'capacity': capacity,
            'policy': policy
        }
    )


def put_mode(num_node, mode, max_thr, min_thr, expand_ratio, shrink_ratio):
    session = boto3.Session(
        region_name=aws_config['region'],
        aws_access_key_id=aws_config['access_key_id'],
        aws_secret_access_key=aws_config['secret_access_key']
    )

    db = session.resource('dynamodb')

    table = db.Table('memcache_mode')

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
    session = boto3.Session(
        region_name=aws_config['region'],
        aws_access_key_id=aws_config['access_key_id'],
        aws_secret_access_key=aws_config['secret_access_key']
    )

    db = session.resource('dynamodb')

    table = db.Table('image')

    scan = table.scan(IndexName='ListKeysIndex')
    with table.batch_writer() as batch:
        for each in scan['Items']:
            batch.delete_item(
                Key={
                    'ID': each['ID']
                }
            )

    while 'LastEvaluatedKey' in scan:
        scan = table.scan(
            IndexName='ListKeysIndex',
            ExclusiveStartKey=scan['LastEvaluatedKey']
        )

        with table.batch_writer() as batch:
            for each in scan['Items']:
                batch.delete_item(
                    Key={
                        'ID': each['ID']
                    }
                )


def update_image(key):
    session = boto3.Session(
        region_name=aws_config['region'],
        aws_access_key_id=aws_config['access_key_id'],
        aws_secret_access_key=aws_config['secret_access_key']
    )

    db = session.resource('dynamodb')

    table = db.Table('image')
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
    session = boto3.Session(
        region_name=aws_config['region'],
        aws_access_key_id=aws_config['access_key_id'],
        aws_secret_access_key=aws_config['secret_access_key']
    )

    db = session.resource('dynamodb')

    table = db.Table('image')

    # ids_to_sort = ', '.join(str(id) for id in key_list)
    records = []
    scan = table.scan(
        IndexName='SortIDIndex',
        FilterExpression=Attr('ID').is_in(key_list)
    )
    with table.batch_writer() as batch:
        for each in scan['Items']:
            if each['ID'] not in records:
                records.append(each['ID'])

    while 'LastEvaluatedKey' in scan:
        scan = table.scan(
            IndexName='SortIDIndex',
            FilterExpression=Attr('ID').is_in(key_list),
            ExclusiveStartKey=scan['LastEvaluatedKey']
        )

        with table.batch_writer() as batch:
            for each in scan['Items']:
                if each['ID'] not in records:
                    records.append(each['ID'])
    records.reverse()
    webapp.logger.warning(records)
    return records


def list_cities():
    session = boto3.Session(
        region_name=aws_config['region'],
        aws_access_key_id=aws_config['access_key_id'],
        aws_secret_access_key=aws_config['secret_access_key']
    )

    db = session.resource('dynamodb')

    table = db.Table('image')

    records = []
    scan = table.scan(IndexName='ListCitiesIndex')
    with table.batch_writer() as batch:
        for each in scan['Items']:
            if each['city'] != 'default' and each['city'] not in records:
                records.append(each['city'])

    while 'LastEvaluatedKey' in scan:
        scan = table.scan(
            IndexName='ListCitiesIndex',
            ExclusiveStartKey=scan['LastEvaluatedKey']
        )

        with table.batch_writer() as batch:
            for each in scan['Items']:
                if each['city'] != 'default' and each['city'] not in records:
                    records.append(each['city'])
    records.sort()
    webapp.logger.warning(records)
    return records


def list_tags():
    session = boto3.Session(
        region_name=aws_config['region'],
        aws_access_key_id=aws_config['access_key_id'],
        aws_secret_access_key=aws_config['secret_access_key']
    )

    db = session.resource('dynamodb')

    table = db.Table('image')

    records = {}
    scan = table.scan(IndexName='ListTagsIndex')
    with table.batch_writer() as batch:
        for each in scan['Items']:
            if each['tag'] != 'default':
                if each['tag'] not in records:
                    records[each['tag']] = 1
                else:
                    records[each['tag']] += 1

    while 'LastEvaluatedKey' in scan:
        scan = table.scan(
            IndexName='ListTagsIndex',
            ExclusiveStartKey=scan['LastEvaluatedKey']
        )

        with table.batch_writer() as batch:
            for each in scan['Items']:
                if each['tag'] != 'default':
                    if each['tag'] not in records:
                        records[each['tag']] = 1
                    else:
                        records[each['tag']] += 1

    webapp.logger.warning(records)
    return records