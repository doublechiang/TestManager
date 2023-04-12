import sys
import logging
import os
import csv
from flask_restful import fields, marshal_with

import settings

wip_fileds = {
    'racksn' : fields.String,
    'location' : fields.String,
    'uuts' : fields.List(fields.String)
}

class SfHand:
    SF_HOST='192.168.204.9'
    SF_SHARE='Monitor'
    SF_WIP_LISTING_FN = 'CurrentRackData.csv'
    SF_RACKDEFPATH='NetApp\\SNLIST\\{}'.format(SF_WIP_LISTING_FN)


    def getWip(self):
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
                rack = wip.get(row[1], dict())
                rack['location'] = row[0]
                rack['racksn']  = row[1]
                uuts = rack.get('uuts', [])
                if row[2] not in uuts:
                    uuts.append(row[2])
                rack['uuts'] = uuts
                wip.update({row[1]: rack})

        os.unlink(self.SF_WIP_LISTING_FN)
                
        return wip

    


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