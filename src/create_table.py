import time
import boto3
from botocore.exceptions import ClientError
from config import REGION, TABLE_NAME, GSI_CUSTOMER, GSI_STATUS


def gsi(name, key_attr):
    return {
        'IndexName': name,
        'KeySchema': [
            {'AttributeName': key_attr, 'KeyType': 'HASH'},
            {'AttributeName': 'order_date', 'KeyType': 'RANGE'},
        ],
        'Projection': {'ProjectionType': 'ALL'},
        'ProvisionedThroughput': {'ReadCapacityUnits': 2, 'WriteCapacityUnits': 5},
    }


def wait_until_active(client, timeout=300):
    start = time.time()
    while time.time() - start < timeout:
        t = client.describe_table(TableName=TABLE_NAME)['Table']
        indexes = t.get('GlobalSecondaryIndexes', [])
        if t['TableStatus'] == 'ACTIVE' and all(i['IndexStatus'] == 'ACTIVE' for i in indexes):
            return
        time.sleep(3)
    raise TimeoutError('Table did not become ACTIVE in time')


def create_table():
    client = boto3.client('dynamodb', region_name=REGION)
    try:
        client.create_table(
            TableName=TABLE_NAME,
            AttributeDefinitions=[
                {'AttributeName': 'order_id', 'AttributeType': 'S'},
                {'AttributeName': 'customer_id', 'AttributeType': 'S'},
                {'AttributeName': 'delivery_status', 'AttributeType': 'S'},
                {'AttributeName': 'order_date', 'AttributeType': 'S'},
            ],
            KeySchema=[{'AttributeName': 'order_id', 'KeyType': 'HASH'}],
            ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 10},
            GlobalSecondaryIndexes=[
                gsi(GSI_CUSTOMER, 'customer_id'),
                gsi(GSI_STATUS, 'delivery_status'),
            ],
        )
        print(f'Creating table {TABLE_NAME}...')
    except ClientError as e:
        if e.response['Error']['Code'] != 'ResourceInUseException':
            raise
        print(f'Table {TABLE_NAME} already exists - nothing to create.')
    print('Waiting for table and indexes to become ACTIVE...')
    wait_until_active(client)
    print(f'Table {TABLE_NAME} is ACTIVE and ready.')


if __name__ == '__main__':
    create_table()
