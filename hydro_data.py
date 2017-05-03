#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
from datetime import timedelta, date
import os, sys
# add ../sources to the PYTHONPATH
sys.path.append(os.path.join("./sources"))
from sensor_worker import dispatch_sensor_data
import atlas_hydro

hydroData = atlas_hydro.read_sensors()


def format_data():
    hydrojson = []

    if hydroData is not None:
        for sensor in hydroData:
            if sensor["sensor_type"] == "atlas_scientific_ec":
                # hydrojson.append({
                    # "sensor_num": sensor["serial_number"],
                    # "type": "ec",
                    # "role": sensor["sensor_type"],
                    # "ec": sensor["ec"],
                # })
                ec_data = {
                    "sensor_num": sensor["serial_number"],
                    "type": "ec",
                    "role": sensor["sensor_type"],
                    "ec": sensor["ec"],
                }

                dispatch_sensor_data('HYDRO_EC', ec_data)

                # hydrojson.append({
                #     "sensor_num": sensor["serial_number"],
                #     "role": sensor["sensor_type"],
                #     "type": "ppm",
                #     "ppm": sensor["ppm"]
                # })

                ppm_data = {
                    "sensor_num": sensor["serial_number"],
                    "role": sensor["sensor_type"],
                    "type": "ppm",
                    "ppm": sensor["ppm"]
                }

                dispatch_sensor_data('HYDRO_PPM', ec_data)


            if sensor["sensor_type"] == "atlas_scientific_temp":
                # hydrojson.append({
                #     "sensor_num": sensor["serial_number"],
                #     "role": sensor["sensor_type"],
                #     "type": "hydro-temp",
                #     "hydro-temp": sensor["sensor_reading"]
                # })

                temp_data = {
                    "sensor_num": sensor["serial_number"],
                    "role": sensor["sensor_type"],
                    "type": "hydro-temp",
                    "hydro-temp": sensor["sensor_reading"]
                }

                dispatch_sensor_data('HYDRO_TEMP', temp_data)

            if sensor["sensor_type"] == "atlas_scientific_ph":
                # hydrojson.append({
                #     "sensor_num": sensor["serial_number"],
                #     "role": sensor["sensor_type"],
                #     "type": "hydro-ph",
                #     "hydro-ph": sensor["sensor_reading"]
                # })

                temp_data = {
                    "sensor_num": sensor["serial_number"],
                    "role": sensor["sensor_type"],
                    "type": "hydro-ph",
                    "hydro-ph": sensor["sensor_reading"]
                }

                dispatch_sensor_data('HYDRO_TEMP', temp_data)

format_data()
