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
inicio = time.time()

storedDataI = []
storeDataV = []

def moving_averageI(newData ,listSize):
    sum = 0
    storedDataI.append(newData)
    if(len(storedDataI) >= listSize):
        storedDataI.pop(0)
    for i in range(0, len(storedDataI)):
        sum = sum + storedDataI[i]
    average = sum/len(storedDataI)
    return average 

def moving_averageV(newData ,listSize):
    sum = 0
    storeDataV.append(newData)
    if(len(storeDataV) >= listSize):
        storeDataV.pop(0)
    for i in range(0, len(storeDataV)):
        sum = sum + storeDataV[i]
    average = sum/len(storeDataV)
    return average  

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
DATA_LINE_CHARGE = str(get_setting('DATA_LINE_CHARGE'))
DATA_LINE_DISCHARGE = str(get_setting('DATA_LINE_DISCHARGE'))
N_MEASUREMENTS = int(get_setting('N_MEASUREMENTS'))
V_E1 = float(get_setting('V_E1'))
V_E2 = float(get_setting('V_E2'))
value = [0,0]
valuestr = ''

power_supply.read_termination = '\n'

def run_time():
    return datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')

def readdaq():
    with nidaqmx.Task() as task:
        task.ai_channels.add_ai_voltage_chan("cDAQ1Mod1/ai0:1", terminal_config=TerminalConfiguration.DIFFERENTIAL)
        value = task.read()
        I = (value[1]+0.022795518411719402)/0.0847029
        if(len(value) > 3):
            value.pop(3)
        value.append(moving_averageI(I, 100))
        value.append(moving_averageV(value[0], 100))
        #print(value)
        time.sleep(0.1)
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
    file.write(str(valuestr)+','+str(run_time())+','+str(time.time() - inicio)+','+str(power_supply.supply_voltage())+','+str(power_supply.supply_current())+','+str(temp.decode('utf-8')))
    time.sleep(0.1)
    file.flush()

def save_file_discharge(file):
    value = readdaq()
    valuestr = ','.join(map(str,value))
    file.write(str(valuestr)+','+str(run_time())+','+str(time.time() - inicio)+','+str(electronic_load.eload_voltage())+','+str(electronic_load.eload_current())+','+str(temp.decode('utf-8')))
    file.flush()
    
file = open("SOC" + "_"+ run_time() + '.txt', 'w', newline='')

for i in range(N_MEASUREMENTS):
    value = readdaq()
    valuestr = ','.join(map(str,value))
    print(valuestr, run_time(), temp.decode('utf-8'))
    file.write(str(valuestr)+','+str(run_time())+','+str(time.time() - inicio)+','+str(temp.decode('utf-8')))
file.close()

while cycle_number < CYCLES:
    set_power_supply()                  
    file = open("CARGA" + "_" + str(cycle_number)+ "_"+ run_time() + '.txt', 'w', newline='')
    file.write(DATA_LINE_CHARGE + '\n')
    I = (value[1]+0.022795518411719402)/0.0847029
    power_supply.on()
    values = readdaq()
    smoothed_i = values[2]
    smoothed_v = values[3]
    while smoothed_i > I_MIN:    #CARGA
        save_file_charge(file)
        values = readdaq()
        smoothed_i = values[2]
        smoothed_v = values [3]
        print(values[0], values[1],smoothed_i, smoothed_v)
    power_supply.off()    
    while smoothed_v > V_E1:    #ESTABILIZACIÓN
        save_file_charge(file)
        values = readdaq()
        smoothed_v = values [3]
        print(smoothed_v)      
    file.close() 

    file = open("DESCARGA" + "_" + str(cycle_number)+ "_"+ run_time() + '.txt', 'w', newline='')
    file.write(DATA_LINE_DISCHARGE + '\n')
    set_electronic_load()
    electronic_load.on()
    values = readdaq()
    smoothed_v = values[3]
    smoothed_i = values[2]
    while values[3] > V_MIN:    #DESCARGA
         save_file_discharge(file)
         values = readdaq()
         smoothed_i = values[2]
         smoothed_v = values[3]
         print(values[3])     
    electronic_load.off()   
    while smoothed_v < V_E2:
        save_file_discharge(file)
        values = readdaq()
        smoothed_v = values [3]
        print(smoothed_v)  
    file.close()     
    cycle_number=+1 