#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
from datetime import timedelta, date
import os, sys
# add ../sources to the PYTHONPATH
sys.path.append(os.path.join("./sources"))
import atlas_hydro

hydroData = atlas_hydro.read_sensors()


def format_data():
    hydrojson = []

    if hydroData is not None:
        for sensor in hydroData:
            if sensor["sensor_type"] == "atlas_scientific_ec":
                hydrojson.append({
                    "sensor_num": sensor["serial_number"],
                    "type": "ec"
                    "role": sensor["sensor_type"],
                    "ec": sensor["ec"],
                })

                hydrojson.append({
                    "sensor_num": sensor["serial_number"],
                    "role": sensor["sensor_type"],
                    "type": "ppm"
                    "ppm": sensor["ppm"]
                })

            if sensor["sensor_type"] == "atlas_scientific_temp":
                hydrojson.append({
                    "sensor_num": sensor["serial_number"],
                    "role": sensor["sensor_type"],
                    "type": "hydro-temp",
                    "hydro-temp": sensor["sensor_reading"]
                })

            if sensor["sensor_type"] == "atlas_scientific_ph":
                hydrojson.append({
                    "sensor_num": sensor["serial_number"],
                    "role": sensor["sensor_type"],
                    "type": "hydro-ph",
                    "hydro-ph": sensor["sensor_reading"]
                })
    print hydrojson
    return hydrojson


format_data()
