from flask_restful import Resource
from flask_apispec import marshal_with, doc
from flask_apispec.views import MethodResource

from marshmallow import Schema, fields, post_load
from sfhand import SfHand


class UUTSchema(Schema):
    uutsn = fields.String(default='Success')

class RackSchema(Schema):
    location = fields.String()
    racksn = fields.String()
    uuts = fields.List(fields.Nested(UUTSchema))

class RackListSchema(Schema):
    racks = fields.List(fields.Nested(RackSchema))

class Wip(MethodResource, Resource):
    @doc(description='Get the list of WIP (Work In Place) racks', tags=['WIP'])
    @marshal_with(RackListSchema)
    def get(self):
        wip = SfHand().getWip()
        return { 'racks': wip }
