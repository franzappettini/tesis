import pyvisa
import time 
import os
import nidaqmx
import csv
import serial
import datetime
from PowerSupply import PowerSupply
from ElectronicLoad import ElectronicLoad
from nidaqmx.constants import (TerminalConfiguration)
import configparser
from configparser import ConfigParser

ser = serial.Serial ( 'COM5' )
temp = ser.readline ()

def get_setting(setting):
    return configFile[config_profile][setting]

def choose_setting():                                       #Se define el perfil de carga con parámetros del archivo config
    print('Seleccionar perfil de carga:\n')
    keys = list(configFile.keys())
    for setting in keys:
        print (str(keys.index(setting))+': '+setting)
    n = int(input('Ingresar el número de perfil entre cero y '+str(len(keys)-1)+': '))
    return keys[int(n)+1]

power_supply = PowerSupply()
electronic_load = ElectronicLoad()

configFile = configparser.ConfigParser()
configFile.read('config.ini')
config_profile = choose_setting()

#Aquí se extraen los parámetros del archivo de config
V_MAX = float(get_setting('V_MAX'))
I_MAX = float(get_setting('I_MAX'))
I_MIN = float(get_setting('I_MIN'))
V_MIN = float(get_setting('V_MIN'))
CYCLES = float(get_setting('CYCLES'))
DATA_LINE = str(get_setting('DATA_LINE'))
N_MEASUREMENTS = int(get_setting('N_MEASUREMENTS'))
value = [0,0]
valuestr = ''

power_supply.read_termination = '\n'

def run_time():
    return datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')

def readdaq():
    with nidaqmx.Task() as task:
        task.ai_channels.add_ai_voltage_chan("cDAQ1Mod1/ai0:1", terminal_config=TerminalConfiguration.DIFFERENTIAL)
        value = task.read()
        I = (value[1]+0.022795518411719402)/0.0847029
        time.sleep(1)
    return value

def set_power_supply():
    power_supply.voltage_current_max(V_MAX, I_MAX)
    power_supply.sensor_ch1()
    power_supply.sensor_ch2()

def set_electronic_load():
    electronic_load.voltage_min(V_MIN)
    electronic_load.current_max(I_MAX)
    
cycle_number = 0

def save_file_charge(file):
    value = readdaq()
    valuestr = ','.join(map(str,value))
    file.write(str(valuestr)+','+str(run_time())+','+str(power_supply.supply_voltage())+','+str(power_supply.supply_current())+','+str(temp.decode('utf-8')))
    file.flush()

def save_file_discharge(file):
    value = readdaq()
    valuestr = ','.join(map(str,value))
    file.write(str(valuestr)+','+str(run_time())+','+str(electronic_load.eload_voltage())+','+str(electronic_load.eload_current())+','+str(temp.decode('utf-8')))
    file.flush()
    time.sleep(1)
    
set_power_supply()
set_electronic_load()

file = open("SOC" + "_"+ run_time() + '.txt', 'a', newline='')

for i in range(N_MEASUREMENTS):
    value = readdaq()
    valuestr = ','.join(map(str,value))
    print(valuestr, run_time(), temp.decode('utf-8'))
    file.write(str(valuestr)+','+str(run_time())+','+str(temp.decode('utf-8')))
file.close()

while cycle_number < CYCLES:
    set_power_supply()                  
    file = open("CARGA" + "_" + str(cycle_number)+ "_"+ run_time() + '.txt', 'a', newline='')
    file.write(DATA_LINE + '\n')
    I = (value[1]+0.022795518411719402)/0.0847029
    power_supply.on()
    while power_supply.supply_current() > I_MIN:
        save_file_charge(file)
    file.close()
    power_supply.off()
    time.sleep(10)
     #AQUI VA EL ERROR DE MEDICIÓN DE VOLTAJE
    electronic_load.on()
    set_electronic_load()
    file = open("DESCARGA" + "_" + str(cycle_number)+ "_"+ run_time() + '.txt', 'a', newline='')
    file.write(DATA_LINE + '\n')
    while value[0] > V_MIN:
         save_file_discharge(file)
    file.close()     
    electronic_load.off()   
    cycle_number=+1 