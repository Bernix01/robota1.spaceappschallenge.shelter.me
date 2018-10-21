"""
REST API Resource Routing
http://flask-restplus.readthedocs.io
"""
import json
from datetime import datetime
from flask import request
from flask_restplus import Resource
from flask_cors import cross_origin
from .security import require_auth
from .modis_robota1 import do_mcd12q1, do_mcd15a2h
from . import api_rest


class SecureResource(Resource):
    """ Calls require_auth decorator on all requests """
    method_decorators = [require_auth]


@api_rest.route('/map-resources/<string:resource_id>')
class MapResources(Resource):
    """ Gets the resources available from a lat,lng """

    def get(self, resource_id):
        if resource_id == "mcd12q1":
            return do_mcd12q1()
        if resource_id == "mcd15a2h":
            return do_mcd15a2h()
        return None, 400


@api_rest.route('/resource/<string:resource_id>')
class ResourceOne(Resource):
    """ Unsecure Resource Class: Inherit from Resource """

    def get(self, resource_id):
        timestamp = datetime.utcnow().isoformat()
        return {'timestamp': timestamp}

    def post(self, resource_id):
        json_payload = request.json
        return {'timestamp': json_payload}, 201


@api_rest.route('/secure-resource/<string:resource_id>')
class SecureResourceOne(SecureResource):
    """ Unsecure Resource Class: Inherit from Resource """

    def get(self, resource_id):
        timestamp = datetime.utcnow().isoformat()
        return {'timestamp': timestamp}
