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
