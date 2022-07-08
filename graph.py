import matplotlib.pyplot as plt
import csv

tiempo = []
Vcell = []
Current = []
temp = []
I_supply = []
sma_current = []
sma_voltage = []
error = []


with open('CARGA_0_2022-02-23-15-06-50.txt','r', newline='') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')
    next(plots)
    for row in plots:
        tiempo.append(float(row[5]))
        Vcell.append(float(row[0]))
        Current.append(float(row[1]))
        temp.append(float(row[7]))
        I_supply.append(float(row[8]))
        sma_current.append(float(row[2]))
        sma_voltage.append(float(row[3]))
        #error.append(float(row[4]))

with open('DESCARGA_0_2022-02-23-13-02-32.txt','r', newline='') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')
    next(plots)
    for row in plots:
        tiempo.append(float(row[5]))
        Vcell.append(float(row[0]))
        Current.append(float(row[1]))
        temp.append(float(row[7]))
        I_supply.append(float(row[8]))
        sma_current.append(float(row[2]))
        sma_voltage.append(float(row[3]))
        #error.append(float(row[4]))

#plt.plot(tiempo, I_supply, label = ' I/V')
plt.plot(tiempo,Vcell, label = 'Vcell')
#plt.plot(tiempo, error, label = 'error')
plt.plot(tiempo,sma_current, label = 'sma current')
#plt.plot(tiempo,Current, label = 'current')
#plt.plot(tiempo, sma_voltage, label = 'sma voltage')
plt.grid()
plt.xlabel('tiempo (s)')
plt.ylabel('Vcell (V)')
plt.title('Cycle')

plt.show()
