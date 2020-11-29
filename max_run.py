#!/usr/bin/python


####################
#
# Base module created by Pumba
# EQ3 Max for Domoticz
# currently only a THERMOSTAT integration
#
#####################

import urllib, json

#required for interacting with Maxcube
from maxcube.cube import MaxCube
from maxcube.connection import MaxCubeConnection 
from maxcube.device import MAX_THERMOSTAT, MAX_THERMOSTAT_PLUS, MAX_DEVICE_MODE_AUTOMATIC, MAX_DEVICE_MODE_MANUAL, MAX_DEVICE_MODE_VACATION, MAX_DEVICE_MODE_BOOST

import logging


from datetime import datetime

interval = 5

DOMOTICZ_IP='192.168.XXX.XXX'
DOMOTICZ_PORT='8080'

IP_CUBE='192.168.X.XXX'
PORT_CUBE=62910

print (' ####################################')
print (' Starting at: '+ str(datetime.today()))
#connecting to domoticz and gathering all idx for 

#searching for -Stat and -Rad 
url= "http://"+DOMOTICZ_IP+":"+DOMOTICZ_PORT+"/json.htm?type=devices&filter=utility&used=true&order=Name"

response = urllib.urlopen(url)

data = json.loads(response.read())


domoticz_props = {}

for i in  data['result']:
	if i['Name'][-5:] == "-Stat":
		print (i['Name'] + " has a idx " + i['idx'])
                domoticz_props[i['Name']]=[i['idx'],i['LastUpdate'],i['Data']]
	elif i['Name'][-4:] == "-Rad":
		print (i['Name'] + " has a idx " + i['idx'])
		domoticz_props[i['Name']]=[i['idx'],i['LastUpdate'],i['Data']]

#searching for -Sens
url= "http://"+DOMOTICZ_IP+":"+DOMOTICZ_PORT+"/json.htm?type=devices&filter=temp&used=true&order=Name"

response = urllib.urlopen(url)

data = json.loads(response.read())


for i in  data['result']:
        if i['Name'][-5:] == "-Sens":
                #print (i['Name'] + " has a idx " + i['idx'] + " last updated " + i['LastUpdate'])
		domoticz_props[i['Name']]=[i['idx'],i['LastUpdate'],i['Data']]
	

cube = MaxCube(MaxCubeConnection(IP_CUBE, PORT_CUBE))


for device in cube.devices:
	if device.type != MAX_THERMOSTAT:
		print("Not a thermostat ommiting this device")
	else:
		print("Updating Termostat: " + device.name + 'Read valve open: ' + str(device.valve_position) + ' Read temperature: ' + str(device.actual_temperature))
                #updating domoticz with the read value
                search_name=device.name[0:-5].encode('ascii','ignore')
       		url = "http://"+DOMOTICZ_IP+":"+DOMOTICZ_PORT+"/json.htm?type=command&param=udevice&idx=" + domoticz_props[search_name +'-Rad'][0] + "&nvalue=0&svalue=" + str(device.valve_position)
		response = urllib.urlopen(url)
		if str(device.actual_temperature) != "None":
                	url = "http://"+DOMOTICZ_IP+":"+DOMOTICZ_PORT+"/json.htm?type=command&param=udevice&idx=" + domoticz_props[search_name +'-Sens'][0] + "&nvalue=0&svalue=" + str(device.actual_temperature)
                	response = urllib.urlopen(url)
                #parsing time 
		date=domoticz_props[device.name.encode('ascii','ignore')][1]
		#print date
                y=date[0:4]
		m=date[5:7]
		d=date[8:10]
		h=date[11:13]
		mm=date[14:16]
		s=date[17:]
		date_conv=datetime(int(y),int(m),int(d),int(h),int(mm),int(s),0)
		age=datetime.today()-date_conv
                print (' Comparing D:' + str(domoticz_props[search_name + '-Stat'][2]) + ' to T:' + str(device.target_temperature) + '. Domoticz device was updated : ' + str(int(age.total_seconds())) + 's ago')
		if float(domoticz_props[search_name + '-Stat'][2]) != float(device.target_temperature):
                	if int(age.total_seconds()) > interval * 60:
				#updating domoticz device
                                print ('Updating domoticz device: ' + search_name + '-Stat, sending value: ' + str(device.target_temperature))
				url = "http://"+DOMOTICZ_IP+":"+DOMOTICZ_PORT+"/json.htm?type=command&param=udevice&idx=" + domoticz_props[search_name +'-Stat'][0] + "&nvalue=0&svalue=" + str(device.target_temperature)
				response = urllib.urlopen(url)
			else:
				#updating termostat
				print ('Updating termostat: '+ device.name + ' with value: ' + domoticz_props[search_name + '-Stat'][2])
				cube.set_target_temperature(device,float(domoticz_props[search_name + '-Stat'][2]))
		
