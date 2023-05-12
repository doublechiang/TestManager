#!/usr/bin/env python3
from flask import Flask, request, redirect, render_template, url_for, session, jsonify, current_app
from flask_restful import Resource, Api, abort
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_apispec.extension import FlaskApiSpec

# from flask_restful_swagger_3 import Api, swagger
import logging
import os
import datetime
import json

from wip import Wip
from sfhand import SfHand
from racktm import UUTManager
from rack import RackList, RackResource
from uut import UutListResource, UutResource

app = Flask(__name__)
api = Api(app)
api.utm = UUTManager()
# api.utm.start('../seeds/WIN')
api.utm.start('/WIN')
app.config['APPLICATION_ROOT'] = 'RackTestManager'
# logging.basicConfig(level=logging.WARNING)
logging.basicConfig(level=logging.DEBUG)

app.config.update({
    'APISPEC_SPEC': APISpec(
        title='UUT Test Manager',
        version='v1',
        plugins=[MarshmallowPlugin()],
        openapi_version='2.0.0'
    ),
    'APISPEC_SWAGGER_URL': '/swagger/',  # URI to access API Doc JSON 
    'APISPEC_SWAGGER_UI_URL': '/swagger-ui/'  # URI to access UI of API Doc
})

docs = FlaskApiSpec(app)
api.add_resource(Wip, '/wip')
api.add_resource(SfHand, '/sfhand')
api.add_resource(RackList, '/racks', '/racks/', resource_class_kwargs={'api': api})
api.add_resource(RackResource, '/racks/<string:racksn>', resource_class_kwargs={'api': api})
api.add_resource(UutListResource, '/uuts', '/uuts/', resource_class_kwargs={'api': api})
api.add_resource(UutResource, '/uuts/<string:sn>', resource_class_kwargs={'api': api})
docs.register(Wip, endpoint='wip')
docs.register(SfHand, endpoint='sfhand')
docs.register(RackList, resource_class_kwargs={'api': api})
docs.register(RackResource, resource_class_kwargs={'api': api})
docs.register(UutListResource, resource_class_kwargs={'api': api})
docs.register(UutResource, resource_class_kwargs={'api': api})
   

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5030)


   

