#!/usr/bin/python
# -*- coding: utf-8 -*-
import nose
import unittest
from sensor_worker2 import dispatch_sensor_data
from nose.tools import assert_equal
from nose.tools import assert_not_equal
from nose.tools import assert_raises
from nose.tools import raises


class DispatchSensorDataTest(unittest.TestCase):
	"""Tests for dispatch_sensor_data"""

	def dispatch_sensor_data_test(self):
		"""It should format the JSON appropriately"""
		json_string = {  "ppm":"618", "sensor_group":"Test", "role":"hydroTest", "type":"ppm", "ppm":"618" }
		# "sensor_num":"DJ00RU96",
		valid_json = "{'sensordata': {'sensor_num': 'DJ00RU96', 'room': u'Grow Room 1', 'sensor_version': u'1.00', 'timestamp': datetime.datetime(2017, 5, 29, 20, 23, 53, 238618), 'hostname': u'iunuTestPi', 'ppm': '618', 'sensor_group': u'Test', 'role': u'hydroTest', 'type': 'ppm'}}"
		result = dispatch_sensor_data(json_string)

		nose.tools.ok_(result, 201)

result = nose.main()
