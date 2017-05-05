# Hydro Sensor #

## Start
1. Configure Atlas Scientific FTDI (Below)
2. `sudo python hydro_data.py`

## About

Hydro Sensor module utilizes Atlas Scientific Temperature (DJ00RVZR), pH (DJ00RUV8), and EC (DJ00RU96) sensors.

* `hydro_data.py` calls `sensor_lib/atlas_hydro.py` and formats the data returned from that function
* `util/sensor_worker.py` adds metadata from the thoth.id and ships JSON to the API

---

## Configure Atlas Scientific FTDI
### Installing dependencies for FTDI adaptors ###

* Install libftdi package.

        sudo apt-get install libftdi-dev

* Install pylibftdi python package.

        sudo pip install pylibftdi

* Create SYMLINK of the FTDI adaptors.
    **NOTE:** If you are using device with root permission, just skip this step.

    The following will allow ordinary users (e.g. ‘pi’ on the RPi) to access to the FTDI device without needing root permissions:

    Create udev rule file by typing `sudo nano /etc/udev/rules.d/99-libftdi.rules` and insert below:

        SUBSYSTEMS=="usb", ATTRS{idVendor}=="0403", ATTRS{idProduct}=="6015", GROUP="dialout", MODE="0660", SYMLINK+="FTDISerial_Converter_$attr{serial}"

    Press CTRL+X, Y and hit Enter to save & exit.

    Restart `udev` service to apply changes above.

        sudo service udev restart


* Modify FTDI python driver

    Since our FTDI devices use other USB PID(0x6015), we need to tweak the original FTDI Driver.

        sudo nano /usr/local/lib/python2.7/dist-packages/pylibftdi/driver.py

    Move down to the line 70 and add `0x6015` at the end of line.

    Original line:

        USB_PID_LIST = [0x6001, 0x6010, 0x6011, 0x6014]

    Added line:

        USB_PID_LIST = [0x6001, 0x6010, 0x6011, 0x6014, 0x6015]        
