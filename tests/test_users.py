from clients import UserClient


def test_login(users):
    resp = users.get('/api/users/exists', query_string={'username': 'hristo'})
    assert resp.status_code == 404

    

    print(dir(resp))

    assert users.get('/api/users/exists')


    return

    client = UserClient()
    if not client.exists('hristo'):
        success, data = client.register('hristo', 'hristo.i.georgiev@gmail.com', 'Христо', 'Георгиев', 'P@r0lata20')
        if not success:
            print(data)
            return

    token = client.login('hristo', 'P@r0lata20')
    print(client.check_token(token))
    print(client.check_token(token + '@@@'))
    print(client.logout(token))
    print(client.logout(token))
