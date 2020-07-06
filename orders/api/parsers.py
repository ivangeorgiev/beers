from flask_restx import reqparse

authorization_arguments = reqparse.RequestParser()
authorization_arguments.add_argument('Authorization', type=str, required=True, help='Access token', location='headers')

add_beer_arguments = reqparse.RequestParser()
add_beer_arguments.add_argument('Authorization', type=str, required=True, help='Access token', location='headers')
add_beer_arguments.add_argument('sku', type=str, required=True, help='Stock keeping unit', location='form')
add_beer_arguments.add_argument('quantity', type=int, required=True, help='Quantity', location='form')

remove_beer_arguments = reqparse.RequestParser()
remove_beer_arguments.add_argument('Authorization', type=str, required=True, help='Access token', location='headers')
remove_beer_arguments.add_argument('sku', type=str, required=True, help='Stock keeping unit', location='form')
