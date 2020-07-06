from flask_restx import fields
from users.api.restplus import api

user = api.model('User', {
    'id': fields.Integer(readOnly=True, description='The unique identifier of an user.'),
    'username': fields.String(required=True, description='Username.'),
    'email': fields.String(required=True, description='E-mail address of the user.'),
    'first_name': fields.String(required=True, description='First name of the user.'),
    'last_name': fields.String(required=True, description='Last name of the user.'),
    'time_registered': fields.DateTime(required=True, description='Moment, in which the user was registered.'),
    'time_modified': fields.DateTime(required=True, description='Moment, in which the user was last modified.'),
})


parse_token = api.model('Access token', {
    'token': fields.String(required=True, description='Token to access the systems.')
})
