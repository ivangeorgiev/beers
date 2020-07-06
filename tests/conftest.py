import os
import tempfile
import pytest

from users.app import app as users_app, initialize_app as initialize_users_app
from users.database import db as users_db
from beers.app import app as beers_app, initialize_app as initialize_beers_app
from beers.database import db as beers_db
from orders.app import app as orders_app, initialize_app as initialize_orders_app
from orders.database import db as orders_db


@pytest.fixture(scope='module')
def users():
    initialize_users_app(users_app)

    db_fd, users_app.config['DATABASE'] = tempfile.mkstemp()
    users_app.config['TESTING'] = True

    with users_app.test_client() as client:
        with users_app.app_context() as ctx:
            ctx.push()
            users_db.drop_all()
            users_db.create_all()

        yield client

    os.close(db_fd)
    os.unlink(users_app.config['DATABASE'])


@pytest.fixture(scope='module')
def beers():
    initialize_beers_app(beers_app)

    db_fd, beers_app.config['DATABASE'] = tempfile.mkstemp()
    beers_app.config['TESTING'] = True

    with beers_app.test_client() as client:
        with beers_app.app_context() as ctx:
            ctx.push()
            beers_db.drop_all()
            beers_db.create_all()

        yield client

    os.close(db_fd)
    os.unlink(beers_app.config['DATABASE'])


@pytest.fixture(scope='module')
def orders():
    initialize_orders_app(orders_app)

    db_fd, orders_app.config['DATABASE'] = tempfile.mkstemp()
    orders_app.config['TESTING'] = True

    with orders_app.test_client() as client:
        with orders_app.app_context() as ctx:
            ctx.push()
            orders_db.drop_all()
            orders_db.create_all()

        yield client

    os.close(db_fd)
    os.unlink(orders_app.config['DATABASE'])

