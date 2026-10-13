import json
import os
import random
from datetime import datetime, timedelta
from config import VALID_STATUSES

RESTAURANTS = ['Spice Hub', 'Dosa Corner', 'Biryani House', 'Pizza Point', 'Green Bowl']
DISHES = ['Masala Dosa', 'Chicken Biryani', 'Paneer Pizza', 'Veg Thali', 'Idli Combo']


def make_orders(n=2000):
    random.seed(42)
    start = datetime(2026, 9, 1)
    orders = []
    for i in range(1, n + 1):
        cust = random.randint(1, 100)
        orders.append({
            'order_id': f'ORD-{i:05d}',
            'customer_id': f'CUST-{cust:03d}',
            'customer_name': f'Customer {cust}',
            'restaurant': random.choice(RESTAURANTS),
            'dish': random.choice(DISHES),
            'total_amount': random.randint(150, 1200),
            'delivery_status': random.choice(VALID_STATUSES),
            'order_date': (start + timedelta(minutes=i * 20)).strftime('%Y-%m-%dT%H:%M:%S'),
        })
    return orders


if __name__ == '__main__':
    folder = os.path.join(os.path.dirname(__file__), '..', 'data')
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, 'orders.json')
    with open(path, 'w') as f:
        json.dump(make_orders(), f)
    print('Created 2000 orders in data/orders.json')
