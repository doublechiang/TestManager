import os
import time
from collections import namedtuple
from watchdog.observers import Observer
import logging


from cfgfldr import CfgFolder
from uut import Uut
from rack import Rack, RackSchema

class UUTManager:
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
    
    def start(self):
        prjs = self.getPrjFolder('../seeds/WIN')
        observer = Observer()
        for p in prjs:
            f = CfgFolder(p.folder)
            f.setNotifier(self.uutNotifier)
            observer.schedule(CfgFolder(p.folder), p.folder, recursive=False)
            uuts = Uut.parse_dir(p.folder)
            self.uuts.extend(uuts)
        observer.start()
        for u in self.uuts:
            self.__parseConfig(u)

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

    
    def __init__(self):
        self.uuts = []
        self.racks = []


if __name__ == '__main__':
    racktm = UUTManager()
    prjs = racktm.get_PrjFldr('seeds/WIN')
    while True:
        time.sleep(1)
