import logging
import traceback
from sqlalchemy.orm.exc import NoResultFound
from flask_restx import Api
from flask import current_app

log = logging.getLogger(__name__)

api = Api(
    version='1.0',
    title='Beers API',
    description='A simple beers management API powered by Flask RestPlus'
)


@api.errorhandler
def default_error_handler(e):
    message = 'An unhandled exception occurred.'
    log.exception(message)

    if not current_app.config.FLASK_DEBUG:
        return {'message': message}, 500


@api.errorhandler(NoResultFound)
def database_not_found_error_handler(e):
    log.warning(traceback.format_exc())
    return {'message': 'A database result was required but none was found.'}, 404
