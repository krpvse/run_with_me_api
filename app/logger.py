import json
import logging.config
import logging.handlers


logger = logging.getLogger('app')


def setup_logging():
    with open('logger_config.json', 'r') as file:
        config = json.load(file)
    logging.config.dictConfig(config)
    logger.debug('Logger is initialized')
