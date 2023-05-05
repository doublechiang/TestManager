import logging
import configparser
import os
from marshmallow import Schema, fields, EXCLUDE

from rack import Rack, RackSchema
from uut import Uut, UutSchema

class ResponseConfig:

    ''' Response config file operation class
    '''

    @staticmethod
    def parse_file(fname):
        """ return the dictionary of the config file.
        """
        uut_dict = {}
        cfg_parser = configparser.RawConfigParser()
        with open(fname) as stream:
            stream = "[dummy]\n" + stream.read()

        try:
            cfg_parser.optionxform = str                           # disable the case sensitive     
            cfg_parser.read_string(stream)
            # below line get single attribute    
            # mac = cfg_parser.get('dummy', 'BMCMAC')
        except:
            logging.error("Processsing file {} with exception!".format(fname))
            return None

        # if the txt file do not contain the [END] section, it's not a valid config file
        if 'END' not in cfg_parser.sections():
            logging.error(f"There is no [END] section in the config file {fname}")
            return None

        uut_dict = {k:v for k, v in cfg_parser['dummy'].items()}

        # create instance based on the dictionary so that we can access it under attribute.
        return uut_dict
    

    def parseConfig(self, fname):
        ''' A Config file contains rack information and uut information 
            parse the config and return a rack instance and uut instance.
        '''
        cfg_dict = ResponseConfig.parse_file(fname)
        try:
            rack = RackSchema().load(cfg_dict)
            uut = UutSchema().load(cfg_dict, partial=True)
        except Exception as e:
            logging.error(e)
            return None, None

        logging.debug(f'Parse config file {fname}, uut: {uut}, rack: {rack}')
        return rack, uut

   
    @staticmethod
    def parse_dir(path):
        """ Scan whole directory and return an array of dictionary of the config file.
        """
        path = os.path.join(path, '')
        dir_list = os.listdir(path)
        cfgs = []
        for f in dir_list:
            ext = os.path.splitext(f)[-1].lower()
            if ext == ".txt":
                print(f'Parsing config file {path + f}')
                rack, uut = ResponseConfig().parseConfig(path + f)
                cfgs.append((rack, uut))
        return cfgs
