#!/usr/bin/env python3
import os
import logging
import urllib
import subprocess
import json

from flask_restful import Resource, abort
from flask import jsonify
from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_apispec import doc
from flask_apispec.views import MethodResource
from marshmallow import Schema, fields, EXCLUDE, INCLUDE, post_load



class UutSchema(Schema):
    class Meta:
        unknown = INCLUDE
    MLB = fields.String()
    CHASSISSN = fields.String()
    MLBSN= fields.String()
    BMCMAC = fields.String()
    RACKSN = fields.String()

    @post_load
    def make_rack(self, data, **kwargs):
        return Uut(**data)

class UutListResource(MethodResource, Resource):
    def __init__(self, api) -> None:
        self.api = api

    @doc(description='Get All UUTs in this PXE', tags=['Work in Progress UUTs'])
    def get(self):
        utm = self.api.utm
        uuts = utm.getUutCollection()
        # filter out the uuts that are not in WIP, the WIP uut is based on the racksn
        # Check the UUT validility from the racksn then if teh uuts is under the racksn.
        wip = utm.getWipCollection()
        racksn_list = list(map(lambda r: r.get('racksn'), wip))
        # if the rack is not in the wip, then the uut is not in the wip
        uuts = [ u for u in uuts if u.RACKSN in racksn_list]
        # TODO, check the UUT validation from the racksn. the WIP rack should contain the WIP UUT.
            
        return json.loads(json.dumps(uuts, default=lambda o: o.__dict__))
    
class UutResource(MethodResource, Resource):
    def __init__(self, api) -> None:
        self.api = api

    @doc(description='Get UUT by Serial number in this PXE', tags=['Work in Progress UUTs'])
    def get(self, sn):
        utm = self.api.utm
        uut = utm.getUut(sn)
        return json.loads(json.dumps(uut, default=lambda o: o.__dict__))

    
class Uut:
    def __init__(self, **kwargs) -> None:
        super().__init__()
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __eq__(self, __value: object) -> bool:
        return self.MLBSN == __value.MLBSN
   


if __name__ == '__main__':
    # print(vars(Uut.parse_file('./samples/WIN/Response/P81251401000101E.txt')))
    # uuts = Uut.parse_dir('samples/WIN/Response')
    # for u in uuts:
    #     print(u.str_to_mac(u.bmcmac))
    Uut.getRDPTunnelCmd()
    pass

