import sys
import logging
import os
import csv
import shutil, time
import configparser
from flask import request
from flask_restful import fields, marshal_with
from flask_restful import Resource
from flask_apispec import marshal_with, doc, use_kwargs
from flask_apispec.views import MethodResource
from marshmallow import Schema, fields, validate, ValidationError


import settings

def validate_requestor(requstor):
    valid_requestor= ['UUTConfig2', 'Linkall', 'Status']
    if requstor not in valid_requestor:
        raise ValidationError(f'Invalid requestor {requstor}, should be one of {valid_requestor}')

class SfRequestSchema(Schema):
    """ Schema for the request
        Status: Message send to Status, include the MBSN, Station and Status.
        Request: UUTConfig2, Linkall, etc, include the MBSN, Request
    """

    FN = fields.String()                    # Filename, for backward compatibility
    MBSN = fields.String(required=True)     # Mainboard serial number
    IP = fields.String()
    Request= fields.String(required=True, validate=validate_requestor)   # UUTConfig2, Linkall, etc
    Model = fields.String(required=True)                 # Model number
    Station = fields.String()               # FAT, RUNNIN, etc.
    Status = fields.String()                # Message Send to Status


class SfResponseSchema(Schema):
    MBSN = fields.String(required=True)     # Mainboard serial number


@doc(description='ShopFloor Acesss API', tags=['ShopFloor'])
class SfHand(MethodResource, Resource):
    SF_HOST='192.168.204.9'
    SF_SHARE='Monitor'
    SF_WIP_LISTING_FN = 'CurrentRackData.csv'
    SF_RACKDEFPATH='NetApp\\SNLIST\\{}'.format(SF_WIP_LISTING_FN)

    WIN_FOLDER='/WIN/'
  

    def getWip(self):
        """ Get the list of WIP (Work In Place) racks
        """
        cmd = "smbclient --user='{}%{}' '//{}/{}' -c 'get {} {}'".format(settings.SF_SHAREUSER, settings.SF_SHAREPASS, self.SF_HOST, self.SF_SHARE, self.SF_RACKDEFPATH, self.SF_WIP_LISTING_FN)
        logging.debug(cmd)
        try:
            os.system(cmd)
        except Exception as e:
            logging.error(e)
            return None

        wip = dict()

        with open(self.SF_WIP_LISTING_FN, 'r') as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=',')
            header = False
            # A row contain the list of location, rack serial, uut serial
            for row in csv_reader:
                if header is False:
                    header = True
                    continue
                # Create the dictionary use rack serial as the key and location as the value, and the list of the uut serial
                location, racksn, uutsn= row[0], row[1], row[2]
                rack = wip.get(row[1], dict())
                rack['location'] = location
                rack['racksn']  = racksn
                uuts = rack.get('uuts', [])
                if uutsn not in uuts:
                    uuts.append({'uutsn': uutsn})
                rack['uuts'] = uuts
                wip.update({racksn: rack})

        os.unlink(self.SF_WIP_LISTING_FN)
                
        return list(wip.values())

    @use_kwargs(SfRequestSchema)
    @marshal_with(SfResponseSchema)
    def post(self, **kwargs):
        """ ShopFloor Acesss API, POST method
            The request body should be a JSON object, with the following fields:
            L10 Request sample:

            'Model' : 'NetApp'
            'MBSN' : 'B41222423233703A'
            'FN': 'B41222423233703A.txt'
            'Request' : 'UUTConfig2' or 'Linkall' or 'Status'

        """
        logging.debug(request)

        try:
            print(request.json)
            SfRequestSchema().load(request.json)
        except ValidationError as e:
            logging.error(e)

        # MBSN is required field, if FN is not exist, use MBSN as the filename
        fn = request.json.get('FN', request.json.get('MBSN'))
        with open(f'{fn}.txt', 'w') as f:
            # werite kwargs to the file
            for key, value in kwargs.items():
                if key in ['FN']:
                    continue
                f.write(f'{key}={value}\n')

        try:
            request_foder = f'{self.WIN_FOLDER}/{request.json.get("Model")}/Request'
            respond_file = f'{self.WIN_FOLDER}/{request.json.get("Model")}/Response/{fn}.txt'
            shutil.copy(f'{fn}.txt', request_foder)
            os.unlink(f'{fn}.txt')
            if self.__wait_for(respond_file):
                respond_dict=self.__map_ini_to_dict(respond_file)
                
            else:
                error = f'shopflow respone file {self.RES_FOLDER + req_fn} not found.'
        except Exception as e:
            logging.error(e)
            error = e
        return respond_dict, 201
    
    def __wait_for(self, fn, timeout=100):
        timeout = time.time() + timeout
        while os.path.isfile(fn) is not True:
            time.sleep(5)
            if time.time() > timeout:
                return False
        return True
    
    def __map_ini_to_dict(self, fname):
        """ Convert the ini file to dictionary
            return the dictionary
        """
        config = configparser.RawConfigParser()
        with open(fname) as stream:
            stream = "[dummy]\n" + stream.read()

        config.read_string(stream)
        return {k:v for k, v in config['dummy'].items()}


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG,
                         format='%(asctime)s - %(message)s',
                         datefmt='%Y-%m-%d %H:%M:%S')
    # path = sys.argv[1] if len(sys.argv) > 1 else '.'
    # # event_handler = LoggingEventHandler()
    # event_handler = FsEvtHandler()
    # observer = Observer()
    # observer.schedule(event_handler, path, recursive=True)
    # observer.start()
    # try:
    #     while observer.is_alive():
    #         observer.join(1)
    # finally:
    #     observer.stop()
    #     observer.join()
    SfHand().getWip()