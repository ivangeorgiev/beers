import os
import logging.config
from flask import Flask, Blueprint, url_for, redirect
from .api import api
from .database import db
from .cli import commands as cli_commands
from .settings import Settings

logging_conf_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '../logging.conf'))
logging.config.fileConfig(logging_conf_path)
log = logging.getLogger(__name__)

def configure_app(app:Flask, local_settings=None):
    app.config.from_object(Settings)
    if local_settings:
        log.info('Local settings apply')
        app.config.from_object(local_settings)

def initialize_api(app):
    blueprint = Blueprint('api', __name__, url_prefix='/api')
    api.init_app(blueprint)

    import importlib
    for api_ref in app.config.get('APIS', []):
        api_module_name, api_attr_name =  f"{api_ref}:ns".split(':')[:2]
        log.info(f'API Load: {api_module_name}.{api_attr_name}')
        api_module = importlib.import_module(api_module_name, __package__)
        api_ns = getattr(api_module, api_attr_name)
        api.add_namespace(api_ns)
        log.info(f'API Initialized: {api_module_name}.{api_attr_name}')

    app.register_blueprint(blueprint)

    log.info('API initialize complete')

def initialize_db(app):
    app.db = db
    db.init_app(app)
    with app.app_context():
        if app.config.get('DATABASE_AUTO_DROP', False):
            log.info('Autodrop DB is ON')
            db.drop_all()
        if app.config.get('DATABASE_AUTO_CREATE', False):
            log.info('Autocreate DB is ON')
            db.create_all()
        if app.config.get('DATABASE_AUTO_SEED', False):
            log.info('Autoseed DB is ON')
            db.seed()
    app.log.info('Database initialized')

def initialize_cli(app):
    for cmd in cli_commands:
        app.cli.add_command(cmd)
    app.log.info('Cli initialized')

def initialize_app(app:Flask, settings:None):
    @app.route('/')
    def home():
        return redirect(url_for('api.root'))

    app.log = log
    configure_app(app, settings)
    initialize_api(app)
    initialize_db(app)
    initialize_cli(app)

def create_app(name=None, settings=None):
    if not name:
        name = __name__
    app = Flask(name)

    from werkzeug.middleware.proxy_fix import ProxyFix
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

    initialize_app(app, settings)
    return app

