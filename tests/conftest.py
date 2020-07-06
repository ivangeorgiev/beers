import os
import tempfile
import pytest
from flask import Flask

from users.app import initialize_app as initialize_users_app
from users.database import db as users_db
from beers.app import initialize_app as initialize_beers_app
from beers.database import db as beers_db
from orders.app import initialize_app as initialize_orders_app
from orders.database import db as orders_db


@pytest.fixture(scope='module')
def users():
    app = Flask(__name__)
    
    initialize_users_app(app)
    
    db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    app.config['TESTING'] = True
    
    with app.test_client() as client:
        with app.app_context() as ctx:
            ctx.push()
            users_db.drop_all()
            users_db.create_all()
    
        yield client
    
    os.close(db_fd)
    os.unlink(app.config['DATABASE'])


@pytest.fixture(scope='module')
def beers():
    app = Flask(__name__)
    
    initialize_beers_app(app)
    
    db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    app.config['TESTING'] = True

    with app.test_client() as client:
        with app.app_context() as ctx:
            ctx.push()
            beers_db.drop_all()
            beers_db.create_all()
            
            from beers.database.models import Beer
            Beer.seed()
            
        yield client

    os.close(db_fd)
    os.unlink(app.config['DATABASE'])


@pytest.fixture(scope='module')
def orders():
    app = Flask(__name__)
    
    initialize_orders_app(app)
    
    db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    app.config['TESTING'] = True
    
    with app.test_client() as client:
        with app.app_context() as ctx:
            ctx.push()
            orders_db.drop_all()
            orders_db.create_all()
    
        yield client
    
    os.close(db_fd)
    os.unlink(app.config['DATABASE'])

