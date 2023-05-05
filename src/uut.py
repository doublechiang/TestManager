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
from flask_apispec.views import MethodResource
from marshmallow import Schema, fields, EXCLUDE, INCLUDE, post_load



class UutSchema(Schema):
    class Meta:
        unknown = EXCLUDE
    MLB = fields.String()
    CHASSISSN = fields.String()
    MLBSN= fields.String()
    BMCMAC = fields.String()

    @post_load
    def make_rack(self, data, **kwargs):
        return Uut(**data)

class UutListResource(MethodResource, Resource):
    def __init__(self, api) -> None:
        self.api = api

    def get(self):
        utm = self.api.utm
        uuts = utm.getUutCollection()
        return json.dumps(uuts, default=lambda o: o.__dict__)
    
class UutResource(MethodResource, Resource):
    def __init__(self, api) -> None:
        self.api = api

    def get(self, sn):
        utm = self.api.utm
        uut = utm.getUut(sn)
        return json.dumps(uut, default=lambda o: o.__dict__) 

    
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

