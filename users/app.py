import os
import logging.config
from flask import Flask, Blueprint
from core.settings import Settings
from core.database import db
from core.api import api
from users.api.endpoints import users_ns
from core.cli import commands as cli_commands

app = Flask(__name__)

logging_conf_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '../logging.conf'))
logging.config.fileConfig(logging_conf_path)
log = logging.getLogger(__name__)


def configure_app(flask_app):
    flask_app.config.from_object(Settings)
    try:
        from users.settings import Settings as LocalSettings
        log.info('Local settings apply')
        flask_app.config.from_object(LocalSettings)
    except ImportError:
        pass
    except Exception as exc:
        raise exc


def initialize_app(flask_app):
    configure_app(flask_app)
    blueprint = Blueprint('api', __name__, url_prefix='/api')
    api.init_app(blueprint)
    api.add_namespace(users_ns)
    flask_app.register_blueprint(blueprint)
    db.init_app(flask_app)
    app.db = db
    for cmd in cli_commands:
        app.cli.add_command(cmd)
