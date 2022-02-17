import random
import numpy as np

listV = np.random.random_sample(size = 50)
print(listV)

window_size = 10

i = 0
moving_averages = []

while i < len(listV) - window_size + 1:

	window_average = round(np.sum(listV[i:i+window_size]) / window_size, 2)
	moving_averages.append(window_average)
	i += 1

print(moving_averages)

listVdiff = [listV[n]-listV[n-1] for n in range(1,len(listV))]
print(listVdiff)

i = 0
smadiff = []
while i < len(listVdiff) - window_size + 1:
	window_average = round(np.sum(listVdiff[i:i+window_size]) / window_size, 2)
	smadiff.append(window_average)
	i += 1

print(smadiff)


abssmadiff = [abs(ele) for ele in smadiff]
print(abssmadiff)
