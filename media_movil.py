import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#Programa para calcular medias moviles y graficarlas

def sma(data, period):   #subfuncion para obtener el sma
    sma1=np.zeros(data.size+1-period)
    for step in range(
            len(sma1)):
        sma1[step]=np.mean(data[step:period+step])
    return sma1

datos = pd.read_csv("carga_50_1.txt")  # se lee el csv

periodo = 300  # periodo del sma
sma = sma(datos[" current"], periodo)  # calculo del sma
x = np.arange(0, len(datos[" current"]))  # eje x para graficar

plt.plot(x, datos[" current"], label="C")  
plt.plot(x[periodo-1:], sma, label="Sma " + str(periodo))  # grafica sma
plt.legend()
plt.grid(True)
plt.show()
