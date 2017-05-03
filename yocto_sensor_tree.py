#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
sys.path.append(os.path.join('./sources'))

from yocto_api import *
from yocto_humidity import *
from yocto_temperature import *
from yocto_pressure import *
from yocto_lightsensor import *
import time

errmsg = YRefParam()


if YAPI.RegisterHub("usb", errmsg) != YAPI.SUCCESS:
    sys.exit("init error" + errmsg.value)

else:
    module = YModule.FirstModule()

    while module is not None:
        print(module.get_serialNumber() + ' (' + module.get_productName() + ')')


        print('TOP LEVEL')

        lightT = YLightSensor.FindLightSensor("LIGHTMK3-853DA.lightSensor")
        humidT = YHumidity.FindHumidity('METEOMK1-7FB03.humidity')
        tempT = YTemperature.FindTemperature('METEOMK1-7FB03.temperature')

        print lightT
        print humidT
        print tempT

        time.sleep(10)

    if lightT.isOnline() and humidT.isOnline() is True:
        i = 1

        for i in range(1, 6):
            print (
                '%2.2f' % tempT.get_currentValue() + "deg F   "
                + "%2.1f" % humidT.get_currentValue() + "%  "
                + str(int(lightT.get_currentValue())/82) + ' PAR'
            )

            i = i + 1
            time.sleep(1)
    else:
        print('No devices found!')
        print('TOP MID LEVEL')

        lightTM = YLightSensor.FindLightSensor('LIGHTMK3-7CCBA.lightSensor')
        humidTM = YHumidity.FindHumidity('METEOMK1-850EF.humidity')
        tempTM = YTemperature.FindTemperature('METEOMK1-850EF.temperature')

    if lightTM.isOnline() and humidTM.isOnline() is True:
        i = 1

        for i in range(1, 6):
            print(
                '%2.2f' % tempTM.get_currentValue() + "deg F   "
                + "%2.1f" % humidTM.get_currentValue() + "%  "
                + str(int(lightTM.get_currentValue())/82) + ' PAR'
            )

            i = i + 1
            time.sleep(1)
    else:
        print('No devices found!')
        print('MID LOW LEVEL')

        lightML = YLightSensor.FindLightSensor('LIGHTMK3-7CAB6.lightSensor')
        humidML = YHumidity.FindHumidity('METEOMK1-85165.humidity')
        tempML = YTemperature.FindTemperature('METEOMK1-85165.temperature')

    if lightML.isOnline() and humidML.isOnline() is True:
        i = 1

        for i in range(1, 6):
            print(
                '%2.2f' % tempML.get_currentValue() + "deg F   "
                + "%2.1f" % humidML.get_currentValue() + "%  "
                + str(int(lightML.get_currentValue()) / 82) + ' PAR'
            )

            i = i + 1
            time.sleep(1)

    else:
        print('No devices found!')
        print('LOW LEVEL')

        lightL = YLightSensor.FindLightSensor('LIGHTMK3-85205.lightSensor')
        humidL = YHumidity.FindHumidity('METEOMK1-7FA23.humidity')
        tempL = YTemperature.FindTemperature('METEOMK1-7FA23.temperature')

    if lightL.isOnline() and humidL.isOnline() is True:
            print(
                '%2.2f' % tempL.get_currentValue() + "deg F   "
                + "%2.1f" % humidL.get_currentValue() + "%  "
                + str(int(lightL.get_currentValue()) / 82) + ' PAR'
            )
    else:
        print('No devices found!')
        print('TEST COMPLETE')


    time.sleep(10)
