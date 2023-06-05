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
import cProfile

#ser = serial.Serial ( 'COM4' )
#temp = ser.readline ()
inicio = time.time()
#E = []
listV = []
listI = []
lista = []
#E_V = []
#error_lista = []
cycle_number = 0

#def moving_averageI(newData ,listSize):
#    sum = 0
#    storedDataI.append(newData)
#    if(len(storedDataI) >= listSize):
#        storedDataI.pop(0)
#    for i in range(0, len(storedDataI)):
#        sum = sum + storedDataI[i]
#    average = sum/len(storedDataI)
#    return average 

def moving_average(newData ,listSize, lista):
    sum = 0
    lista.append(newData)
    if(len(lista) >= listSize):
        lista.pop(0)
    for i in range(0, len(lista)):
        sum = sum + lista[i]
    average = sum/len(lista)
    return average

#def absDiffList(lista, diffStep):
    #print("lista", lista)
    #print("len lista = ",len(lista))
    #print("last lista =",lista[-1])
#    if len(lista) - diffStep < 0:
#        return abs(lista[-1])
#    else:
#        return abs(lista[-1] - lista[len(lista) -1 - diffStep])    

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
#V_E = float(get_setting('V_E'))

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
        value.append(moving_average(I, 100, listI))
        value.append(moving_average(value[0], 100, listV)) 
        #moving_average(absDiffList(listV,1), 100, error_lista)
        #EV = sum(error_lista)/len(error_lista)
        #value.append(EV)
        #value.append(moving_average(EV, 100, E_V))     
        #value.append(moving_average(absDiffList(listV,1), 100, EV))
        time.sleep(1)
    return value

def set_power_supply():
    power_supply.voltage_current_max(V_MAX, I_MAX)
    power_supply.sensor_ch1()
    power_supply.sensor_ch2()

def set_electronic_load():
    electronic_load.voltage_min(V_MIN)
    electronic_load.current_max(I_MAX)

def save_file_charge(file):
    value = readdaq()
    valuestr = ','.join(map(str,value))
    file.write(str(valuestr)+','+str(run_time())+','+str(time.time() - inicio)+','+str(power_supply.supply_voltage())+','+str(power_supply.supply_current())+'\n')#+','+str(temp.decode('utf-8')))
    file.flush()

def save_file_discharge(file):
    value = readdaq()
    valuestr = ','.join(map(str,value))
    file.write(str(valuestr)+','+str(run_time())+','+str(time.time() - inicio)+','+str(electronic_load.eload_voltage())+','+str(electronic_load.eload_current())+'\n')#+','+str(temp.decode('utf-8')))
    file.flush()      
 
while cycle_number < CYCLES:
    #CARGA
    set_power_supply()   
    power_supply.on()    
    time.sleep(4) 
    file = open("CARGA" + "_" + str(cycle_number)+ "_"+ run_time() + '.txt', 'w', newline='')
    file.write(DATA_LINE_CHARGE + '\n')
    value = readdaq()
    
    while power_supply.supply_current() > I_MIN:
        #temp = ser.readline ()
        save_file_charge(file)
       
    power_supply.off()
    start_time = datetime.datetime.now() #end time is 10 sec after the current time
    end_time = start_time + datetime.timedelta(seconds=120) #Run the loop till current time exceeds end time
    while end_time > datetime.datetime.now():
        save_file_charge(file)  
    file.close() 

    #DESCARGA
    file = open("DESCARGA" + "_" + str(cycle_number)+ "_"+ run_time() + '.txt', 'w', newline='')
    file.write(DATA_LINE_DISCHARGE + '\n')
    set_electronic_load()
    electronic_load.on()
    value = readdaq()
    while electronic_load.eload_voltage() > V_MIN:
        #temp = ser.readline ()
        save_file_discharge(file)   
    electronic_load.off()
    start_time = datetime.datetime.now() #end time is 10 sec after the current time
    end_time = start_time + datetime.timedelta(seconds=120) #Run the loop till current time exceeds end time
    while end_time > datetime.datetime.now():
        save_file_discharge(file)   
    value = readdaq()         
    time.sleep(10)
    file.close()     
cycle_number=+1 
