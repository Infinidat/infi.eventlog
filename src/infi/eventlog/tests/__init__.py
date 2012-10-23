from unittest import SkipTest
from infi import unittest
from infi.eventlog import c_api, facade

class FacadeTestCase(unittest.TestCase):
	def test_open_system(self):
		eventlog = facade.EventLog("System")
		with eventlog.open_context():
			pass

