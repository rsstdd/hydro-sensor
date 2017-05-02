#!/usr/bin/env python

import time
from collections import OrderedDict
from pylibftdi.device import Device
from pylibftdi.driver import FtdiError
from sets import Set

class AtlasDevice(Device):

    def read_line(self):
        """
        Read the response from the Atlas Sensor
        :return:
        """
        line_buffer = []
        try:
            start_time = time.time()
            while True:
                # read bytes until Carriage Return is received.
                next_char = self.read(1)    # read one byte
                if next_char == "\r":  # response of sensor always ends with CR.
                    break
                line_buffer.append(next_char)
                if time.time() - start_time > 1.0:  # timeout
                    line_buffer = ''
                    break
            return ''.join(line_buffer)

        except FtdiError:
            return ''

    def send_cmd(self, cmd):
        """
        Send command to the Atlas Sensor.
        Before sending, add Carriage Return at the end of the command.
        :param cmd:
        :return:
        """
        buf = cmd + "\r"  # add carriage return
        try:
            self.write(buf)
            return True
        except FtdiError:
            print ("Failed to send command to the sensor.")
            return False


def log_sensor_readings(all_curr_readings):

    for reading in all_curr_readings:
        try:
            print reading
            print '---------'
        except:
            pass

    return


def read_sensors():

    all_curr_readings = []
    ref_temp = 25

    for key, value in sensors.items():
        if value["is_connected"] is True:

    # Get the readings from any Atlas Scientific temperature sensors

            if value["sensor_type"] == "atlas_scientific_temp":
                dev = AtlasDevice(value["serial_number"])
                dev.send_cmd("R")
                sensor_reading=dev.read_line()
                all_curr_readings.append({'name': value["name"], 'serial_number': value["serial_number"], 'sensor_type': value["sensor_type"], 'sensor_reading': sensor_reading})
                if value["is_ref"] is True:
                    ref_temp = sensor_reading

            else:
                dev = AtlasDevice(value["serial_number"])
                # Set reference temperature value on the sensor
                dev.send_cmd("T," + str(ref_temp))

    # Get the readings from any Atlas Scientific Elec Conductivity sensors

                if value["sensor_type"] == "atlas_scientific_ec":
                    dev = AtlasDevice(value["serial_number"])
                    dev.send_cmd("R")
                    sensor_reading=dev.read_line()
                    atlas_scientific_ec = Set([value["name"], value["serial_number"], value["sensor_type"], sensor_reading])
                    all_curr_readings.append({'name': value["name"], 'serial_number': value["serial_number"], 'sensor_type': value["sensor_type"], 'sensor_reading': sensor_reading})

                if value["sensor_type"] == "atlas_scientific_ph":
                    dev = AtlasDevice(value["serial_number"])
                    dev.send_cmd("R")
                    sensor_reading=dev.read_line()
                    atlas_scientific_ph = Set([value["name"], value["serial_number"], value["sensor_type"], sensor_reading])
                    all_curr_readings.append({'name': value["name"], 'serial_number': value["serial_number"], 'sensor_type': value["sensor_type"], 'sensor_reading': sensor_reading})


                if value["sensor_type"] == "atlas_scientific_flo":
                    dev = AtlasDevice(value["serial_number"])
                    dev.send_cmd("R")
                    sensor_reading=dev.read_line()
                    atlas_scientific_ph = Set([value["name"], value["serial_number"], value["sensor_type"], sensor_reading])
                    all_curr_readings.append({'name': value["name"], 'serial_number': value["serial_number"], 'sensor_type': value["sensor_type"], 'sensor_reading': sensor_reading})


    log_sensor_readings(all_curr_readings)

    return all_curr_readings


sensors = OrderedDict([("atlas_sensor_1", {  # Atlas Scientific Temp Sensor
                            "sensor_type": "atlas_scientific_temp",
                            "name": "temp",
                            "is_connected": True,
                            "is_ref": True,
                            "serial_number": 'DJ00RVZR',  # Enter Serial Number
                            "accuracy": 1}),

                       ("atlas_sensor_2", {  # FLOW
                            "sensor_type": "atlas_scientific_flo",
                            "name": "flow",
                            "is_connected": False,
                            "is_ref": False,
                            "serial_number": 'DJ00RB93',  # Enter Serial Number
                            "accuracy": 2}),

                       ("atlas_sensor_3", {  # pH Atlas Scientific Sensor
                            "sensor_type": "atlas_scientific_ph",
                            "name": "ph",
                            "is_connected": True,
                            "is_ref": False,
                            "serial_number": 'DJ00RUV8',  # Enter Serial Number
                            "accuracy": 0}),

                       ("atlas_sensor_4", {  # Atlas Scientific EC Sensor
                            "sensor_type": "atlas_scientific_ec",
                            "name": "ec",
                            "is_connected": True,
                            "is_ref": False,
                            "serial_number": 'DJ00RU96',  # Enter Serial Number
                            "accuracy": 0,
                            "ppm_multiplier": 0.67})])  # Convert EC to PPM

loops = 0

while True:  # Repeat the code indefinitely

    if loops == 300:
        loops = 0

        read_sensors()

    loops += 1
