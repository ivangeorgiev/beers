import json


def check_order(order, is_open, beers=None):
    assert isinstance(order, dict)
    assert 'is_open' in order
    assert order['is_open'] == is_open

    if beers is not None:
        assert 'beers' in order
        assert isinstance(order['beers'], list)
        assert len(order['beers']) == len(beers)
        for k, beer in enumerate(beers):
            assert order['beers'][k]['sku'] == beer['sku']
            assert order['beers'][k]['quantity'] == beer['quantity']


def test_orders(users, beers, orders):
    # 1. Get orders without token
    resp = orders.get('/api/orders/')
    assert resp.status_code == 400

    # 2. Get orders with wrong token
    resp = orders.get('/api/orders/', headers={'Authorization': 'AAA'})
    assert resp.status_code == 401

    # 3. Get orders
    resp = orders.get('/api/orders/', headers={'Authorization': 'TESTING_TOKEN'})
    assert resp.status_code == 200
    data = json.loads(resp.data)
    assert isinstance(data, list)
    assert len(data) == 0

    # 4. Open an order without token
    resp = orders.get('/api/orders/current')
    assert resp.status_code == 400

    # 5. Open an order with wrong token
    resp = orders.get('/api/orders/current', headers={'Authorization': 'AAA'})
    assert resp.status_code == 401

    # 6. Open an order
    resp = orders.get('/api/orders/current', headers={'Authorization': 'TESTING_TOKEN'})
    assert resp.status_code == 200
    data = json.loads(resp.data)
    check_order(data, 'True', [])

    resp = orders.get('/api/orders/', headers={'Authorization': 'TESTING_TOKEN'})
    assert resp.status_code == 200
    data = json.loads(resp.data)
    assert isinstance(data, list)
    assert len(data) == 1
    check_order(data[0], 'True', None)

    # 7. Get details about order without token
    resp = orders.get('/api/orders/1')
    assert resp.status_code == 400

    # 8. Get details about order with wrong token
    resp = orders.get('/api/orders/1', headers={'Authorization': 'AAA'})
    assert resp.status_code == 401

    # 9. Get details about order
    resp = orders.get('/api/orders/1', headers={'Authorization': 'TESTING_TOKEN'})
    assert resp.status_code == 200
    data = json.loads(resp.data)
    check_order(data, 'True', [])

    # 10. Get details about non-existing order
    resp = orders.get('/api/orders/2', headers={'Authorization': 'TESTING_TOKEN'})
    assert resp.status_code == 404

    # 11. Add a beer without token
    resp = orders.put('/api/orders/current')
    assert resp.status_code == 400

    # 12. Add a beer with wrong token
    resp = orders.put('/api/orders/current')
    assert resp.status_code == 400

    # 13. Add a beer
    resp = orders.put('/api/orders/current', headers={'Authorization': 'TESTING_TOKEN'})
    assert resp.status_code == 400

    data = dict()
    data['sku'] = 'TESTING_SKU'
    data['quantity'] = '2'
    resp = orders.put('/api/orders/current', headers={'Authorization': 'TESTING_TOKEN'}, data=data)
    assert resp.status_code == 201

    resp = orders.get('/api/orders/current', headers={'Authorization': 'TESTING_TOKEN'})
    assert resp.status_code == 200
    data = json.loads(resp.data)
    check_order(data, 'True', [{'sku': 'TESTING_SKU', 'quantity': "2"}])

    # 14. Add more beer
    data = dict()
    data['sku'] = 'TESTING_SKU'
    data['quantity'] = '2'
    resp = orders.put('/api/orders/current', headers={'Authorization': 'TESTING_TOKEN'}, data=data)
    assert resp.status_code == 201

    resp = orders.get('/api/orders/current', headers={'Authorization': 'TESTING_TOKEN'})
    assert resp.status_code == 200
    data = json.loads(resp.data)
    check_order(data, 'True', [{'sku': 'TESTING_SKU', 'quantity': "4"}])

    # 15. Add another beer
    data = dict()
    data['sku'] = 'ANOTHER_TESTING_SKU'
    data['quantity'] = '2'
    resp = orders.put('/api/orders/current', headers={'Authorization': 'TESTING_TOKEN'}, data=data)
    assert resp.status_code == 201

    resp = orders.get('/api/orders/current', headers={'Authorization': 'TESTING_TOKEN'})
    assert resp.status_code == 200
    data = json.loads(resp.data)
    check_order(data, 'True', [{'sku': 'TESTING_SKU', 'quantity': "4"}, {'sku': 'ANOTHER_TESTING_SKU', 'quantity': "2"}])

    # 16. Add a non-existing beer
    data = dict()
    data['sku'] = 'NON_TESTING_SKU'
    data['quantity'] = '2'
    resp = orders.put('/api/orders/current', headers={'Authorization': 'TESTING_TOKEN'}, data=data)
    assert resp.status_code == 404

    # 17. Add negative quantity of beers
    data = dict()
    data['sku'] = 'NON_TESTING_SKU'
    data['quantity'] = -2
    resp = orders.put('/api/orders/current', headers={'Authorization': 'TESTING_TOKEN'}, data=data)
    assert resp.status_code == 400

    # 18. Remove another beer without token
    resp = orders.delete('/api/orders/current')
    assert resp.status_code == 400

    # 19. Remove another beer with wrong token
    resp = orders.delete('/api/orders/current', headers={'Authorization': 'AAA'})
    assert resp.status_code == 400
    resp = orders.delete('/api/orders/current', data=dict(sku='12345'), headers={'Authorization': 'AAA'})
    assert resp.status_code == 401

    # 20. Remove another beer
    resp = orders.delete('/api/orders/current', data=dict(sku='ANOTHER_TESTING_SKU'), headers={'Authorization': 'TESTING_TOKEN'})
    assert resp.status_code == 204
    resp = orders.get('/api/orders/current', headers={'Authorization': 'TESTING_TOKEN'})
    assert resp.status_code == 200
    data = json.loads(resp.data)
    check_order(data, 'True', [{'sku': 'TESTING_SKU', 'quantity': "4"}])

    # 21. Checkout without token
    resp = orders.get('/api/orders/checkout')
    assert resp.status_code == 400

    # 22. Checkout with wrong token
    resp = orders.get('/api/orders/checkout', headers={'Authorization': 'AAA'})
    assert resp.status_code == 401

    # 23. Checkout
    resp = orders.get('/api/orders/checkout', headers={'Authorization': 'TESTING_TOKEN'})
    assert resp.status_code == 200

    resp = orders.get('/api/orders/', headers={'Authorization': 'TESTING_TOKEN'})
    assert resp.status_code == 200
    data = json.loads(resp.data)
    assert isinstance(data, list)
    assert len(data) == 1
    check_order(data[0], 'False', None)
