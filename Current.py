import random
import numpy as np
import matplotlib.pyplot as plt

num_customers = 10
#(Uniform distribution between 0 and 5 minutes)
InterArrivalTime = np.random.uniform(0,5)
ArrivalTime = []
StartTime = []
WaitingTime = []
CompletionTime = []
TimeInSystem = []

#(Normal distribution with mean=2, std=0.5)
ServiceTime1 = np.random.normal(2, 0.5)
ServiceTime2 = np.random.normal(2, 0.5)

ATM1 = []
ATM2 = []

for i in range(num_customers):
    if i == 0: #Customer 1
        ArrivalTime.append(InterArrivalTime[i])
        StartTime.append(ArrivalTime[i])
        WaitingTime.append(0)
        CompletionTime.append(StartTime[i] + ServiceTime1[i])
        TimeInSystem.append(CompletionTime[i] - ArrivalTime[i])
        ATM1.append(CompletionTime[i])
        ATM2.append(0)
    else:
        ArrivalTime.append(ArrivalTime[i - 1] + InterArrivalTime[i])
        #the rest of the logic

AvgWaitingTime= sum(WaitingTime)/num_customers
NumWaitingCust = sum(1 for wt in WaitingTime if wt > 0)
TotalTime = max(CompletionTime)
WaitingProb = (WaitingTime / num_customers) * 100
#Utilization1 = sum(ServiceTime1) /
