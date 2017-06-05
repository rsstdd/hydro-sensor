#!/usr/bin/env python2.7

from sensor_worker import *
import datetime
import unittest
from unittest import TestCase
from mock import MagicMock as Mock
from mock import patch

input_json = {
	"ppm": "618",
	"sensor_group": "Test",
	"role": "hydroTest",
	"type": "ppm",
	"ppm": "618"
}

data = {
	'open_thoth': {
		"customer": {
			"customerName": "Solstice",
			"facility": "solstice"
		},
		"location": {
			"room": "Grow Room 1",
			"position": "{ x: '', y: ''}",
			"coord": {
			  "lat": "",
			  "long": ""
			}
		},
		"device": {
			"hostname": "iunuTestPi",
			"sensorGroup": "Test",
			"sensorVersion": "1.00",
			"camtype": "",
			"lenstype": "",
			"role": "hydroTest",
			"rotation": "",
			"mount": ""
		}
	},
	'deviceData': {
		'sensor_num': 'DJ00RU96',
		'room': 'Grow Room 1',
		'sensor_version': '1.00',
		'timestamp': datetime.datetime(2017, 6, 5, 21, 11, 13, 36125),
		'hostname': u'iunuTestPi', 'hydro_ppm': '630',
		'net_hostname': 'iunuTestPi', 'role': u'hydroTest',
		'type': 'hydro_ppm'
	}
}

# def return_data_package():
# 	deviceData = {
# 		'open_thoth': {
# 			"customer": {
# 				"customerName": "Solstice",
# 				"facility": "solstice"
# 			},
# 			"location": {
# 				"room": "Grow Room 1",
# 				"position": "{ x: '', y: ''}",
# 				"coord": {
# 				  "lat": "",
# 				  "long": ""
# 				}
# 			},
# 			"device": {
# 				"hostname": "iunuTestPi",
# 				"sensorGroup": "Test",
# 				"sensorVersion": "1.00",
# 				"camtype": "",
# 				"lenstype": "",
# 				"role": "hydroTest",
# 				"rotation": "",
# 				"mount": ""
# 			}
# 		},
# 		'deviceData': {
# 			'sensor_num': 'DJ00RU96',
# 			'room': u'Grow Room 1',
# 			'sensor_version': '1.00',
# 			'timestamp': datetime.datetime(2017, 6, 5, 21, 11, 13, 36125),
# 			'hostname': u'iunuTestPi', 'hydro_ppm': '630',
# 			'net_hostname': 'iunuTestPi', 'role': u'hydroTest',
# 			'type': 'hydro_ppm'
# 			}
# 		}
# 	return deviceData

class Test_sensor_worker(TestCase):

	@patch('sensor_worker.format_sensor_data', side_effect=return_data_package)
	def test_format_sensor_data(self, format_sensor_data):
		""" Test Format Sensor Data"""
		print 'format_sensor_data', format_sensor_data
		assert format_sensor_data(deviceData) === ''

if __name__ == '__main__':
	unittest.main()
