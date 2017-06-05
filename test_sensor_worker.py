#!/usr/bin/env python2.7

from sensor_worker import *
import datetime
import unittest
from unittest import TestCase
# from mock import MagicMock as Mock
from mock import patch
import nose
from nose.tools import *

valid_format = {
	'dataPackage': {
		'sensor_num': 'DJ00RU96',
		'room': 'Grow Room 1',
		'sensor_version': '1.00',
		'timestamp': datetime.datetime(2017, 6, 5, 22, 38, 7, 920763),
		'hostname': 'iunuTestPi',
		'hydro_ppm': '630',
		'net_hostname': 'iunuTestPi',
		'role': 'hydroTest',
		'type': 'hydro_ppm'},
		'customerName': 'Solstice'
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
		'hostname': u'iunuTestPi',
		'hydro_ppm': '630',
		'net_hostname': 'iunuTestPi',
		'role': 'hydroTest',
		'type': 'hydro_ppm'
	}
}


class Test_sensor_worker(unittest.TestCase):

	# @patch('sensor_worker.format_sensor_data', side_effect=return_data_package)
	def test_format_sensor_data(self):
		""" Test Format Sensor Data"""
		result = format_sensor_data(data)

		self.assertEqual(result, valid_format)


if __name__ == '__main__':
	unittest.main()








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


thoth = {
  "lat":"",
  "hostname":"iunuTestPi",
  "role":"hydroTest",
  "room":"Grow Room 1",
  "long":""
}

thoth2 = {
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
}
#
# no_thoth = ''
#
# mock = Mock(side_effect=chain([thoth], cycle([thoth2], cycle([no_thoth])))
