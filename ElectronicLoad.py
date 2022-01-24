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

    def voltage_min(self, voltage):
        self.electronic_load.write(":SOUR:CURR:VON "+str(voltage))

    def current_max(self, current):
        self.electronic_load.write(":SOUR:CURR:LEV:IMM "+str(current))

    def electronic_load_voltage(self):
        return float(self.electronic_load.query(':MEAS:VOLT?'))

    def electronic_load_current(self):
        return float(self.query(':MEAS:CURR?'))   

    def on(self):
        self.electronic_load.write(':SOUR:INP:STAT ON')

    def off(self):
        self.electronic_load.write(':SOUR:INP:STAT OFF')
