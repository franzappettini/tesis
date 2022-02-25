def moving_averageV(newData ,listSize):
    sum = 0
    storedDataV.append(newData)
    if(len(storedDataV) >= listSize):
        storedDataV.pop(0)
    for i in range(0, len(storedDataV)):
        sum = sum + storedDataV[i]
    average = sum/len(storedDataV)
    return average

def moving_average(newData ,listSize, lista):
    sum = 0
    lista.append(newData)
    if(len(lista) >= listSize):
    	print(len(lista))
    	print(listSize)
    	lista.pop(0)
    for i in range(0, len(lista)):
        sum = sum + lista[i]
    average = sum/len(lista)
    return average

storedDataV = [1]
storedDataI = [10]

MAV = moving_average(7,5,storedDataV)
MAI = moving_average(7,3,storedDataI)

print(storedDataV)
print(MAV)

print(storedDataI)
print(MAI)

MAV = moving_average(7,3,storedDataV)
MAI = moving_average(7,3,storedDataI)

print(storedDataV)
print(MAV)

print(storedDataI)
print(MAI)

MAV = moving_average(7,3,storedDataV)
MAI = moving_average(7,3,storedDataI)

print(storedDataV)
print(MAV)

print(storedDataI)
print(MAI)