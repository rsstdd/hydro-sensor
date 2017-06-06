#!/usr/bin/env python2.7

try:
	import mock
except ImportError:
	from unittest import mock

import datetime
import unittest
from unittest import TestCase
# from mock import mock
from mock import patch
import nose
from nose.tools import *
from sensor_worker import *

thoth = {
  "lat":"",
  "hostname":"iunuTestPi",
  "role":"hydroTest",
  "room":"Grow Room 1",
  "long":""
}


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
	"open_thoth": {
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
	"deviceData": {
		"sensor_num": "DJ00RU96",
		"room": "Grow Room 1",
		"sensor_version": "1.00",
		"timestamp": str(datetime.datetime.utcnow()),
		"hostname": "iunuTestPi",
		"hydro_ppm": "630",
		"net_hostname": "iunuTestPi",
		"role": "hydroTest",
		"type": "hydro_ppm"
	}
}

class Test_Sensor_Worker(unittest.TestCase):

	@patch('sensor_worker')
	def test_format_sensor_data(thoth):
			thoth_mock.return_value = thoth

			assert format_sensor_data(data) == valid_format

	# # mock = MagicMock(side_effect=[])
	# @patch('sensor_worker.open_thoth')
	# # @patch('open_thoth2_id')
	#
	# 	""" Test Format Sensor Data"""
	# 	print format_sensor_data(data)
	#


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
