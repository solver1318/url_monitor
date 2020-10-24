import sys
from prometheus_client import CollectorRegistry, generate_latest
from wsgiref.simple_server import make_server
from wsgiref.util import setup_testing_defaults
from collector import Collector
from http_connector import HTTPConnector
from config import Config
from logger import Logger

CONFIG_PATH_ENV = 'CONFIG_PATH'
COMMENT_INDICATOR = '#'

logger = Logger.__call__().get_logger()

def urlMonitoring(environ, response):
    '''
    WSGI-based URL monitoring web service.
    NOTE: Only /metrics path supported
    :param environ: system env variables
    :param response: response binder
    :return: list: [utf-8 encoded prometheus metrics]
    '''
    setup_testing_defaults(environ)
    if environ['PATH_INFO'] == '/metrics':
        logger.info('Start collecting metrics')
        res = []
        if CONFIG_PATH_ENV in environ:
            config = Config(environ[CONFIG_PATH_ENV])
            for url in config.getTargets():
                registry = CollectorRegistry()
                connector = HTTPConnector(url)
                try:
                    Collector(registry, connector).do()
                except Exception as e:
                    logger.error('Exception happened: ' + str(e))
                    status = '500 Internal Server Error'
                    response(status, [('Content-Type', 'text/plain')])
                    return []
                res.append(generate_latest(registry))

        status = '200 OK'
        headers = [('Content-type', 'text/plain; charset=utf-8')]
        logger.debug('Successfully collected ' + str(res))
        response(status, headers)
        return res
    else:
        response('404 Not Found', [('Content-Type', 'text/plain')])
        return [b'Not found']

if __name__ == '__main__':
    port = sys.argv[1]
    with make_server('', int(port), urlMonitoring) as httpd:
        logger.info("Serving on port %s..." % port)
        httpd.serve_forever()
