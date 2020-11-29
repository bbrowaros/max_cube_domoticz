# max_cube_domoticz
Eq-3 max cube integration with domoticz via python

## Purpose

This script is a effect of a rewrtite integration based on following scripts: 
https://www.domoticz.com/wiki/EQ3_MAX!

The original script stopped working for me first in domoticz directly, after a while changes implemented in lua language caused that this script stopped working compleatly. 
This caused that I've rewrite the script logic based on following integration: 
https://github.com/hackercowboy/python-maxcube-api

this integration was written to work with Home Assistant but using this library and logic from original EQ3_MAX I was able to maintain the operation of my EQ-3 MAX integration with domoticz. This is a temporary solution and I'm working on creating a plugin to Domoticz. Don't know if this will be created. For now I'm publishing this script to help anyone who has problems with EQ3_MAX and Domoticz integration based on LUA. 

**Note: this script was tested only on Linux and is only integrating a Thermostat as I've got only this devices in my setup**

## Prereq: 

EQ-3 Max cube needs to be connected to your network and thermostat paired. There is no logic for a room division but we are relaying on naming convention (like in original script created in lua for domoticz). When you pair devices with cube please name them with:<br />
- `<name of device>-Stat`<br />

On Domoticz instance please create a 3 virtual devices per one `<name of device>-Stat` device in EQ-3 Max cube. <br />

- `<name of device>-Stat` - type of device: General Percentage, this will store the current open valve value <br />
- `<name of device>-Rad`  - type of device: Thermostat SetPoint, this will store and update the target temperature <br />
- `<name of device>-Sens` - type of device: Temp, this is to get the read actual temperature from thermostat <br />

**Note the `<name of device>` need to match between EQ-3 Max and Domoticz (including spaces etc). Please avoid using a special characters or local characters to allow smooth working as this script was fast written and is not design to detect and compensate on that.**

For more detailed description on how to setup EQ-3 MAX and Domoticz please read:  <br />
https://www.domoticz.com/wiki/EQ3_MAX!#Installing_EQ3_MAX.21_Devices

## Install instructions: 

To operate you need to install: <br />
https://github.com/hackercowboy/python-maxcube-api <br />

please use: 
``` pip install maxcube-api ```

clone this git repository: 
``` git clone 
  cd max_cube_domoticz
  ```

Please make sure that the path to python is correct on top of the scripts:
``` #which python ``` in both scripts. 
To test the communication please edit script: ``` max_test.py ``` and add a IP of Max cube: <br />
``` cube = MaxCube(MaxCubeConnection('192.168.XXX.XXX', 62910)) ``` <br />

Change permissions of the script to execute: <br />
``` chmod +x ./max_test.py ``` <br />

Then to test it you can execute: <br />
``` ./max_test.py ``` <br />

If all goes good you will receive: <br />
```Room: Salon
Device: Salon-Stat
Room: Dzieci
Device: Ewa pokoj-Stat
Room: Sypialnia
Device: Sypialnia-Stat

Type:   MAX_THERMOSTAT
RF:     19AB4F
Room ID:1
Room:   Salon
Name:   Salon-Stat
Serial: OEQ1419266
MaxSetP:30.5
MinSetP:4.5
Mode:   MANUAL
Actual: 25.6
Target: 23.0
Valve pos: 10

Type:   MAX_THERMOSTAT
RF:     19AB4D
Room ID:2
Room:   Dzieci
Name:   Ewa pokoj-Stat
Serial: OEQ1419268
MaxSetP:30.5
MinSetP:4.5
Mode:   MANUAL
Actual: 25.1
Target: 23.0
Valve pos: 11

Type:   MAX_THERMOSTAT
RF:     199A5C
Room ID:3
Room:   Sypialnia
Name:   Sypialnia-Stat
Serial: OEQ1417525
MaxSetP:30.5
MinSetP:4.5
Mode:   MANUAL
Actual: None
Target: 16.0
Valve pos: 0
```
If all is ok then we can proceed to actual script. <br />
**Note: at this step you need to have all devices in Domoticz setup so plase read the Prereq section**

Modify script ```max_run.py``` and add: 
IP and Port of Domoticz: 
```DOMOTICZ_IP='192.168.XXX.XXX'
DOMOTICZ_PORT='8080'

IP_CUBE='192.168.X.XXX'
PORT_CUBE=62910
```
once this is done add execution permissions to script ```#chmod +x ./max_run.py``` and execute it: ```./max_run.py```. If all goes well you should see something like that: 
```$ ./max_run.py
 ####################################
 Starting at: 2020-11-29 16:38:30.162087
Salon-Stat has a idx 6492
Ewa pokoj-Stat has a idx 6493
Sypialnia-Stat has a idx 6721
Salon-Rad has a idx 6491
Ewa pokoj-Rad has a idx 6494
Sypialnia-Rad has a idx 6720
Updating Termostat: Salon-StatRead valve open: 9 Read temperature: 25.6
 Comparing D:23.0 to T:23.0. Domoticz device was updated : 5741s ago
Updating Termostat: Ewa pokoj-StatRead valve open: 14 Read temperature: 25.0
 Comparing D:23.0 to T:23.0. Domoticz device was updated : 5742s ago
Updating Termostat: Sypialnia-StatRead valve open: 0 Read temperature: None
 Comparing D:16.0 to T:16.0. Domoticz device was updated : 5742s ago
```

Script will autodetect the idx numbers of devices used in domoticz and perform checks. 

## Make it constant running 

I'm using a crontab to run this script every 1m
