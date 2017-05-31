#!/usr/bin/python
# -*- coding: utf-8 -*-
from sensor_worker2 import dispatch_sensor_data
import nose
from nose.tools import *
import unittest


class DispatchSensorDataTest(unittest.TestCase):
	"""Tests for dispatch_sensor_data"""

	def dispatch_sensor_data_test(self):
		"""It should format the JSON appropriately"""
		json_string = {  "ppm":"618", "sensor_group":"Test", "role":"hydroTest", "type":"ppm", "ppm":"618" }
		valid_json = "{'sensor_num':'DJ00RU96', sensordata': {'sensor_num': 'DJ00RU96', 'room': u'Grow Room 1', 'sensor_version': u'1.00', 'timestamp': datetime.datetime(2017, 5, 29, 20, 23, 53, 238618), 'hostname': u'iunuTestPi', 'ppm': '618', 'sensor_group': u'Test', 'role': u'hydroTest', 'type': 'ppm'}}"
		result = dispatch_sensor_data(json_string)
		nose.tools.ok_(result, valid_json)

result = nose.main()
