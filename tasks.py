from beers import serve_beers, setup_beers
from orders import serve_orders, setup_orders
from users import serve_users, setup_users
from invoke import task


@task
def users(c, command):
    if command == 'serve':
        app = Flask(__name__)
        serve_users(app)

    if command == 'setup':
        app = Flask(__name__)
        setup_users(app)


@task
def beers(c, command):
    if command == 'serve':
        app = Flask(__name__)
        serve_beers(app)

    if command == 'setup':
        app = Flask(__name__)
        setup_beers(app)


@task
def orders(c, command):
    if command == 'serve':
        app = Flask(__name__)
        serve_orders(app)

    if command == 'setup':
        app = Flask(__name__)
        setup_orders(app)
