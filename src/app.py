#!/usr/bin/env python3
from flask import Flask, request, redirect, render_template, url_for, session, jsonify
from flask_restful import Resource, Api, abort
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_apispec.extension import FlaskApiSpec

# from flask_restful_swagger_3 import Api, swagger
import logging
import os
import datetime
import json



# from uut import UutResource

from uut import Uut
from wip import Wip

app = Flask(__name__)
api = Api(app)
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
docs.register(Wip)
   

if __name__ == '__main__':
    app.run(debug=True)


   

