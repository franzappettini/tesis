readings = np.array([])
reading = 10
max_samples = 10

readings = np.append(readings, reading)
avg = np.mean(readings)

print('current average =', avg)
print('readings used for average:', readings)

if len(readings)==max_samples:
    readings = np.delete(readings,0)
print('readings saved for next time:', readings)    
