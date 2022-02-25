import random

V_E = 1e-3

E = 1
while E > V_E:
    # save_file_charge(file)  
    listVdiff = []
    i = 0
    window_size = 10
    sma_listVdiff = []
    abs_smadiff = []
    # values = readdaq()
    # smoothed_v = values[s3]
    listV = [1e-5, 2e-5, 3e-5, 20e-5]
    # while i <30:  
        # values= readdaq()
        # listV.append(values[3])
        # i+=1
    listVdiff = [listV[n]-listV[n-1] for n in range(1,len(listV))]
    print(listVdiff)
    abs_smadiff = [abs(ele) for ele in listVdiff]
    print(abs_smadiff)

    while i < len(abs_smadiff) - window_size + 1:
        print(i)
        window = abs_smadiff[i : i + window_size]
        print(window)
        window_average = round(sum(window)/window_size,2)
        sma_listVdiff.append(window_average)
        i+=1
    print(sma_listVdiff)

    def Average (abs_smadiff):
        return sum(abs_smadiff)/len(abs_smadiff)	
    E = Average(abs_smadiff)
    listE = []
    listE.append(E)
    print(E)