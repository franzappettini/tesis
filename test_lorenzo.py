import time
from random import seed
from random import random
seed(1)

def moving_average(newData ,listSize, lista):
    sum = 0
    lista.append(newData)
    if(len(lista) >= listSize):
        lista.pop(0)
    for i in range(0, len(lista)):
        sum = sum + lista[i]
    average = sum/len(lista)
    return average 

def absDiffList(lista, diffStep):
    print("lista", lista)
    print("len lista = ",len(lista))
    print("last lista =",lista[-1])
    if len(lista) - diffStep < 0:
        return abs(lista[-1])
    else:
        return abs(lista[-1] - lista[len(lista) -1 - diffStep])

listV = []
listI = []
window_size = 5
sma_listVdiff = [1]
Elorenzo = []

while True:
    value = [random()*4, random()*8]

    I = (value[1] + 0.022795518411719402)/0.0847029
    value.append(moving_average(I, 8, listI))
    value.append(moving_average(value[0], 8, listV))
    print("value = ", value)
    print("listV = ", listV)
    print("listI = ", listI)

    i = 0
    listVdiff = [listV[n] - listV[n - 1] for n in range(1,len(listV))]
    print("listVdiff = ", listVdiff)
    abs_smadiff = [abs(ele) for ele in listVdiff]
    print("abs_smadiff = ", abs_smadiff)
    
    while i < len(abs_smadiff) - window_size + 1:
        print("i = ", i)
        window = abs_smadiff[i : i + window_size]
        window_average = sum(window)/window_size
        sma_listVdiff.append(window_average)
        i+=1
    print("sma_listVdiff = ", sma_listVdiff)
    E = sum(sma_listVdiff)/len(sma_listVdiff)
    print("E = ", E, "\n")

    moving_average(absDiffList(listV,1), 5, Elorenzo)
    print("Elorenzo = ", Elorenzo)
    Ef = sum(Elorenzo)/len(Elorenzo)
    print("Ef = ", Ef)
    time.sleep(1)