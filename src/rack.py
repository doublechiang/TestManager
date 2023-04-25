from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from marshmallow import Schema, fields


class RackSchema(Schema):
    racksn = fields.String(rqeuired=True)
    rack_mount_mac1 = fields.String(required=True)


class RackList(Resource):
    def get(self):
        return {'rack': 'rack1'}
    

class Rack(Resource):
    pass
    
            