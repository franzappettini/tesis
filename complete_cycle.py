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
N_MEASUREMENTS = float(get_setting('N_MEASUREMENTS'))

def run_time():
    return datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')

def readdaq():
    task = nidaqmx.Task()
    task.ai_channels.add_ai_voltage_chan("cDAQ1Mod1/ai0:1", terminal_config=TerminalConfiguration.DIFFERENTIAL)
    task.start()
    I = task.read()
    task.stop()
    return I

def set_power_supply():
    power_supply.voltage_current_max(V_MAX, I_MAX)

def set_electronic_load():
    electronic_load.voltage_min(V_MIN)
    electronic_load.current_max(I_MAX)

set_power_supply()
set_electronic_load()

for i in range(N_MEASUREMENTS):         #Tomar lecturas de la batería para estimar el estado de carga previo a comenzar la carga
    readdaq()
    temp = ser.readline ()
    run_time()
    power_supply.supply_voltage()
    power_supply.supply_current()

number_cycle = 0
    
while number_cycle < CYCLES:
    set_power_supply()                  
    power_supply.on()
    while I > I_MIN:
            with open('data\\' + "CARGA" + "_" + str(number_cycle) + "_" + run_time() + '.txt', 'w') as file:
                file.write(DATA_LINE)
                file.write("\n")
                readdaq()
                temp = ser.readline ()
                run_time()
                power_supply.supply_voltage()
                power_supply.supply_current()                       
    power_supply.off()
    
     #AQUI VA EL ERROR DE MEDICIÓN DE VOLTAJE
    electronic_load.on()
    set_electronic_load()
    while V > V_MIN:
            with open('data\\' + "DESCARGA"+"_" + str(number_cycle) + "_" + run_time() + '.txt', 'w') as file:
                file.write(DATA_LINE)
                file.write("\n")
                readdaq()
                temp = ser.readline ()
                run_time()
                electronic_load.eload_voltage_voltage()
                electronic_load.eload_current_current()
    electronic_load.off()   
    number_cycle=+1 

