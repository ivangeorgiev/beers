import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Settings(object):
    APIS = ['beers.api.endpoints:beers_ns', 'users.api.endpoints:users_ns', 'orders.api.endpoints:order_ns']
    # Flask settings
    FLASK_SERVER_NAME = os.environ.get('FLASK_SERVER_NAME') or 'localhost:5000'
    FLASK_DEBUG = False  # Do not use debug mode in production
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    # SQLAlchemy settings
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, '..', 'db.sqlite3')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    DATABASE_AUTO_DROP = os.environ.get('DATABASE_AUTO_DROP', 'No').upper() in ['Y', 'YES', 'TRUE']
    DATABASE_AUTO_CREATE = os.environ.get('DATABASE_AUTO_CREATE', 'Yes').upper() in ['Y', 'YES', 'TRUE']
    DATABASE_AUTO_SEED = os.environ.get('DATABASE_AUTO_SEED', 'No').upper() in ['Y', 'YES', 'TRUE']
    # Flask-Restplus settings
    RESTPLUS_SWAGGER_UI_DOC_EXPANSION = 'list'
    RESTPLUS_VALIDATE = True
    RESTPLUS_MASK_SWAGGER = False
    RESTPLUS_ERROR_404_HELP = False
