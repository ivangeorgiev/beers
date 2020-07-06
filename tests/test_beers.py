import json


def check_beer(beer, name, sku, price):
    assert isinstance(beer, dict)
    assert 'name' in beer
    assert 'sku' in beer
    assert 'price' in beer
    assert beer['name'] == name
    assert beer['sku'] == sku
    assert beer['price'] == price


def test_products(users, beers, orders):
    # 1. List the beers and check that they installed correctly
    resp = beers.get('/api/beers/')
    assert resp.status_code == 200
    data = json.loads(resp.data)
    assert isinstance(data, list)
    assert len(data) == 3
    check_beer(data[0], 'Бургаско', '123456', '1.19')
    check_beer(data[1], 'Загорка', '123457', '2.00')
    check_beer(data[2], 'Tuborg', '123458', '1.50')
    
    # 2. Get a non-existing beer by SKU
    resp = beers.get('/api/beers/123')
    assert resp.status_code == 404
    
    # 2. Get an existing beer by SKU
    resp = beers.get('/api/beers/123456')
    assert resp.status_code == 200

    data = dict()
    data['sku'] = 6060
    data['name'] = 'Kozel'
    data['price'] = '2.50'
    
    # 3. Try to create a beer without token
    resp = beers.post('/api/beers/', data=data)
    assert resp.status_code == 400
    
    # 4. Try to create a beer with invalid token
    resp = beers.post('/api/beers/', data=data, headers={'Authorization': 'AAA'})
    assert resp.status_code == 401
    
    # 5. Create a beer with valid token
    resp = beers.post('/api/beers/', data=data, headers={'Authorization': 'TESTING_TOKEN'})
    assert resp.status_code == 201
    beer = json.loads(resp.data)
    check_beer(beer, 'Kozel', '6060', '2.50')

    resp = beers.get('/api/beers/')
    assert resp.status_code == 200
    data = json.loads(resp.data)
    assert isinstance(data, list)
    assert len(data) == 4

    data = dict()
    data['name'] = 'Heiniken'
    data['price'] = '3.50'

    # 6. Try to modify a beer without token
    resp = beers.put('/api/beers/6060', data=data)
    assert resp.status_code == 400

    # 7. Modify a beer with wrong token
    resp = beers.put('/api/beers/6060', data=data, headers = {'Authorization': 'AAA'})
    assert resp.status_code == 401

    # 8. Modify a beer
    resp = beers.put('/api/beers/6060', data=data, headers={'Authorization': 'TESTING_TOKEN'})
    assert resp.status_code == 200
    beer = json.loads(resp.data)
    check_beer(beer, 'Heiniken', '6060', '3.50')

    # 9. Modify a non-existing beer
    resp = beers.put('/api/beers/6061', data=data, headers={'Authorization': 'TESTING_TOKEN'})
    assert resp.status_code == 404

    # 10. Delete a beer without token
    resp = beers.delete('/api/beers/6060', data=data)
    assert resp.status_code == 400

    # 11. Delete a beer with wrong token
    resp = beers.delete('/api/beers/6060', data=data, headers={'Authorization': 'AAA'})
    assert resp.status_code == 401

    # 12. Delete a beer
    resp = beers.delete('/api/beers/6060', data=data, headers={'Authorization': 'TESTING_TOKEN'})
    assert resp.status_code == 204

    # 13. Modify a non-existing beer
    resp = beers.delete('/api/beers/6060', data=data, headers={'Authorization': 'TESTING_TOKEN'})
    assert resp.status_code == 404

    resp = beers.get('/api/beers/')
    assert resp.status_code == 200
    data = json.loads(resp.data)
    assert isinstance(data, list)
    assert len(data) == 3
