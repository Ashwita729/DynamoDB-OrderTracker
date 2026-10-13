import json
import os
import time
from config import get_resource, TABLE_NAME


def load_items(items):
    ddb = get_resource()
    written = 0
    for start in range(0, len(items), 25):
        batch = items[start:start + 25]
        request = {TABLE_NAME: [{'PutRequest': {'Item': item}} for item in batch]}
        delay = 0.2
        while request:
            response = ddb.batch_write_item(RequestItems=request)
            leftover = response.get('UnprocessedItems', {})
            written += len(request[TABLE_NAME]) - len(leftover.get(TABLE_NAME, []))
            request = leftover
            if request:
                print(f'  throttled, retrying {len(request[TABLE_NAME])} items in {delay:.1f}s')
                time.sleep(delay)
                delay = min(delay * 2, 5)
        if (start // 25) % 10 == 0:
            print(f'  progress: {written} items written')
    return written


if __name__ == '__main__':
    path = os.path.join(os.path.dirname(__file__), '..', 'data', 'orders.json')
    with open(path) as f:
        data = json.load(f)
    print(f'Loading {len(data)} orders (this can take a few minutes on the free tier)...')
    print(f'Done. Total written: {load_items(data)}')
