from beers import serve_beers, setup_beers
from orders import serve_orders, setup_orders
from users import serve_users, setup_users
from invoke import task


@task
def users(c, command):
    if command == 'serve':
        serve_users()

    if command == 'setup':
        setup_users()

    if command == 'dev':
        from clients import UserClient
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


@task
def beers(c, command):
    if command == 'serve':
        serve_beers()

    if command == 'setup':
        setup_beers()

@task
def orders(c, command):
    if command == 'serve':
        serve_orders()

    if command == 'setup':
        setup_orders()
