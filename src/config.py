import os
import boto3

REGION = os.getenv('AWS_REGION', 'ap-south-1')
TABLE_NAME = os.getenv('TABLE_NAME', 'Orders')
GSI_CUSTOMER = 'customer_id-index'
GSI_STATUS = 'delivery_status-index'
VALID_STATUSES = ['PLACED', 'PREPARING', 'OUT_FOR_DELIVERY', 'DELIVERED', 'CANCELLED']


def get_resource():
    return boto3.resource('dynamodb', region_name=REGION)


def get_table():
    return get_resource().Table(TABLE_NAME)
