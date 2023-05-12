''' Configuration folder class
'''
from watchdog.events import LoggingEventHandler, FileSystemEventHandler, FileModifiedEvent, FileCreatedEvent
import logging


from uut import Uut

class CfgFolder(FileSystemEventHandler):
    ''' Folder  processing Quanta configuration files 
    '''
    def on_modified(self, event):
        # logging.debug(f'on_modify:{event}')
        logging.info(f'on_modify:{event}')
#        print(f'on_modify:{event}' )
        if isinstance(event, FileModifiedEvent):
            if self.notifier is not None:
                self.notifier(event.src_path)
        return

    def on_created(self, event):
        logging.debug(f'on_created:{event}')
 #       print(f'on_created:{event}')
        if isinstance(event, FileCreatedEvent):
            if self.notifier is not None:
                self.notifier(event.src_path)
        return
    
    def setNotifier(self, notifier):
        self.notifier = notifier
        return
    
    # def _update_uut(self, uut):
    #     if uut is not None:
    #         self.chassis_key.update({uut.chassissn: uut})
    #         self.rack_key.update({uut.racksn: uut})
    #         self.mlb_key.update({uut.mlbsn: uut})
    #         self.csn_key.update({uut.csn: uut})
    #     return
    
    # def scan(self):
    #     uuts = Uut.parse_dir(self.path)
    #     return uuts
    
    
    def __init__(self, path):
        self.path = path
        self.notifier = None 

        # instances = Uut.parse_dir(path)
        # self.rack_key = dict()
        # self.mlb_key= dict()
        # self.chassis_key = dict()
        # self.csn_key = dict()
        # for u in instances:
        #     self._update_uut(u)

