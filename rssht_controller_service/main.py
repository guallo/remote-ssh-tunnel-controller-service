import os
import sys
import pid
import argparse
import daemon
import logging

from . import config
os.chdir(config.SERVICE_WORKING_DIRECTORY)
sys.path.extend(config.SERVICE_PATH)

from . import util
util.import_configd()

from .service import Service


logger = logging.getLogger(__name__)


def main():
    logging.basicConfig(
        filename=config.LOGGING_FILENAME, 
        filemode=config.LOGGING_FILEMODE, 
        format=config.LOGGING_FORMAT, 
        level=config.LOGGING_LEVEL)
    
    logger.debug('Parsing command line arguments.')
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--daemonize', action='store_true')
    args = parser.parse_args()
    
    s = Service()
    util.import_addons()
    
    if args.daemonize:
        filenos = [logging.getLogger().handlers[0].stream.fileno()]
        pidfile = pid.PidFile(
            pidname=os.path.basename(config.PID_FILENAME), 
            piddir=os.path.dirname(config.PID_FILENAME), 
            enforce_dotpid_postfix=False, 
            register_term_signal_handler=False)
        
        logger.debug('Entering daemon context.')
        
        with daemon.DaemonContext(files_preserve=filenos, 
                            working_directory=config.SERVICE_WORKING_DIRECTORY, 
                            pidfile=pidfile, detach_process=True):
            s.run()
    else:
        s.run()
    
    Service.instance = None
