#!/usr/bin/python

import string
import os
import time
import pylibftdi
from pylibftdi.device import Device
from pylibftdi.driver import FtdiError
from pylibftdi import Driver
from collections import OrderedDict


class AtlasDevice(Device):

    def __init__(self, sn):
        Device.__init__(self, mode='t', device_id=sn)
    #
    # def read_line(self):
    #     """
    #       taken from the ftdi library and modified to
    #       use the ezo line separator "\r"
    #     """
    #     lsl = len('\r')
    #     line_buffer = []
    #     while True:
    #         next_char = self.read(1)
    #         if next_char == '' or (size > 0 and len(line_buffer) > size):
    #             break
    #         line_buffer.append(next_char)
    #         if (len(line_buffer) >= lsl and
    #                 line_buffer[-lsl:] == list('\r')):
    #             break
    #     return ''.join(line_buffer)

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

    def read_lines(self):
        """
        Taken from ftdi lib to work with
        modified readline function
        """
        lines = []
        try:
            while True:
                line = self.read_line()
                if not line:
                    break
                    self.flush_input()
                lines.append(line)
                return lines
        except FtdiError:
            print "Failed to read from the sensor."
            return ''

    def send_cmd(self, cmd):
        """
        Send command to the Atlas Sensor.
        Carriage Return at the end of the command ends statement.
        :param cmd:
        :return:
        """
        buf = cmd + "\r"
        try:
            self.write(buf)
            return True
        except FtdiError:
                print "Failed to send command to the sensor."
                return False


def log_sensor_readings(all_curr_readings):
    for readings in all_curr_readings:

        try:
            while True:
                dev.send_cmd("R")
                lines = dev.read_lines()
                for i in range(len(lines)):
                    # print lines[i]
                    if lines[i][0] != '*':
                        print "Response: ", lines[i]
                time.sleep(delaytime)
        # catches the ctrl-c command, which breaks the loop above
        except KeyboardInterrupt:
            print("Continuous polling stopped")

        else:
            # pass commands straight to board
            if len(input_val) == 0:
                lines = dev.read_lines()
                for i in range(len(lines)):
                    print lines[i]
            else:
                dev.send_cmd(input_val)
                time.sleep(1.3)
                lines = dev.read_lines()
                for i in range(len(lines)):
                    print lines[i]


def read_sensors():
    """ Should read the sensors """

    all_curr_readings = []
    ref_temp = 25

    for key, value in sensors.items():
        # Get the readings from any Atlas Scientific temperature sensors to use as ref_temp
        print " %s " % key
        dev = AtlasDevice(value["serial_number"])
        dev.send_cmd("T," + str(ref_temp))

# Get the readings from any Atlas Scientific Elec Conductivity sensors

        if value["sensor_type"] == "atlas_scientific_ph":
            dev = AtlasDevice(value["serial_number"])
            dev.send_cmd("R")
            sensor_reading = dev.read_line()

            # (round(((float(dev.read_line())) *
                            #   value["ppm_multiplier"]), value["accuracy"]))

# Get the readings from any other Atlas Scientific sensors

        else:
            dev = AtlasDevice(value["serial_number"])
            dev.send_cmd("R")
            sensor_reading = round(float(dev.read_line()),
                                   value["accuracy"])
            all_curr_readings.append([value["name"], sensor_reading])

    log_sensor_readings(all_curr_readings)

    return

sensors = OrderedDict([("atlas_sensor_ph", {"sensor_type": "atlas_scientific_ph", "name": "ph", "is_connected": True, "is_ref": False, "serial_number": 'DJ00RUFM', "accuracy": 2})])
loops = 0

while True:  # Repeat the code indefinitely

    if loops == 300:
        loops = 0

        read_sensors()

        print "%s" % loops

    loops += 1
    # time.sleep(1)
