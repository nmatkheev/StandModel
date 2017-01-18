import os
import datetime


DEBUG = False

if not DEBUG:
    BASE_DIR = "/logs"
else:
    BASE_DIR = ""
log_suffix = datetime.datetime.now().strftime("%H_%M")


def get_logconf(port):
    return {
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
                'filename': os.path.join(BASE_DIR, 'back{}_{}_info.log'.format(port, log_suffix)),
                'formatter': 'simple',
                'filters': ['cutter']
            },
            'restofall': {
                'level': 'DEBUG',
                'class': 'logging.FileHandler',
                'filename': os.path.join(BASE_DIR, 'back{}_{}_rubb.log'.format(port, log_suffix)),
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