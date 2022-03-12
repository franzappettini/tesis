inputs = I_MIN, V_MIN, N_MEASUREMENTS, I_MAX, V_MAX, CYCLES, V_E
outputs = file(V, I, temperature, time)
number_cycle = 0

#OPEN CIRCUIT VOLTAGE
for i in range(N_MEASUREMENTS):
    [V, I, temperature, time] = update()
    write.file(V, I, temperature, time)

while number_cycle < cycles:
    #CHARGE
    power_supply(set.I_MAX, set.V_MAX, set.I_MIN)	
    power_supply.on
    open file
    while I > I_MIN:
        [V, I, temperature, time] = update()
        write.file(V, I, temperature, time)
    end while
    power_supply.off
    #STABILIZATION
    while E > V_E:
        V = read.V
        lista = absolute_value(difference(moving_average(V),100)))
        E = average (lista)
    close file    
    electronic_load(set.V_MIN, I_MAX)
    electronic_load.on
    open file
    #DISCHARGE
    while V > V_MIN:
        [V, I, temperature, time] = update()
        write.file(V, I, temperature, time)
    end while
    power_supply.off    
    #STABILIZATION
    while E > V_E:
        V = read.V
        lista = absolute_value(difference(moving_average(V),100)))
        E = E = average (lista)
    close file
    cycle_number=+1




    
