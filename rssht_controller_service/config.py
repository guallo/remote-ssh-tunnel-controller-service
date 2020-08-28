import os
import logging

# Absolute path to avoid misbehavior due to os.chdir
_SERVICE_HOME = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

# Absolute path as required by daemon.DaemonContext
SERVICE_WORKING_DIRECTORY = _SERVICE_HOME

LIB_DIRECTORY = os.path.join(_SERVICE_HOME, 'lib')

SERVICE_PATH = [
    LIB_DIRECTORY,
]

CONFIGD_PACKAGE_DIRECTORY = os.path.join(_SERVICE_HOME, 'configd')
ADDONS_PACKAGE_DIRECTORY = os.path.join(_SERVICE_HOME, 'addons')

PID_FILENAME = os.path.join(SERVICE_WORKING_DIRECTORY, 'rssht-controller-service.pid')

LOGGING_FILENAME = os.path.join(SERVICE_WORKING_DIRECTORY, 'rssht-controller-service.log')
LOGGING_FILEMODE = 'a'
LOGGING_FORMAT = '%(asctime)s %(name)s %(levelname)s %(message)s'
LOGGING_LEVEL = logging.WARN

# In seconds
TIMEOUT = 60

# In seconds
CHECK_INTERVAL = 60

# Should be >= 1
MAX_THREADS = 2
