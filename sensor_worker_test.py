#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, sys
import unittest
# sys.path.append(os.path.join("..", "test")
from sensor_worker2 import dispatch_sensor_data
from jsonTest import json_string

from socket import gethostname
import datetime
import json
import requests
from pymongo import MongoClient


class DispatchSensorDataTest(unittest.TestCase):
	"""Tests for dispatch_sensor_data"""

	def dispatch_sensor_data_test(self):
		"""It should format the JSON appropriately"""
		json_string = { "sensor_num":"DJ00RU96", "ppm":"618", "sensor_group":"Test", "role":"hydroTest", "type":"ppm", "ppm":"618" }
		valid_json = "{'sensordata': {'sensor_num': 'DJ00RU96', 'room': u'Grow Room 1', 'sensor_version': u'1.00', 'timestamp': datetime.datetime(2017, 5, 29, 20, 23, 53, 238618), 'hostname': u'iunuTestPi', 'ppm': '618', 'sensor_group': u'Test', 'role': u'hydroTest', 'type': 'ppm'}}"

		result = dispatch_sensor_data(json_string)

		print valid_post

		self.assertEqual(valid_post, valid_json)


if __name__ == '__main__':
	unittest.main()
