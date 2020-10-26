import json
import unittest
from base import TestBase
from constants import Constants


class TestConfig(unittest.TestCase, TestBase):

    def setUp(self):
        self.config = self.getConfig()

    def test_getTargets(self):
        '''
        Check if the number of target URLs from Config object is correct.
        :return:
        '''
        with open(Constants.CONFIG_JSON) as json_file:
            data = json.load(json_file)
        self.assertEqual(len(data['TARGETS']), len(self.config.getTargets()),
                         'Wrong # of targets')
        for index, url in enumerate(self.config.getTargets()):
            self.assertEqual(data['TARGETS'][index], url, 'Wrong url %s vs %s' % (data['TARGETS'][index], url))
