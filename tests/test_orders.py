import pytest
from moto import mock_aws


@pytest.fixture(autouse=True)
def fake_aws(monkeypatch):
    monkeypatch.setenv('AWS_ACCESS_KEY_ID', 'testing')
    monkeypatch.setenv('AWS_SECRET_ACCESS_KEY', 'testing')
    monkeypatch.setenv('AWS_DEFAULT_REGION', 'ap-south-1')
    with mock_aws():
        import create_table
        create_table.create_table()
        yield


def test_batch_write_and_scan():
    from generate_data import make_orders
    from batch_load import load_items
    from scan_orders import scan_all
    assert load_items(make_orders(60)) == 60
    assert len(scan_all()) == 60


def test_put_order_and_query_by_customer():
    from put_order import put_order
    from query_gsi import query_by_customer
    order = put_order('CUST-TEST')
    results = query_by_customer('CUST-TEST')
    assert [r['order_id'] for r in results] == [order['order_id']]


def test_query_by_status():
    from generate_data import make_orders
    from batch_load import load_items
    from query_gsi import query_by_status
    load_items(make_orders(100))
    results = query_by_status('DELIVERED')
    assert len(results) > 0
    assert all(r['delivery_status'] == 'DELIVERED' for r in results)
