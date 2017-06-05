#!/usr/bin/env python2.7

from sensor_worker import dispatch_sensor_data
import datetime
import unittest
from unittest import TestCase
from mock import MagicMock as Mock
from mock import patch

class TestDispatchSensorData(TestCase):

	@patch('sensor_worker.dispatch_sensor_data')
	def test_dispatch_sensor_data(self, MockResponse):
		res = MockResponse()

		res.dispatch_sensor_data.return_value = [
			{
				'sensor_num':'DJ00RU96',
				'sensordata': {
					'sensor_num': 'DJ00RU96',
					'room': 'Grow Room 1',
					'sensor_version': '1.00',
					'timestamp': datetime.datetime(2017, 5, 29, 20, 23, 53, 238618),
					'hostname': 'iunuTestPi',
					'ppm': '618',
					'sensor_group': 'Test',
					'role': 'hydroTest',
					'type': 'ppm'
				}
			}
		]

		input_json = {
			"ppm": "618",
			"sensor_group": "Test",
			"role": "hydroTest",
			"type": "ppm",
			"ppm": "618"
		}

		dispatch_sensor_data(input_json)

		assert result == valid_json

		print result
