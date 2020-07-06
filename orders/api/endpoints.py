import logging
from flask import request
from flask_restx import Resource
from clients import UserClient, BeerClient

from orders.api.restplus import api
from orders.api.serializers import order_model, order_with_beers
from orders.api.parsers import authorization_arguments, add_beer_arguments, remove_beer_arguments
from orders.database.models import Order

log = logging.getLogger(__name__)


order_ns = api.namespace('orders', description='Operations related to orders')


@order_ns.route('/')
class OrderCollection(Resource):
    @api.response(401, 'You are not authorized to see orders.')
    @api.expect(authorization_arguments)
    @api.marshal_list_with(order_model)
    def get(self):
        """
        Returns list of current user's orders.
        """

        args = authorization_arguments.parse_args(request)

        client = UserClient()
        user = client.check_token(args.get('Authorization'))
        if not user:
            return None, 401

        return Order.query.filter_by(owner_id=user['id']).all()


@order_ns.route('/current')
class OrderItem(Resource):
    @api.response(401, 'You are not authorized to see orders.')
    @api.expect(authorization_arguments)
    @api.marshal_with(order_with_beers)
    def get(self):
        """
        Returns opened order of current user.
        """

        args = authorization_arguments.parse_args(request)

        client = UserClient()
        user = client.check_token(args.get('Authorization'))
        if not user:
            return None, 401

        return Order.get_opened_order(user['id'])

    @api.response(201, 'Beer successfully added to order.')
    @api.response(401, 'You are not authorized to add beers.')
    @api.response(404, 'Beer does not exist.')
    @api.expect(add_beer_arguments)
    def put(self):
        """
        Adds a quantity of beers to the opened order of current user.
        """
        args = add_beer_arguments.parse_args(request)

        if args.get('quantity') <= 0:
            return None, 400

        client = UserClient()
        user = client.check_token(args.get('Authorization'))
        if not user:
            return None, 401

        beers = BeerClient()
        if not beers.get(args.get('sku')):
            return None, 404

        order = Order.get_opened_order(user['id'])
        order.add_beer(args.get('sku'), args.get('quantity'))

        return None, 201

    @api.response(204, 'Beer successfully removed from order.')
    @api.response(401, 'You are not authorized to remove beers.')
    @api.expect(remove_beer_arguments)
    def delete(self):
        """
        Remove beers from the opened order of current user.
        """
        args = remove_beer_arguments.parse_args(request)

        client = UserClient()
        user = client.check_token(args.get('Authorization'))
        if not user:
            return None, 401

        order = Order.get_opened_order(user['id'])
        order.remove_beer(args.get('sku'))

        return None, 204


@order_ns.route('/checkout')
@api.expect(authorization_arguments)
class OrderCheckout(Resource):
    @api.response(200, 'Order was checked out.')
    @api.response(401, 'You are not authorized to checkout an order.')
    def get(self):
        """
        Checks out the user's current order
        """
        args = authorization_arguments.parse_args(request)

        client = UserClient()
        user = client.check_token(args.get('Authorization'))
        if not user:
            return None, 401

        order = Order.get_opened_order(user['id'])
        order.checkout()

        return None, 200


@order_ns.route('/<int:id>')
@api.expect(authorization_arguments)
class OrderDetails(Resource):
    @api.response(401, 'You are not authorized to search orders.')
    @api.marshal_with(order_with_beers)
    def get(self, id):
        """
        Get details about an order
        """
        args = authorization_arguments.parse_args(request)

        client = UserClient()
        user = client.check_token(args.get('Authorization'))
        if not user:
            return None, 401

        order = Order.query.filter_by(owner_id=user['id'], id=id).first()
        if order is None:
            return None, 404

        return order
