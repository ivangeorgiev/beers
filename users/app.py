import os
import logging.config
from flask import Flask, Blueprint
from users.settings import Settings
from users.database import db
from users.api.restplus import api
from users.api.endpoints import users_ns


logging_conf_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '../logging.conf'))
logging.config.fileConfig(logging_conf_path)
log = logging.getLogger(__name__)


def configure_app(flask_app):
    flask_app.config['SERVER_NAME'] = Settings.FLASK_SERVER_NAME
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = Settings.SQLALCHEMY_DATABASE_URI
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = Settings.SQLALCHEMY_TRACK_MODIFICATIONS
    flask_app.config['SWAGGER_UI_DOC_EXPANSION'] = Settings.RESTPLUS_SWAGGER_UI_DOC_EXPANSION
    flask_app.config['RESTPLUS_VALIDATE'] = Settings.RESTPLUS_VALIDATE
    flask_app.config['RESTPLUS_MASK_SWAGGER'] = Settings.RESTPLUS_MASK_SWAGGER
    flask_app.config['ERROR_404_HELP'] = Settings.RESTPLUS_ERROR_404_HELP


def initialize_app(flask_app):
    configure_app(flask_app)
    blueprint = Blueprint('api', __name__, url_prefix='/api')
    api.init_app(blueprint)
    api.add_namespace(users_ns)
    flask_app.register_blueprint(blueprint)
    db.init_app(flask_app)


def serve_users(flask_app):
    initialize_app(flask_app)
    log.info('>>>>> Starting development server at http://{}/api/ <<<<<'.format(flask_app.config['SERVER_NAME']))
    flask_app.run(debug=Settings.FLASK_DEBUG)


def setup_users(flask_app):
    initialize_app(flask_app)
    flask_app.app_context().push()
    db.drop_all()
    db.create_all()
