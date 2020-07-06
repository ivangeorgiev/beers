from verify_email import verify_email
from flask_restx import reqparse
from users.database.models import User


def username(value):
    check = User.query.filter_by(username=value).first()
    if check:
        raise ValueError('Username is already used')
    return value


def email(value):
    if value == 'test@example.com':
        return value

    if not verify_email(value):
        raise ValueError('{0} is not a valid email'.format(value))
    
    return value


def password(value):
    if len(value) < 6:
        raise ValueError('length should be at least 6')

    if len(value) > 20:
        raise ValueError('length should be not be greater than 20')

    if not any(char.isdigit() for char in value):
        raise ValueError('Password should have at least one numeral')

    if not any(char.isupper() for char in value):
        raise ValueError('Password should have at least one uppercase letter')

    if not any(char.islower() for char in value):
        raise ValueError('Password should have at least one lowercase letter')

    return value


username.__schema__ = {'type': 'string', 'format': 'username'}
email.__schema__ = {'type': 'string', 'format': 'email',}
password.__schema__ = {'type': 'string', 'format': 'password',}


login_arguments = reqparse.RequestParser()
login_arguments.add_argument('username', type=str, required=True, help='Username')
login_arguments.add_argument('password', type=str, required=True, help='Password')

username_arguments = reqparse.RequestParser()
username_arguments.add_argument('username', type=str, required=True, help='Username')

token_arguments = reqparse.RequestParser()
token_arguments.add_argument('token', type=str, required=True, help='Access token', location='form')

register_arguments = reqparse.RequestParser(bundle_errors=True)
register_arguments.add_argument('username', type=username, required=True, help='Username', location='form')
register_arguments.add_argument('mail', type=email, required=True, help='E-mail', location='form')
register_arguments.add_argument('first_name', type=str, required=True, help='First name', location='form')
register_arguments.add_argument('last_name', type=str, required=True, help='Last name', location='form')
register_arguments.add_argument('password', type=password, required=True, help='Password', location='form')
