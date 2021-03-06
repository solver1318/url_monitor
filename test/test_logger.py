import unittest
from base import TestBase
from logger import Logger

class TestUtils(unittest.TestCase, TestBase):

    def test_getLogger(self):
        '''
        Check if singleton Logger is initialized.
        :return:
        '''
        self.assertIsNotNone(Logger.__call__().get_logger())
