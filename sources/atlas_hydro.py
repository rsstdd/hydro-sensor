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
                next_char = self.read(1)  # read one byte
                if next_char == "\r":  # sensor always ends with CR.
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


def read_sensors():

    readings = []
    ref_temp = 25

    for key, value in sensors.items():
        if value["is_connected"] is True:

            if value["sensor_type"] == "atlas_scientific_temp":
                # instantiate atlas scientific temp device
                dev = AtlasDevice(value["serial_number"])
                dev.send_cmd("R")
                sensor_reading = dev.read_line()
                report_temp = round(float(sensor_reading),
                            value["accuracy"])
                readings.append(
                    {
                        'type': value["type"],
                        'serial_number': value["serial_number"],
                        'sensor_type': value["sensor_type"],
                        'sensor_reading': report_temp
                    })

                if value["is_ref"] is True:
                    ref_temp = sensor_reading  # calibration temp for pH

            else:
                # Set reference temperature value on the sensor
                dev.send_cmd("T," + str(ref_temp))

    # Get the readings from any Atlas Scientific Elec Conductivity sensors

                if value["sensor_type"] == "atlas_scientific_ec":
                    # instantiate atlas scientific EC device

                    dev = AtlasDevice(value["serial_number"])
                    dev.send_cmd("R")
                    sensor_reading = dev.read_line()
                    # calculate ppm ~ .67 * reading

                    ppmNum = (round((float(sensor_reading.split(',')[0])
                        * value["ppm_multiplier"]), value["accuracy"]))
                    ppmStr = str(ppmNum)
                    readings.append(
                        {
                            'type': value["type"],
                            'serial_number': value["serial_number"],
                            'sensor_type': value["sensor_type"],
                            'ec': sensor_reading,
                            'ppm': ppmStr
                        })

                if value["sensor_type"] == "atlas_scientific_ph":
                    # instantiate atlas scientific EC device

                    dev = AtlasDevice(value["serial_number"])
                    dev.send_cmd("R")
                    sensor_reading = round(float(dev.read_line()),
                                value["accuracy"])
                    readings.append(
                        {
                            'type': value["type"],
                            'serial_number': value["serial_number"],
                            'sensor_type': value["sensor_type"],
                            'sensor_reading': sensor_reading
                        })

    return readings


sensors = [{
        # TEMP Atlas Scientific Sensor (also reference temp)
            "sensor_type": "atlas_scientific_temp",
            "type": "hydro-temp",
            "is_connected": True,
            "is_ref": True,
            "serial_number": 'DJ00RVZR',
            "accuracy": 2
        }, {
         # pH Atlas Scientific Sensor
            "sensor_type": "atlas_scientific_ph",
            "type": "hydro-ph",
            "is_connected": True,
            "is_ref": False,
            "serial_number": 'DJ00RUV8',
            "accuracy": 3
        }, {
          # Atlas Scientific EC Sensor
            "sensor_type": "atlas_scientific_ec",
            "type": "ec",
            "is_connected": True,
            "is_ref": False,
            "serial_number": 'DJ00RU96',
            "accuracy": 0,
            "ppm_multiplier": 0.67  # Convert EC to PPM
        }]


def get_sensor_data():
    read_sensors()
