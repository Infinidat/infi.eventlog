from unittest import SkipTest
from infi import unittest
from infi.eventlog import c_api, facade

class FacadeTestCase(unittest.TestCase):
	def test__open_system_channel(self):
		eventlog = facade.LocalEventLog()
		with eventlog.open_channel_context("System"):
			pass

	def test__get_available_channels(self):
		eventlog = facade.LocalEventLog()
		channels = list(eventlog.get_available_channels())
		self.assertIn("System", channels)