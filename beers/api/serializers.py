from flask_restx import fields
from core.api import api

beer_model = api.model('Beer', {
    'id': fields.Integer(readOnly=True, description='The unique identifier of a beer.'),
    'name': fields.String(required=True, description='Name of the beer.'),
    'sku': fields.String(required=True, description='Stock Keeping Unit'),
    'price': fields.String(required=True, description='Price of a single unit /bottle/ of beer.'),
    'image': fields.String(required=True, description='Image containing the beer.'),
    'time_created': fields.DateTime(required=True, description='Moment, in which the beer was created.'),
    'time_modified': fields.DateTime(required=True, description='Moment, in which the beer was last modified.'),
})
