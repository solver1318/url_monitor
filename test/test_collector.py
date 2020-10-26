import unittest
from prometheus_client import CollectorRegistry, generate_latest
from base import TestBase
from constants import Constants
from collector import Collector
from http_connector import HTTPConnector

class TestCollector(unittest.TestCase, TestBase):
    def setUp(self):
        '''
        Initialize connector objects which will access target URLs and start a mock server.
        :return:
        '''
        self.config = self.getConfig()
        self.connectors = []
        for url in self.config.getTargets():
            self.connectors.append(HTTPConnector(url % Constants.MOCK_SERVER_PORT))
        self.startMockServer()

    def test_collectSuccessfully(self):
        '''
        Access successful REST APIs via Collector and check if the number of results is correct.
        :return:
        '''
        res = []
        for connector in self.connectors:
            registry = CollectorRegistry()
            Collector(registry, connector).do()
            res.append(generate_latest(registry))
        self.assertTrue(len(res) == len(self.connectors))

    def test_collectFromWrongURL(self):
        '''
        Access wrong REST API and check if Exception raises up.
        :return:
        '''
        wrongURL = '404'
        wrongURLConnector = HTTPConnector('http://localhost:%s/%s' % (Constants.MOCK_SERVER_PORT, wrongURL))
        registry = CollectorRegistry()
        try:
            Collector(registry, wrongURLConnector).do()
            self.assertTrue(False, 'Should not be passed here because this test case tries to access to wrong URL')
        except Exception as e:
            self.assertTrue(wrongURL in str(e))

    def tearDown(self):
        '''
        Kill the mock server.
        :return:
        '''
        self.stopMockServer()
