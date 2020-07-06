from flask_restx import reqparse
from beers.database.models import Beer


def sku(value):
    check = Beer.query.filter_by(sku=value).first()
    if check:
        raise ValueError('SKU is already used.')
    return value


sku.__schema__ = {'type': 'string', 'format': 'SKU'}


authorization_arguments = reqparse.RequestParser()
authorization_arguments.add_argument('Authorization', type=str, required=True, help='Access token', location='headers')

beer_create_arguments = reqparse.RequestParser()
beer_create_arguments.add_argument('Authorization', type=str, required=True, help='Access token', location='headers')
beer_create_arguments.add_argument('sku', type=sku, required=True, help='Stock keeping unit', location='form')
beer_create_arguments.add_argument('name', type=str, required=True, help='Name', location='form')
beer_create_arguments.add_argument('price', type=float, required=True, help='Price per unit', location='form')
beer_create_arguments.add_argument('image', type=str, required=False, default=None, help='Image', location='form')


beer_modify_arguments = reqparse.RequestParser()
beer_modify_arguments.add_argument('Authorization', type=str, required=True, help='Access token', location='headers')
beer_modify_arguments.add_argument('name', type=str, required=True, help='Name', location='form')
beer_modify_arguments.add_argument('price', type=float, required=True, help='Price per unit', location='form')
beer_modify_arguments.add_argument('image', type=str, required=False, default=None, help='Image', location='form')
