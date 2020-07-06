import logging
from flask import request
from flask_restx import Resource
from clients import UserClient
from beers.api.restplus import api
from beers.api.serializers import beer_model
from beers.api.parsers import beer_create_arguments, authorization_arguments, beer_modify_arguments
from beers.database.models import Beer

log = logging.getLogger(__name__)


beers_ns = api.namespace('beers', description='Operations related to beers')


@beers_ns.route('/')
class BeerCollection(Resource):
    @api.marshal_list_with(beer_model)
    def get(self):
        """
        Returns list of available beers.
        """
        return Beer.query.all()

    @api.response(201, 'Beer successfully created.')
    @api.response(401, 'You are not authorized to create beers.')
    @api.expect(beer_create_arguments)
    @api.marshal_with(beer_model)
    def post(self):
        """
        Creates a new beer.
        """
        args = beer_create_arguments.parse_args(request)

        client = UserClient()
        if not client.check_token(args.get('Authorization')):
            return None, 401

        new_beer = Beer.create(
            args.get('name'),
            args.get('sku'),
            args.get('price'),
            args.get('image')
        )

        return new_beer, 201


@beers_ns.route('/<sku>')
class BeerItem(Resource):
    @api.marshal_with(beer_model)
    @api.response(404, 'Beer not found.')
    def get(self, sku):
        """
        Find a beer by SKU.
        """

        # This is not the same depending on the debug mode, but returns a message on production
        # return Beer.query.filter_by(sku=sku).one()

        beer = Beer.query.filter_by(sku=sku).first()
        if beer is None:
            return None, 404
        return beer

    @api.expect(beer_modify_arguments)
    @api.marshal_with(beer_model)
    @api.response(401, 'You are not authorized to update beers.')
    @api.response(404, 'Beer does not exists.')
    def put(self, sku):
        """
        Updates a beer.
        """

        args = beer_modify_arguments.parse_args(request)

        client = UserClient()
        if not client.check_token(args.get('Authorization')):
            return None, 401

        beer = Beer.query.filter_by(sku=sku).first()
        if beer is None:
            return None, 404

        beer.modify(
            args.get('name'),
            args.get('price'),
            args.get('image')
        )

        return beer

    @api.response(204, 'Beer successfully deleted.')
    @api.response(401, 'You are not authorized to delete beers.')
    @api.expect(authorization_arguments)
    def delete(self, sku):
        """
        Deletes a beer.
        """

        args = authorization_arguments.parse_args(request)

        client = UserClient()
        if not client.check_token(args.get('Authorization')):
            return None, 401

        beer = Beer.query.filter_by(sku=sku).first()
        if beer is None:
            return None, 404

        beer.delete()
        return None, 204
