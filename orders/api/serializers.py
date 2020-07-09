from flask_restx import fields
from core.api import api

order_model = api.model('Order', {
    'id': fields.Integer(readOnly=True, description='The unique identifier of an order.'),
    'is_open': fields.String(required=True, description='Is the order opened.'),
    'time_created': fields.DateTime(required=True, description='Moment, in which the order was created.'),
    'time_modified': fields.DateTime(required=True, description='Moment, in which the order was last modified.'),
})

order_beer = api.model('Beer in an order', {
    'id': fields.Integer(readOnly=True, description='The unique identifier of a beer in an order.'),
    'sku': fields.String(required=True, description='Stock keeping unit.'),
    'quantity': fields.String(required=True, description='Ordered quantity of beer.'),
    'time_created': fields.DateTime(required=True, description='Moment, in which the beer in the order was created.'),
    'time_modified': fields.DateTime(required=True, description='Moment, in which the beer in the  order was last modified.'),
})

order_with_beers = api.inherit('Order with beers', order_model, {
    'beers': fields.List(fields.Nested(order_beer))
})
