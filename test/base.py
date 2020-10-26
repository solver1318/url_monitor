
from constants import Constants
from mock_server import MockServerRequestHandler
from http.server import HTTPServer
from threading import Thread
from config import Config

class TestBase:

    def getConfig(self):
        '''
        Return Config object which can be shared by all test cases.
        :return: Config
        '''
        return Config(Constants.CONFIG_JSON)

    def startMockServer(self):
        '''
        Start a mock REST API server.
        :return:
        '''
        self.mockServer = HTTPServer(('localhost', Constants.MOCK_SERVER_PORT),
                                      MockServerRequestHandler)
        self.mockServerThread = Thread(target=self.mockServer.serve_forever)
        self.mockServerThread.setDaemon(True)
        self.mockServerThread.start()

    def stopMockServer(self):
        '''
        Stop the mock server.
        :return:
        '''
        self.mockServer.shutdown()
