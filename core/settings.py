import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Settings(object):
    # Flask settings
    FLASK_SERVER_NAME = os.environ.get('FLASK_SERVER_NAME') or 'localhost:5000'
    FLASK_DEBUG = False  # Do not use debug mode in production
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    # SQLAlchemy settings
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, '..', 'db.sqlite3')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Flask-Restplus settings
    RESTPLUS_SWAGGER_UI_DOC_EXPANSION = 'list'
    RESTPLUS_VALIDATE = True
    RESTPLUS_MASK_SWAGGER = False
    RESTPLUS_ERROR_404_HELP = False
