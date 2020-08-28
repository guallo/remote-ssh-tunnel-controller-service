import enum
import time
import signal
import logging
import datetime
import traceback
import concurrent.futures

from asingleton import singleton
from pydispatch import dispatcher

from rssht_controller_lib import factories

from . import util
from . import config


logger = logging.getLogger(__name__)


@singleton
class Service:
    class Signal(enum.Enum):
        CHECK_AGENT = enum.auto()
    
    def run(self):
        logger.debug('Starting service.')
        self.register_signal_handlers()
        
        while True:
            logger.debug('Connecting to SSH server.')
            try:
                rssht_ctl = util.timeout(config.TIMEOUT, factories.RSSHTControllerFactory.new)
            except Exception as exception:
                logger.error(traceback.format_exc())
            else:
                logger.debug('Fetching from SSH server.')
                try:
                    util.timeout(config.TIMEOUT, rssht_ctl.update)
                except Exception as exception:
                    logger.error(traceback.format_exc())
                else:
                    agents = rssht_ctl.get_agents()
                    self.check_agents(agents)
                
                rssht_ctl.dispose()
                rssht_ctl.get_da().get_sshc().close()
                del rssht_ctl
            
            logger.debug('Going to sleep.')
            time.sleep(config.CHECK_INTERVAL)
    
    def register_signal_handlers(self):
        logger.debug('Registering signal handlers.')
        
        def exit_handler(signum, frame):
            logger.debug('Exiting service because of signal %d.', signum)
            exit()
        
        signal.signal(signal.SIGINT, exit_handler)
        signal.signal(signal.SIGQUIT, exit_handler)
        signal.signal(signal.SIGTERM, exit_handler)
    
    def check_agents(self, agents):
        now = datetime.datetime.now(datetime.timezone.utc)
        futures = []
        
        with concurrent.futures.ThreadPoolExecutor(config.MAX_THREADS) as executor:
            for agent in agents:
                future = executor.submit(self.send_check_agent_signal, agent, now)
                futures.append(future)
            
        for future in futures:
            try:
                future.result()
            except Exception as exception:
                logger.error(traceback.format_exc())
    
    def send_check_agent_signal(self, agent, now):
        dispatcher.send(signal=Service.Signal.CHECK_AGENT, sender=self, 
                        agent=agent, now=now)
