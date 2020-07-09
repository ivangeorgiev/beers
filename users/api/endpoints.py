import logging
from flask import request
from flask_restx import Resource
from core.api import api
from users.api.serializers import user, parse_token
from users.api.parsers import login_arguments, username_arguments, token_arguments, register_arguments
from users.database.models import User

log = logging.getLogger(__name__)

users_ns = api.namespace('users', description='Operations related to users')


@users_ns.route('/login')
class UserLogin(Resource):
    @api.expect(login_arguments)
    @api.marshal_with(parse_token)
    def post(self):
        """
        Get a token to access the systems.
        """
        args = login_arguments.parse_args(request)

        username = args.get('username')
        password = args.get('password')

        user = User.query.filter_by(username=username).first()
        if not user or not user.check_password(password.encode()):
            return {'message': 'Invalid username and / or password'}, 404

        if user.token is None:
            user.set_token()

        return {'token': user.token}


@users_ns.route('/logout')
class UserLogout(Resource):
    @api.expect(token_arguments)
    @api.marshal_with(parse_token)
    def post(self):
        """
        Clear a token so that it is no longer active.
        """
        args = token_arguments.parse_args(request)
        token = args.get('token')

        item = User.query.filter_by(token=token).first()
        if item is not None:
            item.clear_token()
            return True

        return {'message': 'Invalid token.'}, 404


@users_ns.route('/exists')
class UsernameExists(Resource):
    @api.expect(username_arguments)
    def get(self):
        """
        Check if an username is already used.
        """
        args = username_arguments.parse_args(request)
        username = args.get('username')
        item = User.query.filter_by(username=username).first()
        if item is not None:
            return True

        return False, 404


@users_ns.route('/check_token')
class CheckToken(Resource):
    @api.expect(token_arguments)
    @api.marshal_with(user)
    @api.response(404, 'Invalid token.')
    def post(self):
        """
        Check if a token is active and retrieve information about it's owner.
        """
        args = token_arguments.parse_args(request)
        token = args.get('token')

        item = User.query.filter_by(token=token).first()
        if item is not None:
            return item

        return None, 404


@users_ns.route('/register')
class UserRegister(Resource):
    @api.expect(register_arguments)
    @api.marshal_with(user)
    def post(self):
        """
        Register a new user.
        """
        args = register_arguments.parse_args(request)

        new_user = User.register(
            args.get('username'),
            args.get('mail'),
            args.get('first_name'),
            args.get('last_name')
        )

        new_user.set_token()
        new_user.set_password(args.get('password').encode())

        return new_user
