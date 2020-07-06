import os
import tempfile
import pytest

from users.app import app as users_app, initialize_app
from users.database import db as users_db


@pytest.fixture(scope='module')
def users():
    initialize_app(users_app)

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

