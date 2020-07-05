import os
import logging.config
from flask import Flask, Blueprint
from beers.settings import Settings
from beers.database import db
from beers.api.restplus import api
from beers.api.endpoints import beers_ns


app = Flask(__name__)


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
    api.add_namespace(beers_ns)
    flask_app.register_blueprint(blueprint)
    db.init_app(flask_app)


def serve_beers():
    initialize_app(app)
    log.info('>>>>> Starting development server at http://{}/api/ <<<<<'.format(app.config['SERVER_NAME']))
    app.run(debug=Settings.FLASK_DEBUG)


def setup_beers():
    initialize_app(app)
    app.app_context().push()
    db.drop_all()
    db.create_all()

    from beers.database.models import Beer
    Beer.create('Бургаско', 123456, 1.19, 'https://cdncloudcart.com/15635/products/images/206/bira-burgasko-svetlo-500-ml-ken-image_5e24491fc2a15_800x800.jpeg?1579436338')
    Beer.create('Загорка', 123457, 2.00, 'https://shami.bg/uploads/2019/06/38b3674a0aaee5a32c1193d8cab7104b.png')
    Beer.create('Tuborg', 123458, 1.50, 'https://cdn.nokovandson.com/crop/276/490/480//I0/I0pLF5nGwJ.png')

