#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import time
from datetime import timedelta, date
import os
import sys

import atlas_hydro
from sensor_worker2 import dispatch_sensor_data

hydroData = atlas_hydro.read_sensors() # should this be in the loop?

def format_data():
	if hydroData:
		for sensor in hydroData:

			if sensor["sensor_type"] == "atlas_scientific_ec":
				ec_data = {
					"ec": str(sensor["ec"]),
					"role": sensor["sensor_type"],
					"sensor_num": sensor["serial_number"],
					"type": "ec"
				}

				dispatch_sensor_data(ec_data)

				ppm_data = {
					"ppm": str(sensor["ppm"]),
					"role": sensor["sensor_type"],
					"sensor_num": sensor["serial_number"],
					"type": "ppm"
				}

				dispatch_sensor_data(ppm_data)

			if sensor["sensor_type"] == "atlas_scientific_temp":
				temp_data = {
					"hydroTemp": str(sensor["sensor_reading"]),
					"role": sensor["sensor_type"],
					"sensor_num": sensor["serial_number"],
					"type": "hydroTemp"
				}

				dispatch_sensor_data(temp_data)

			if sensor["sensor_type"] == "atlas_scientific_ph":
				ph_data = {
					"hydroPh": str(sensor["sensor_reading"]),
					"role": sensor["sensor_type"],
					"sensor_num": sensor["serial_number"],
					"type": "hydroPh"
				}

				dispatch_sensor_data(ph_data)


format_data()
