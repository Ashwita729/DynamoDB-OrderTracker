import argparse
import uuid
from datetime import datetime, timezone
from config import get_table


def put_order(customer_id, restaurant='Test Kitchen', dish='Masala Dosa', total_amount=250):
    order = {
        'order_id': 'ORD-' + uuid.uuid4().hex[:10].upper(),
        'customer_id': customer_id,
        'customer_name': 'Customer ' + customer_id,
        'restaurant': restaurant,
        'dish': dish,
        'total_amount': total_amount,
        'delivery_status': 'PLACED',
        'order_date': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S'),
    }
    get_table().put_item(Item=order, ConditionExpression='attribute_not_exists(order_id)')
    return order


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--customer', default='CUST-001')
    args = parser.parse_args()
    print('New order saved:', put_order(args.customer))
