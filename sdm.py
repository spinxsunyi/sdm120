#!/usr/bin/python

import minimalmodbus
import json
import paho.mqtt.publish as publish
import os
import time 
from time import sleep
from datetime import datetime
import sys
import urllib2

rs485 = minimalmodbus.Instrument('/dev/ttyUSB0', 1)
rs485.serial.baudrate = 9600
rs485.serial.bytesize = 8
rs485.serial.parity = minimalmodbus.serial.PARITY_NONE
rs485.serial.stopbits = 1
rs485.serial.timeout = 1
rs485.debug = False
rs485.mode = minimalmodbus.MODE_RTU
print rs485

# Enter Your API key here
myAPI = 'GCCOV8FWLO2WKP0U' 
# URL where we will send the data, Don't change it
baseURL = 'https://api.thingspeak.com/update?api_key=%s' % myAPI 

file = open("/home/pi/data2.csv", "a")
i=0
if os.stat("/home/pi/data2.csv").st_size == 0:
        file.write("Time, Volts, Current, Active_Power, Apparent_Power, Reactive_Power, Power_Factor, Phase_Angle, Frequency, Import_Active_Energy, Export_Active_Energy, Import_Reactive_Energy, Export_Reactive_Energy, Total_Active_Energy, Total_Reactive_Energy\n")

now = datetime.now()
file.write("{} program start\n").format(now)
print("{} program start\n").format(now)

while True:
    now = datetime.now()
    try:
        Volts = rs485.read_float(0, functioncode=4, number_of_registers=2)
        Current = rs485.read_float(6, functioncode=4, number_of_registers=2)
        Active_Power = rs485.read_float(12, functioncode=4, number_of_registers=2)
        Apparent_Power = rs485.read_float(18, functioncode=4, number_of_registers=2)
        Reactive_Power = rs485.read_float(24, functioncode=4, number_of_registers=2)
        Power_Factor = rs485.read_float(30, functioncode=4, number_of_registers=2)
        Phase_Angle = rs485.read_float(36, functioncode=4, number_of_registers=2)
        Frequency = rs485.read_float(70, functioncode=4, number_of_registers=2)
        Import_Active_Energy = rs485.read_float(72, functioncode=4, number_of_registers=2) 
        Export_Active_Energy = rs485.read_float(74, functioncode=4, number_of_registers=2)
        Import_Reactive_Energy = rs485.read_float(76, functioncode=4, number_of_registers=2)
        Export_Reactive_Energy = rs485.read_float(78, functioncode=4, number_of_registers=2)
        Total_Active_Energy = rs485.read_float(342, functioncode=4, number_of_registers=2)
        Total_Reactive_Energy = rs485.read_float(344, functioncode=4, number_of_registers=2)
        data = '{}, {:.3f}, {:.3f}, {:.3f}, {:.3f}, {:.3f}, {:.3f}, {:.3f}, {:.3f}, {:.3f}, {:.3f}, {:.3f}, {:.3f}, {:.3f}, {:.3f}{}'.format(
            now,Volts,Current,Active_Power,Apparent_Power,
            Reactive_Power,Power_Factor,Phase_Angle,Frequency,Import_Active_Energy,
            Export_Active_Energy,Import_Reactive_Energy,Export_Reactive_Energy,Total_Active_Energy,Total_Reactive_Energy
            ,chr(10))
    except NoResponseError:
        data = '{}, no response error'.format(now)
    else:
        data ='{}, unknown error'.format(now)
    
    print(data)
    
    # file.write(now + "," + Volts + "," + Current + "," +  Active_Power + "," + Apparent_Power + "," + Reactive_Power + "," + Power_Factor + "," + Phase_Angle + "," + Frequency + "," + Import_Active_Energy + "," +Export_Active_Energy + "," + Import_Reactive_Energy + "," + Export_Reactive_Energy + "," + Total_Active_Energy + "," + Total_Reactive_Energy + "\n")
    # print(now + "," + Volts + "," + Current + "," +  Active_Power + "," + Apparent_Power + "," + Reactive_Power + "," + Power_Factor + "," + Phase_Angle + "," + Frequency + "," + Import_Active_Energy + "," +Export_Active_Energy + "," + Import_Reactive_Energy + "," + Export_Reactive_Energy + "," + Total_Active_Energy + "," + Total_Reactive_Energy + "\n")
    file.write(data)
    file.flush()
    # file.close()

    # print 'Time: {0:.1f} '.format(time.time())
    # print 'Voltage: {0:.1f} Volts'.format(Volts)
    # print 'Current: {0:.1f} Amps'.format(Current)
    # print 'Active power: {0:.1f} Watts'.format(Active_Power)
    #print 'Apparent power: {0:.1f} VoltAmps'.format(Apparent_Power)
    #print 'Reactive power: {0:.1f} VAr'.format(Reactive_Power)
    #print 'Power factor: {0:.1f}'.format(Power_Factor)
    #print 'Phase angle: {0:.1f} Degree'.format(Phase_Angle)
    #print 'Frequency: {0:.1f} Hz'.format(Frequency)
    #print 'Import active energy: {0:.3f} Kwh'.format(Import_Active_Energy)
    #print 'Export active energy: {0:.3f} kwh'.format(Export_Active_Energy)
    #print 'Import reactive energy: {0:.3f} kvarh'.format(Import_Reactive_Energy)
    #print 'Export reactive energy: {0:.3f} kvarh'.format(Export_Reactive_Energy)
    # print 'Total active energy: {0:.3f} kwh'.format(Total_Active_Energy)
    # print 'Total reactive energy: {0:.3f} kvarh'.format(Total_Reactive_Energy)
    #print 'Current Yield (V*A): {0:.1f} Watt'.format(Volts * Current)
    time.sleep(10)

    