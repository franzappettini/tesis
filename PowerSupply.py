import pyvisa
import time 
import os
import nidaqmx
import csv
import serial
import configparser
from configparser import ConfigParser

class PowerSupply(object):
    def __init__(self, identity = ''):
        self.rm = pyvisa.ResourceManager()
        self.device_list = self.rm.list_resources()
        self.identity = identity
        if self.identity=='':
            self.identity = self.get_id()
        self.power_supply = self.rm.open_resource(self.identity)

    def get_id(self):
        for device_id in self.device_list:
            if (len(device_id.split('::')) == 5 and
                device_id.split('::')[3].startswith('DP')):
                return device_id    
        print ('Fuente de poder no detectada')
        return ''
            
    def supply_voltage(self):
        return float(self.power_supply.query(':MEAS:VOLT? CH3'))

    def supply_current(self):
        return float(self.power_supply.query(':MEAS:CURR? CH3'))

    def on(self):
        self.power_supply.write(':OUTP CH3, ON')

    def off(self):
        self.power_supply.write(':OUTP CH3, OFF')

    def voltage_current_max(self, voltage, current):
        self.power_supply.write(":APPL CH3,"+str(voltage)+","+str(current))
