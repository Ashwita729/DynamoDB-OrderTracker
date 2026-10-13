import boto3
from config import REGION, TABLE_NAME

if __name__ == '__main__':
    answer = input(f'Type YES to permanently delete table {TABLE_NAME}: ')
    if answer == 'YES':
        boto3.client('dynamodb', region_name=REGION).delete_table(TableName=TABLE_NAME)
        print('Delete started. The table disappears in about a minute.')
    else:
        print('Cancelled.')
