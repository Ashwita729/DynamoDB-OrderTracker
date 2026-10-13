import argparse
from config import get_table


def scan_all():
    table = get_table()
    items = []
    kwargs = {}
    while True:
        response = table.scan(**kwargs)
        items.extend(response['Items'])
        if 'LastEvaluatedKey' not in response:
            return items
        kwargs['ExclusiveStartKey'] = response['LastEvaluatedKey']


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--show', type=int, default=10, help='how many orders to print')
    args = parser.parse_args()
    orders = scan_all()
    print(f'Total orders found by Scan: {len(orders)}')
    for o in orders[:args.show]:
        print(o['order_id'], o['customer_id'], o['delivery_status'], o['total_amount'])
