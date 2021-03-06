import os
import datetime

DEBUG = False

# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = "/logs" if not DEBUG else ""
log_suffix = datetime.datetime.now().strftime("%H%M")


LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'simple': {
            'format': '%(levelname)s,%(asctime)s,%(message)s',
            'datefmt': '%d/%m/%Y %H:%M:%S'
        },
    },
    'filters': {
        'cutter': {
            '()': 'LogFilters.log_filters.DelegateFilter',
        },
        'not_cutter': {
            '()': 'LogFilters.log_filters.RestOfFilter',
        },
    },
    'handlers': {
        'mydata': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'front_{0}_info.log'.format(log_suffix)),
            'formatter': 'simple',
            'filters': ['cutter']
        },
        'restofall': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'front_{0}_rubb.log'.format(log_suffix)),
            'formatter': 'simple',
            'filters': ['not_cutter']
        },
    },
    'loggers': {
        'aiohttp': {
            'handlers': ['restofall'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'my_logs': {
            'handlers': ['mydata'],
            'level': 'INFO'
        },
    },
}
