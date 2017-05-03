#!/usr/bin/python
# -*- coding: utf-8 -*-

from socket import gethostname
import json
from datetime import timedelta, date
import os, sys
# add ../sources to the PYTHONPATH
sys.path.append(os.path.join('./sources'))

from yocto_api import *
from yocto_humidity import *
from yocto_temperature import *
from yocto_pressure import *
from yocto_lightsensor import *
from yocto_carbondioxide import *
from yocto_datalogger import *
import datetime

from sensor_worker import dispatch_sensor_data

module = YModule.FirstModule()
while module is not None:
    # print(module.get_serialNumber() + ' (' + module.get_productName() + ')')

    target = module.get_serialNumber()
    moddesc = module.describe()

    if module.get_userVar() == 0:
        print module.get_userVar()

        datalogger = YDataLogger.FindDataLogger(target)

        datalogger.set_timeUTC(datetime.datetime.utcnow())
        datalogger.set_autoStart(YDataLogger.AUTOSTART_ON)
        datalogger.set_recording(YDataLogger.RECORDING_ON)
        module.set_luminosity(0)

        print (module.set_userVar(1))
        print "Saving to flash"

        module.saveToFlash()

    module.set_luminosity(25)

    if "METEO" in moddesc:
        humSensor = YHumidity.FindHumidity(target + '.humidity')
        pressSensor = YPressure.FindPressure(target + '.pressure')
        tempSensor = YTemperature.FindTemperature(target + '.temperature')

    #   print('%2.1f' % tempSensor.get_currentValue() + "°C   " +
    #          "%4.0f" % pressSensor.get_currentValue() + "mb  " +
    #          "%4.0f" % humSensor.get_currentValue() + "% ")

        temp = tempSensor.get_currentValue()
        press = pressSensor.get_currentValue()
        hum = humSensor.get_currentValue()
        sensor_num = target
        hostname = gethostname()
        timestamp = datetime.datetime.now()

        jsonPackage = {
            'sensor_num': sensor_num,
            'hostname': hostname,
            'timestamp': timestamp,
            'temperature': temp,
            'pressure': press,
            'humidity': hum
        }

        dispatch_sensor_data("METEO", jsonPackage)

        es = 0.6108 * exp((2.5e6 / 461) * (1 / 273 - 1 / (273 + temp)))

        vpd = es * (100 - hum) / 100

        print vpd

        vpdPackage = {
            'sensor_num': sensor_num,
            'hostname': hostname,
            'timestamp': timestamp,
            'vpd': vpd
        }

        print jsonPackage
        # mongoize('vpd', vpdPackage)

    if "LIGHT" in moddesc:
        sensor = YLightSensor.FindLightSensor(target + '.lightSensor')

        # print("Light :  "+ str(int(sensor.get_currentValue()))+" lx ")
        # googleize(target,[sensor.get_currentValue()])

        jsonPackage = {
            'sensor_num': target,
            'hostname': gethostname(),
            'timestamp': datetime.datetime.now(),
            'lux': sensor.get_currentValue(),
        }

        print jsonPackage

        dispatch_sensor_data("METEO", jsonPackage)

    if "CO2" in moddesc:
        sensor = YCarbonDioxide.FindCarbonDioxide(target+'.carbonDioxide')

        # print("CO2 :" + str(int(sensor.get_currentValue()))+" ppm")

        jsonPackage = {
            'sensor_num': target,
            'hostname': gethostname(),
            'timestamp': datetime.datetime.now(),
            'co2': sensor.get_currentValue(),
        }

        dispatch_sensor_data("METEO", jsonPackage)

    module.set_luminosity(0)
    module = module.nextModule()
