COMMENT_INDICATOR = '#'

def retouch(response):
    '''
    Remove # HELP XXXX and # TYPE XXXX lines to only include prometheus output lines.
    :param response: utf-8 encoded prometheus format
    :return: str: retouched lines
    '''
    output = [line + '\n' for line in response.decode().splitlines() if not line.startswith(COMMENT_INDICATOR)]
    return ''.join(output).encode('utf-8')

import logging

class SingletonType(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonType, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class Logger(object, metaclass=SingletonType):
    """
    Singleton logger.
    """
    _logger = None

    def __init__(self):
        self._logger = logging.getLogger("urlMon")
        self._logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s \t [%(levelname)s | %(filename)s:%(lineno)s] > %(message)s')
        streamHandler = logging.StreamHandler()
        streamHandler.setFormatter(formatter)
        self._logger.addHandler(streamHandler)

    def get_logger(self):
        return self._logger