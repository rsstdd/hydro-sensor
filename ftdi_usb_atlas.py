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

    def read_lines(self):
        """
        also taken from ftdi lib to work with modified readline function
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
        Before sending, add Carriage Return at the end of the command.
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

def check_for_only_one_reference_temperature():
    """
    Check that only one Primary Temperature sensor is defined
    """
    ref_check = 0

    for key, value in sensors.items():
        if (value["is_connected"]) is True:
            if value["sensor_type"] == "atlas_scientific_rtd":
                if value["is_ref"] is True:
                    ref_check += 1
    if ref_check > 1:
        os.system('clear')
        print ("\n\n                     !!!! WARNING !!!!\n\n"
        "You can only have one Primary Temperature sensor, Please set the\n"
        "Temperature sensor that is in the liquid you are testing to True\n"
        "and the other to False\n\n                     !!!! WARNING !!!!\n\n")
        sys.exit()
    return

def log_sensor_readings(all_curr_readings):

    # Create a timestamp and store all readings on the MySQL database

    last_timestamp = curs.fetchone()
    last_timestamp = last_timestamp[0].strftime('%Y-%m-%d %H:%M:%S')

    for readings in all_curr_readings:
        while True:
            input_val = raw_input("Enter command: ")

            # continuous polling command automatically polls the board
            if input_val.upper().startswith("POLL"):
                delaytime = float(string.split(input_val, ',')[1])

                dev.send_cmd("C,0") # turn off continuous mode
                #clear all previous data
                time.sleep(1)
                dev.flush()

                print("Polling sensors every %0.2f seconds, press ctrl-c to stop polling" % delaytime)

                try:
                    while True:
                        dev.send_cmd("R")
                        lines = dev.read_lines()
                        for i in range(len(lines)):
                            # print lines[i]
                            if lines[i][0] != '*':
                                print "Response: " , lines[i]
                        time.sleep(delaytime)

                except KeyboardInterrupt: # catches the ctrl-c command, which breaks the loop above
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

    all_curr_readings = []
    ref_temp = 25

    # Get the readings from any 1-Wire temperature sensors

    for key, value in sensors.items():
        if value["is_connected"] is True:
            if value["sensor_type"] == "atlas_scientific_rtd":
                sensor_reading = (round(float(read_1_wire_temp(key)),
                                 value["accuracy"]))
                all_curr_readings.append([value["name"], sensor_reading])
                if value["is_ref"] is True:
                    ref_temp = sensor_reading

    # Get the readings from any Atlas Scientific temperature sensors

            elif value["sensor_type"] == "atlas_scientific_temp":
                dev = AtlasDevice(value["serial_number"])
                dev.send_cmd("R")
                sensor_reading = round(float(dev.read_line()),
                                value["accuracy"])
                all_curr_readings.append([value["name"], sensor_reading])
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
                    sensor_reading = (round(((float(dev.read_line())) *
                                  value["ppm_multiplier"]), value["accuracy"]))

    # Get the readings from any other Atlas Scientific sensors

                else:
                    dev = AtlasDevice(value["serial_number"])
                    dev.send_cmd("R")
                    sensor_reading = round(float(dev.read_line()),
                                    value["accuracy"])
                    all_curr_readings.append([value["name"], sensor_reading])

    log_sensor_readings(all_curr_readings)

    return

sensors = OrderedDict([("atlas_sensor_rtd", {  # Atlas Scientific RTD Temp Sensor
                            "sensor_type": "atlas_scientific_rtd",
                            "name": "atlas_temp",
                            "is_connected": True,
                            "is_ref": True,
                            "serial_number": 1,  # Enter Serial Number
                            "accuracy": 1}),

                       ("atlas_sensor_ph", {  # pH/ORP Atlas Scientific Sensor
                            "sensor_type": "atlas_scientific_ph",
                            "name": "ph",
                            "is_connected": True,
                            "is_ref": False,
                            "serial_number": 1,  # Enter Serial Number
                            "accuracy": 2}) #,
                    ])

                    #    ("atlas_sensor_ec", {  # Atlas Scientific EC Sensor
                    #         "sensor_type": "atlas_scientific_ec",
                    #         "name": "ec",
                    #         "is_connected": True,
                    #         "is_ref": False,
                    #         "serial_number": 1,  # Enter Serial Number
                    #         "accuracy": 0,
                    #         "ppm_multiplier": 0.67})]),  # Convert EC to PPM
                    #
                    #    ("atlas_sensor_flow", {  # Atlas Scientific FLOW
                    #         "sensor_type": "atlas_scientific_flow",
                    #         "name": "flow",
                    #         "is_connected": True,
                    #         "is_ref": False,
                    #         "serial_number": 1,  # Enter Serial Number
                    #         "accuracy": 0,
                    #         "ppm_multiplier": 0.67}
                    # ])

check_for_only_one_reference_temperature()

loops = 0  # Set starting loops count for timing relay and sensor readings

while True:  # Repeat the code indefinitely

    if loops == 300:
        loops = 0

        read_sensors()

    loops += 1
    time.sleep(1) # not sure if we need this
