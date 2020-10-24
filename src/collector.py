from prometheus_client import Gauge
from http_connector import HTTPConnector

from logger import Logger

logger = Logger.__call__().get_logger()

AVAILABILITY = {
    HTTPConnector.HTTP_OK: 1,
    HTTPConnector.HTTP_SERVICE_UNAVAILABLE: 0
}

class Collector:
    """
    Collect availability and response time from connector.
    Register prometheus formatted metrics into registry.
    """

    __PREFIX = 'sample_external_url_'

    def __init__(self, registry, connector):
        self.__registry = registry
        self.__connector = connector

    def do(self):
        '''
        Call connector's access and receive HTTP status & response time(ms).
        Put 2 Gauges objets, availability _up and response time _response_ms into registry.
        :return: None
        '''
        status, elapsedTime = self.__connector.access()
        if not status in AVAILABILITY:
            raise Exception('Unknown HTTP status(%d) is received' % status)

        logger.debug('HTTP Status (%s) and elapsedTime (%s ms) ' % (status, elapsedTime))

        avaiability = Gauge(
            self.__PREFIX + '_up',
            'Availability, UP or DOWN',
            ['url'], registry=self.__registry
        )            
        avaiability.labels(self.__connector.url).set(AVAILABILITY[status])
        responseMiliSec = Gauge(
            self.__PREFIX + '_response_ms',
            'Elapsed Time(MS)',
            ['url'], registry=self.__registry
        )            
        responseMiliSec.labels(self.__connector.url).set(elapsedTime)
        logger.debug('Collecting done')
