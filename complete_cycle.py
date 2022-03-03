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
import numpy as np 

ser = serial.Serial ( 'COM3' )
temp = ser.readline ()
inicio = time.time()

storedDataI = []
storedDataV = []
listVdiff = []
abs_smadiff = []
window_size = 100
sma_listVdiff = []

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
    storedDataV.append(newData)
    if(len(storedDataV) >= listSize):
        storedDataV.pop(0)
    for i in range(0, len(storedDataV)):
        sum = sum + storedDataV[i]
    average = sum/len(storedDataV)
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
V_E = float(get_setting('V_E'))

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
        value.append(moving_averageI(I, 100))
        value.append(moving_averageV(value[0], 100))     
        i = 0 
        listVdiff = [storedDataV[n]-storedDataV[n-1] for n in range(1,len(storedDataV))]
        abs_smadiff = [abs(ele) for ele in listVdiff]
        i = 0
        while i < len(abs_smadiff)- window_size+1:
            window = abs_smadiff[i : i + window_size]
            window_average = sum(window)/window_size
            sma_listVdiff.append(window_average)
            i+=1

        def Average (sma_listVdiff):
            return sum(sma_listVdiff)/len(sma_listVdiff)	
        E = Average(sma_listVdiff)
        value.append(E)      
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

    #CARGA
    set_power_supply()        
    file = open("CARGA" + "_" + str(cycle_number)+ "_"+ run_time() + '.txt', 'w', newline='')
    file.write(DATA_LINE_CHARGE + '\n')
    power_supply.on()
    values = readdaq()
    time.sleep(3)
    while values[2] > I_MIN:
        temp = ser.readline ()
        save_file_charge(file)
    power_supply.off()  

    save_file_charge(file)

    #ESTABILIZACIÓN
    while values[4]> V_E:
        temp = ser.readline () 
        save_file_charge(file) 
        print(values[4])

    file.close() 

    file = open("DESCARGA" + "_" + str(cycle_number)+ "_"+ run_time() + '.txt', 'w', newline='')
    file.write(DATA_LINE_DISCHARGE + '\n')
    set_electronic_load()
    electronic_load.on()

    #DESCARGA
    while values[0] > V_MIN:
        temp = ser.readline ()
        save_file_discharge(file)   
    electronic_load.off()  
         
    while values[4] > V_E:
        temp = ser.readline ()
        save_file_discharge(file)  
  
    file.close()     
    cycle_number=+1 
power_supply.off
electronic_load.off