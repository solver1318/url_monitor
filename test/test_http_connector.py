import unittest
from base import TestBase
from constants import Constants
from http_connector import HTTPConnector

class TestHttpConnector(unittest.TestCase, TestBase):

    def setUp(self):
        self.config = self.getConfig()
        self.connectors = []
        for url in self.config.getTargets():
            self.connectors.append(HTTPConnector(url % Constants.MOCK_SERVER_PORT))
        self.startMockServer()

    def testAccessToMockserver(self):
        for connector in self.connectors:
            expectedStatus = int(connector.url.split('/')[-1])
            status, elapsedTime = connector.access()
            self.assertTrue(status == expectedStatus)
            self.assertTrue(Constants.MIN_SLEEP * 1000 <= float(elapsedTime) <= Constants.MAX_SLEEP * 1000)

    def tearDown(self):
        self.stopMockServer()
