from unittest import SkipTest
from infi import unittest
from infi.eventlog import c_api, facade

class FacadeTestCase(unittest.TestCase):
	def test_open_system(self):
		eventlog = facade.LocalEventLog()
		with eventlog.open_channel_context("System"):
			pass
