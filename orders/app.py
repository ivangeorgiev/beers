import os
import logging.config
from flask import Flask, Blueprint
from core.settings import Settings
from core.database import db
from core.api import api
from orders.api.endpoints import order_ns

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
    api.add_namespace(order_ns)
    flask_app.register_blueprint(blueprint)
    db.init_app(flask_app)


def serve_orders(flask_app):
    initialize_app(flask_app)
    log.info('>>>>> Starting development server at http://{}/api/ <<<<<'.format(flask_app.config['SERVER_NAME']))
    flask_app.run(debug=Settings.FLASK_DEBUG)


def setup_orders(flask_app):
    initialize_app(flask_app)
    flask_app.app_context().push()
    db.drop_all()
    db.create_all()
