import matplotlib.pyplot as plt
import csv

tiempo = []
Vcell = []
Current = []
temp = []
I_supply = []

with open('carga_50_1.txt','r', newline='') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')
    next(plots)
    for row in plots:
        tiempo.append(float(row[1]))
        Vcell.append(float(row[0]))
        Current.append(float(row[2]))
        temp.append(float(row[3]))
        I_supply.append(float(row[4]))

#plt.plot(tiempo, I_supply, label = ' I/V')
plt.plot(tiempo,Vcell, label = 'V1')
#plt.plot(tiempo,Current, label = 'V2')
plt.grid()
plt.xlabel('tiempo (s)')
plt.ylabel('Vcell (V)')
plt.title('carga de una celda')

plt.show()
