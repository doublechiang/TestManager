import json
from flask import Flask, jsonify
from flask_restful import Api, Resource, reqparse, abort, marshal_with
from marshmallow import Schema, fields, post_load, EXCLUDE
from flask_apispec.views import MethodResource


class RackSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    RACKSN = fields.String(rqeuired=True)
    RACK_MOUNT_MAC1 = fields.String(required=True)

    # Build the Rack object from the schema
    @post_load
    def make_rack(self, data, **kwargs):
        return Rack(**data)
    

class RackList(MethodResource, Resource):

    def __init__(self, api) -> None:
        self.api = api

    def get(self):
        utm = self.api.utm
        racks = utm.getRackCollection()
        return json.dumps(racks, default=lambda o: o.__dict__)
    

class RackResource(MethodResource, Resource):

    def __init__(self, api) -> None:
        self.api = api

    def get(self, racksn):
        # return a single json rack instance
        utm = self.api.utm
        rack = utm.getRack(racksn)
        return json.dumps(rack, default=lambda o: o.__dict__) 

   
class Rack:
    ''' A Rack contain a list of UUTs
    '''
    def __init__(self, **kwargs) -> None:
        super().__init__()
        self.uuts = []
        for key, value in kwargs.items():
            setattr(self, key, value)
            
    # compare inssance of Rack instance
    def __eq__(self, __value: object) -> bool:
        return self.RACKSN == __value.RACKSN
    
    def updateUut(self, uut):
        ''' Update the UUTs list
        '''
        if uut not in self.uuts:
            self.uuts.append(uut)
        else:
            self.uuts[self.uuts.index(uut)] = uut

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__)
            