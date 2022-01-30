import pyvisa
import time 
import os
import nidaqmx
import csv
import serial

class ElectronicLoad(object):
    def __init__(self, identity = ''):
        self.rm = pyvisa.ResourceManager()
        self.device_list = self.rm.list_resources()
        print('Dispositivos conectados: '+ str(self.device_list))
        self.identity = identity
        if self.identity=='':
            self.identity = self.get_id()
        self.electronic_load = self.rm.open_resource(self.identity)

    def get_id(self):
        for device_id in self.device_list:
            if (len(device_id.split('::')) == 5 and
                device_id.split('::')[3].startswith('DL')):
                return device_id    
        print ('Carga electrónica no detectadada')
        return ''        

    def voltage_min(self, voltage):
        self.electronic_load.write(":SOUR:CURR:VON "+str(voltage))

    def current_max(self, current):
        self.electronic_load.write(":SOUR:CURR:LEV:IMM "+str(current))

    def eload_voltage(self):
        return float(self.electronic_load.query(':MEAS:VOLT?'))

    def eload_current(self):
        return float(self.electronic_load.query(':MEAS:CURR?'))   

    def on(self):
        self.electronic_load.write(':SOUR:INP:STAT ON')

    def off(self):
        self.electronic_load.write(':SOUR:INP:STAT OFF')
