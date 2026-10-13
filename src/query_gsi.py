import argparse
from boto3.dynamodb.conditions import Key
from config import get_table, GSI_CUSTOMER, GSI_STATUS


def query_by_customer(customer_id, limit=10):
    return get_table().query(
        IndexName=GSI_CUSTOMER,
        KeyConditionExpression=Key('customer_id').eq(customer_id),
        ScanIndexForward=False,
        Limit=limit,
    )['Items']


def query_by_status(status, limit=10):
    return get_table().query(
        IndexName=GSI_STATUS,
        KeyConditionExpression=Key('delivery_status').eq(status),
        ScanIndexForward=False,
        Limit=limit,
    )['Items']


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--customer')
    group.add_argument('--status')
    args = parser.parse_args()
    if args.customer:
        results = query_by_customer(args.customer)
    else:
        results = query_by_status(args.status)
    print(f'Query returned {len(results)} orders (newest first, max 10):')
    for o in results:
        print(o['order_id'], o['customer_id'], o['delivery_status'], o['order_date'])
