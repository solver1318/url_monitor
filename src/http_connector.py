import requests
from logger import Logger

logger = Logger.__call__().get_logger()

class HTTPConnector:
    HTTP_OK = 200
    HTTP_SERVICE_UNAVAILABLE = 503

    def __init__(self, url):
        """
        Connector to actually access to target url.
        """
        self.url = url

    def access(self):
        '''
        Access to the url and get HTTP status & response time(ms).
        :return: tuple: (HTTP status, response time(ms))
        '''
        logger.debug('GET ' + self.url)
        response = requests.get(self.url)
        return response.status_code, format(response.elapsed.total_seconds() * 1000, '.3f')
