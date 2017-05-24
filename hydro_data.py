#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import time
from datetime import timedelta, date
import os
import sys

import atlas_hydro
from sensor_worker import dispatch_sensor_data

hydroData = atlas_hydro.read_sensors() # should this be in the loop?

def format_data():
	if hydroData:
		for sensor in hydroData:

			if sensor["sensor_type"] == "atlas_scientific_ec":
				ec_data = {
					"sensor_num": sensor["serial_number"],
					"type": "ec",
					"role": sensor["sensor_type"],
					"ec": str(sensor["ec"]),
					"value": str(sensor["ec"])
				}

				dispatch_sensor_data(ec_data)

				ppm_data = {
					"sensor_num": sensor["serial_number"],
					"role": sensor["sensor_type"],
					"type": "ppm",
					"ppm": str(sensor["ppm"])
					# "value": str(sensor["ppm"])
				}

				dispatch_sensor_data(ppm_data)

			if sensor["sensor_type"] == "atlas_scientific_temp":
				temp_data = {
					"sensor_num": sensor["serial_number"],
					"role": sensor["sensor_type"],
					"type": "hydro_temp",
					"hydroTemp": str(sensor["sensor_reading"])
					# "value": str(sensor["sensor_reading"])
				}

				dispatch_sensor_data(temp_data)

			if sensor["sensor_type"] == "atlas_scientific_ph":
				temp_data = {
					"sensor_num": sensor["serial_number"],
					"role": sensor["sensor_type"],
					"type": "hydro-ph",
					"hydroPh": str(sensor["sensor_reading"])
					# "value": str(sensor["sensor_reading"])
				}

				dispatch_sensor_data(temp_data)


format_data()
