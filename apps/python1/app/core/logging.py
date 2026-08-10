import logging.config

LOGGING_CONFIG={
    'version':1,
    'disable_existing_loggers':False,
    'formatters':{
        'default':{
            "datefmt": "%Y-%m-%d %H:%M:%S",
            "format": "%(levelname)-8s | %(asctime)s | %(name)s:%(funcName)s:%(lineno)d | %(message)s"
        }
    },
    "handlers":{
        "console":{
            "class":"logging.StreamHandler",
            "formatter":"default",
            "stream": "ext://sys.stdout"
        }
    },
    "root":{
        "handlers":["console"],
        "level":"INFO"
    }
}

def setup_logging()->None:
    logging.config.dictConfig(LOGGING_CONFIG)
