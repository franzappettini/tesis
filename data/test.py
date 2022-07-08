import pandas as pd
import matplotlib.pyplot as plt
import csv
df_d = []
df = pd.read_csv('V_losses.txt')
df_tiempo = df[' time']
df_supply_voltage = df[' supply voltage']
df_n = df['Vbattery'] - df[' sma Vbattery']
df_d = df[' supply voltage']-df['Vbattery']
df_p = df[' supply voltage']-df[' sma Vbattery']
#with open('losses_voltage.txt', 'w', newline='') as f:
#    plots = csv.reader(f, delimiter=',')
#    f.write(str(df_d))

    


#df['losses'] = df[' supply voltage']-df['Vbattery']

plt.plot(df_tiempo, df_p, label = 'pérdidas de voltaje')
plt.grid()
plt.xlabel('tiempo (s)')
plt.ylabel('Voltaje (V)')
plt.show()


