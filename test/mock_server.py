import requests
import random
import time

from http.server import BaseHTTPRequestHandler
from constants import Constants

class MockServerRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        '''
        Mock REST APIs and only supports GET /200 or /503.
        GET /200 always return HTTP OK
        GET /503 always return HTTP SERVICE_UNAVAILABLE
        :return:
        '''
        # Sleep randomly between 1 and 3 secs
        time.sleep(random.randrange(Constants.MIN_SLEEP, Constants.MAX_SLEEP))
        if self.path == '/200':
            self.send_response(requests.codes.ok)
        elif self.path == '/503':
            self.send_response(requests.codes.service_unavailable)
        else:
            self.send_response(requests.codes.not_found)
        self.end_headers()
        return
