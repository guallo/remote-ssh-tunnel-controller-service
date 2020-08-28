import os

from rssht_controller_service import config

# In seconds
config.CONNECTION_DOWN_THRESHOLD = 25

config.AGENT_CLIENT_MAP = {
    'The Agent ID': {
        # True or False. If True, does not make changes in FusionPBX.
        'simulate': False,
        'base_url': 'https://localhost',
        'username': 'username',
        'password': 'password',
        'domain': 'the.client.domain',
        'call_flow': '__FAILOVER__',
        # In seconds. A negative value (e.g. -1) means switch immediately (i.e. do not wait)
        'switch-threshold': 10 * 60,
        # In seconds. A negative value (e.g. -1) means switch back immediately (i.e. do not wait)
        'switch-back-threshold': 10 * 60,
    },
}

config.GECKODRIVER_BIN = os.path.join(config._SERVICE_HOME, 'geckodriver')
config.GECKODRIVER_LOG_FILENAME = os.path.join(config.SERVICE_WORKING_DIRECTORY, 'geckodriver.log')
config.GECKODRIVER_LOG_LEVEL = 'warn'
config.FIREFOX_BIN = '/usr/bin/firefox'
config.BROWSER_HEADLESS = True
config.WEBDRIVER_TIMEOUT = 10
