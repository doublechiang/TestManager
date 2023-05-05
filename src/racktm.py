import os
import time
from collections import namedtuple
from watchdog.observers import Observer
import logging


from cfgfldr import CfgFolder
from uut import Uut
from rack import Rack, RackSchema
from resconfig import ResponseConfig

class UUTManager:
    ''' The UUT manager class
        Contain the racks and uuts information
    '''
    def getPrjFolder(self, win_root):
        """ The WIN folder has resonse/config folder to store the config files.
            Parameters: win_root: the root folder of WIN
            return a list of named tuple (prj, folder)
        """
        Project = namedtuple('Project', 'prj folder')
        prjs = []
        for entry in os.listdir(win_root):
            fldr = f'{win_root}/{entry}/response/config'
            if os.path.isdir(fldr):
                prjs.append(Project(entry, fldr))
        return prjs
    
    def start(self, win_root):
        # prjs = self.getPrjFolder('../seeds/WIN')
        prjs = self.getPrjFolder(win_root)
        observer = Observer()
        for p in prjs:
            f = CfgFolder(p.folder)
            f.setNotifier(self.uutNotifier)
            observer.schedule(CfgFolder(p.folder), p.folder, recursive=False)
            cfgs = ResponseConfig.parse_dir(p.folder)
            for pair in cfgs:
                rack, uut = pair
                
                logging.debug(f'rack:{rack}, uut:{uut}')
                rack.updateUut(uut)
                if rack not in self.racks:
                    self.racks.append(rack)
                self.uuts.append(uut)
            
        observer.start()

    def uutNotifier(self, cfg_path):
        """ Callback notifier for uut config file change 
        """
        uut = Uut.parse_file(cfg_path)

    def __parseConfig(self, uut):
        """ UUT manager will parse the config file and create the UUT instance
        """
        logging.debug(f'Parse config file {uut}')
        rack = RackSchema().load(RackSchema().dump(uut))
        print(rack)

    def getRackCollection(self):
        return self.racks


    def getRack(self, racksn):
        """ Get the rack instance by the rack serial number
        """
        for r in self.racks:
            if r.RACKSN == racksn:
                return r
        return {}
    
    def getUutCollection(self):
        print(self.uuts)
        return self.uuts
    
    def getUut(self, sn):
        ''' Get the UUT by SN, idealy any serial number. 
        '''
        for r in self.uuts:
            if r.CHASSISSN == sn:
                return r
        return {}
   
    def __init__(self):
        self.uuts = []
        self.racks = []


if __name__ == '__main__':
    racktm = UUTManager()
    prjs = racktm.get_PrjFldr('seeds/WIN')
    while True:
        time.sleep(1)
