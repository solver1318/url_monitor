import unittest
from base import TestBase
from utils import retouch, Logger

class TestUtils(unittest.TestCase, TestBase):

    def test_getLogger(self):
        self.assertIsNotNone(Logger.__call__().get_logger())

    def test_retouch(self):
        naiveOutput = ''.join([
            '# HELP sample_external_url__up Availability, UP or DOWN\n',
            '# TYPE sample_external_url__up gauge\n',
            'sample_external_url__up{url="https://httpstat.us/503"} 0.0\n',
            '# HELP sample_external_url__response_ms Elapsed Time(MS)\n',
            '# TYPE sample_external_url__response_ms gauge\n',
            'sample_external_url__response_ms{url="https://httpstat.us/503"} 132.487\n'
        ]).encode('utf-8')
        retouched = retouch(naiveOutput)
        # retouched should not have comments
        self.assertTrue(not '# HELP' in retouched.decode())
        self.assertTrue(not '# TYPE' in retouched.decode())
