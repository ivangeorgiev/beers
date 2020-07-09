import os
import logging.config
from flask import Flask, Blueprint
from .api import api
from .database import db
from .cli import commands as cli_commands
from .settings import Settings

def configure_app(app:Flask):
    app.config.from_object(Settings)
    pass

def initialize_app(flask_app):
    configure_app(flask_app)
    blueprint = Blueprint('api', __name__, url_prefix='/api')
    api.init_app(blueprint)

    from beers.api.endpoints import beers_ns
    from users.api.endpoints import users_ns
    from orders.api.endpoints import order_ns

    api.add_namespace(beers_ns)
    api.add_namespace(users_ns)
    api.add_namespace(order_ns)
    flask_app.register_blueprint(blueprint)
    flask_app.db = db
    db.init_app(flask_app)


def initialize_cli(app):
    for cmd in cli_commands:
        app.cli.add_command(cmd)

def create_app():
    app = Flask(__name__)
    initialize_app(app)
    initialize_cli(app)
    return app

