import logging
import logging.config

# TODO: Implement file-based logging
ENVY_LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'file': {
            'format': '[%(asctime)s][%(levelname)s] %(name)s %(filename)s:%(funcName)s:%(lineno)d | %(message)s',
            'datefmt': '%H:%M:%S',
        }
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'file',
            'stream': 'ext://sys.stderr',
        }
    },
    'loggers': {
        'envy': {
            'handlers': ['file'],
            # TODO: Allow DEBUG level once file-based logging
            # is implemented
            'level': 'CRITICAL',
        }
    }
}

logging.config.dictConfig(ENVY_LOGGING)
LOG = logging.getLogger('envy')


def debug(msg, **kwargs):
    LOG.debug(msg % kwargs)


def info(msg, **kwargs):
    LOG.info(msg % kwargs)


def warning(msg, **kwargs):
    LOG.info(msg % kwargs)


def error(msg, **kwargs):
    LOG.info(msg % kwargs)


def set_level(new_level):
    LOG.setLevel(new_level)
