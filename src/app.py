#!/usr/bin/env python3
from flask import Flask, request, redirect, render_template, url_for, session, jsonify
from flask_restful import Resource, abort
from flask_restful_swagger_3 import Api, swagger
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

api.add_resource(Wip, '/wip')
   

if __name__ == '__main__':
    app.run(debug=True)


   

