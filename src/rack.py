import json
from flask import Flask, jsonify
from flask_restful import Api, Resource, reqparse, abort, marshal_with
from marshmallow import Schema, fields, post_load, EXCLUDE
from flask_apispec import doc
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

    @doc(description='Get All Racks in this PXE', tags=['Work in Progress Racks'])
    def get(self):
        utm = self.api.utm
        racks = utm.getRackCollection()
        # filter out the racks that are not in WIP
        wip = utm.getWipCollection()
        # print(wip)
        # compose a racksn list from the wip list
        racksn_list = list(map(lambda r: r.get('racksn'), wip))
        racks = [ r for r in racks if r.RACKSN in racksn_list]

        return json.dumps(racks, default=lambda o: o.__dict__)
    

class RackResource(MethodResource, Resource):

    def __init__(self, api) -> None:
        self.api = api

    @doc(description='Get Racks by Rack SN in this PXE', tags=['Work in Progress Racks'])
    def get(self, racksn):
        # return a single json rack instance
        utm = self.api.utm
        rack = utm.getRack(racksn)
        wip = utm.getWipCollection()
        racksn_list = list(map(lambda r: r.get('racksn'), wip))
        if rack.RACKSN not in racksn_list:
            rack = {}
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
            