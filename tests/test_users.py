import json


def test_login(users, beers, orders):
    resp = users.get('/api/users/exists', query_string={'username': 'hristo'})
    assert resp.status_code == 404
    
    data = {'username': 'hristo', 'mail': 'hristo.i.georgiev@gmail.com', 'first_name': 'Hristo', 'last_name': 'Georgiev', 'password': '4csTJdx4'}
    resp = users.post('/api/users/register', data=data)
    
    assert resp.status_code == 200
    
    resp = users.get('/api/users/exists', query_string={'username': 'hristo'})
    assert resp.status_code == 200
    
    resp = users.post('/api/users/login', data={'username': 'hristo', 'password': '4csTJdx4'})
    data = json.loads(resp.data)
    token = data['token']
    
    resp = users.post('/api/users/check_token', data={'token': token})
    assert resp.status_code == 200
    
    resp = users.post('/api/users/check_token', data={'token': token + '@@@'})
    assert resp.status_code == 404
    
    resp = users.post('/api/users/logout', data={'token': token})
    assert resp.status_code == 200
    
    resp = users.post('/api/users/logout', data={'token': token})
    assert resp.status_code == 404
    
    resp = users.post('/api/users/check_token', data={'token': token})
    assert resp.status_code == 404

