import string
import pylibftdi
from pylibftdi.device import Device
from pylibftdi.driver import FtdiError
from pylibftdi import Driver
import os
import time
import sys
import time
from collections import OrderedDict

# sleep(10)

class AtlasDevice(Device):


    def __init__(self, sn):
        Device.__init__(self, mode='t', device_id=sn)

    def read_line(self, size=0):
        """
        taken from the ftdi library and modified to
        use the ezo line separator "\r"
        """
        lsl = len('\r')
        line_buffer = []
        while True:
            # read bytes until Carriage Return is received.
            next_char = self.read(1)
            if next_char == '' or (size > 0 and len(line_buffer) > size):
                break
            line_buffer.append(next_char)
            if (len(line_buffer) >= lsl and
                    line_buffer[-lsl:] == list('\r')):
                break
        return ''.join(line_buffer)

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


# def get_ftdi_device_list():
#     """
#     return a list of lines, each a colon-separated
#     vendor:product:serial summary of detected devices
#     """
#     dev_list = []
#
#     for device in Driver().list_devices():
#         # list_devices returns bytes rather than strings
#         dev_info = map(lambda x: x.decode('latin1'), device)
#         # device must always be this triple
#         vendor, product, serial = dev_info
#         dev_list.append(serial)
#     return dev_list


def log_sensor_readings(all_curr_readings):

    # Create a timestamp and store all readings on the MySQL database

    conn, curs = open_database_connection()

    curs.execute("INSERT INTO sensors (timestamp) VALUES(now());")
    curs.execute("SELECT MAX(timestamp) FROM sensors")
    last_timestamp = curs.fetchone()
    last_timestamp = last_timestamp[0].strftime('%Y-%m-%d %H:%M:%S')

    for readings in all_curr_readings:
        try:
            curs.execute(("UPDATE sensors SET {} = {} WHERE timestamp = '{}'")
                        .format(readings[0], readings[1], last_timestamp))
        except:
            pass

    close_database_connection(conn, curs)

    return


def read_sensors():

    all_curr_readings = []
    ref_temp = 25

    # Get the readings from any 1-Wire temperature sensors

    for key, value in sensors.items():
        if value["is_connected"] is True:
            if value["sensor_type"] == "atlas_scientific_temp":
                sensor_reading = (round(float(dev.read_line()),
                                value["accuracy"])
                all_curr_readings.append([value["name"], sensor_reading])
                if value["is_ref"] is True:
                    ref_temp=sensor_reading

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


sensors = OrderedDict([("atlas_sensor_1", {  # Atlas Scientific Temp Sensor
                            "sensor_type": "atlas_scientific_temp",
                            "name": "atlas_temp",
                            "is_connected": True,
                            "is_ref": True,
                            "serial_number": 'DJ00RROZR',  # Enter Serial Number
                            "accuracy": 1}),

                       ("atlas_sensor_2", {  # FLOW
                            "sensor_type": "atlas_scientific_flo",
                            "name": "ph",
                            "is_connected": True,
                            "is_ref": False,
                            "serial_number": '',  # Enter Serial Number
                            "accuracy": 2}),

                       ("atlas_sensor_3", {  # pH/ORP Atlas Scientific Sensor
                            "sensor_type": "atlas_scientific_ph",
                            "name": "orp",
                            "is_connected": True,
                            "is_ref": False,
                            "serial_number": 'DJ00R0V8',  # Enter Serial Number
                            "accuracy": 0}),

                       ("atlas_sensor_4", {  # Atlas Scientific EC Sensor
                            "sensor_type": "atlas_scientific_ec",
                            "name": "ec",
                            "is_connected": True,
                            "is_ref": False,
                            "serial_number": 1,  # Enter Serial Number
                            "accuracy": 0,
                            "ppm_multiplier": 0.67})])  # Convert EC to PPM

loops = 0

while True:  # Repeat the code indefinitely

    if loops == 300:
        loops = 0

        read_sensors()

    loops += 1
    # time.sleep(1)
