import json


def check_beer(product, name):
    pass


def test_products(users, beers, orders):
    # 1. we list the beers and check that they installed correctly
    resp = beers.get('/api/beers/')
    print(resp.status_code)
    print(resp.data)
    
    # 2.
    # 3.
    # 4.
    # 5.
    
    pass
