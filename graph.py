import matplotlib.pyplot as plt
import csv

tiempo = []
Vcell = []
Current = []
temp = []
I_supply = []
sma_current = []
sma_voltage = []


with open('CARGA_0_2022-02-09-11-30-36.txt','r', newline='') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')
    next(plots)
    for row in plots:
        tiempo.append(float(row[5]))
        Vcell.append(float(row[0]))
        Current.append(float(row[1]))
        temp.append(float(row[7]))
        I_supply.append(float(row[6]))
        sma_current.append(float(row[2]))
        sma_voltage.append(float(row[3]))

with open('DESCARGA_0_2022-02-09-14-57-17.txt','r', newline='') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')
    next(plots)
    for row in plots:
        tiempo.append(float(row[5]))
        Vcell.append(float(row[0]))
        Current.append(float(row[1]))
        temp.append(float(row[7]))
        I_supply.append(float(row[6]))
        sma_current.append(float(row[2]))
        sma_voltage.append(float(row[3]))

#plt.plot(tiempo, I_supply, label = ' I/V')
plt.plot(tiempo,Vcell, label = 'Vcell')
#plt.plot(tiempo,sma_current, label = 'sma current')
#plt.plot(tiempo,Current, label = 'current')
#plt.plot(tiempo, sma_voltage, label = 'sma voltage')
plt.grid()
plt.xlabel('tiempo (s)')
plt.ylabel('Vcell (V)')
plt.title('carga de una celda')

plt.show()
