#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import time
from datetime import timedelta, date
import os
import sys

import atlas_hydro
from sensor_worker import dispatch_sensor_data

hydroData = atlas_hydro.read_sensors()

def format_data():
	if hydroData:
		for sensor in hydroData:

			if sensor["sensor_type"] == "atlas_scientific_ec":
				ec_data = {
					"hydro_ec": str(sensor["ec"]),
					"role": sensor["sensor_type"],
					"sensor_num": sensor["serial_number"],
					"type": "hydro_ec"
				}

				dispatch_sensor_data(ec_data)

				ppm_data = {
					"hydro_ppm": str(sensor["ppm"]),
					"role": sensor["sensor_type"],
					"sensor_num": sensor["serial_number"],
					"type": "hydro_ppm"
				}

				dispatch_sensor_data(ppm_data)

			if sensor["sensor_type"] == "atlas_scientific_temp":
				temp_data = {
					"hydro_temp": str(sensor["sensor_reading"]),
					"role": sensor["sensor_type"],
					"sensor_num": sensor["serial_number"],
					"type": "hydro_temp"
				}

				dispatch_sensor_data(temp_data)

			if sensor["sensor_type"] == "atlas_scientific_ph":
				ph_data = {
					"hydro_ph": str(sensor["sensor_reading"]),
					"role": sensor["sensor_type"],
					"sensor_num": sensor["serial_number"],
					"type": "hydro_ph"
				}

				dispatch_sensor_data(ph_data)


format_data()
