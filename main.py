import random
import numpy as np
import math
import matplotlib.pyplot as plt
from tabulate import tabulate

num_customers = 10000
Customers = []
InterArrivalTime = []
ArrivalTime = []
StartTime = []
WaitingTime = []
ServiceTime = []
CompletionTime = []
TimeInSystem = []
ATM1 = []
ATM2 = []

def generate_IAT():
    return np.random.uniform(0,5)

def generate_ST():
    return np.random.normal(2, 0.5)

#(Normal distribution with mean=2, std=0.5)
ServiceTime1 = []
ServiceTime2 = []
maxInQueue = 0



for i in range(num_customers):
    Customers.append(i+1)
    if i == 0: #Customer 1
        IAT = generate_IAT()
        IAT = math.floor(IAT * 10) / 10
        InterArrivalTime.append(IAT)
        ArrivalTime.append(IAT)
        StartTime.append(ArrivalTime[i])
        WaitingTime.append(0)
        ST = generate_ST()
        ST = math.floor(ST * 10) / 10
        ServiceTime.append(ST)
        ServiceTime1.append(ST)
        CompletionTime.append(StartTime[i]+ ServiceTime[i])
        TimeInSystem.append(CompletionTime[i] - ArrivalTime[i])
        ATM1.append(CompletionTime[i])
        ATM2.append(0)
    else:
        IAT = generate_IAT()
        IAT = math.floor(IAT * 10) / 10
        InterArrivalTime.append(IAT)
        ArrivalTime.append(ArrivalTime[i - 1] + InterArrivalTime[i])
        atm = min(ATM1[i-1],ATM2[i-1])
        StartTime.append(max(ArrivalTime[i],atm))
        WaitingTime.append(StartTime[i]-ArrivalTime[i])
        ST = generate_ST()
        ST = math.floor(ST * 10) / 10
        ServiceTime.append(ST)
        if atm==ATM1[i-1]:
            ServiceTime1.append(ST)
            CompletionTime.append(StartTime[i] + ServiceTime[i])
            ATM1.append(CompletionTime[i])
            ATM2.append(ATM2[i-1])
        else:
            ServiceTime2.append(ST)
            CompletionTime.append(StartTime[i] + ServiceTime[i])
            ATM2.append(CompletionTime[i])
            ATM1.append(ATM1[i-1])

        TimeInSystem.append(CompletionTime[i] - ArrivalTime[i])
c = 0
for i in range(num_customers):
    if(WaitingTime[i] > 0):
        c = c+1
    else:
        maxInQueue = max(c,maxInQueue)
        c = 0

AvgWaitingTime= sum(WaitingTime)/num_customers
NumWaitingCust = sum(1 for wt in WaitingTime if wt > 0)
TotalTime = max(CompletionTime)
TotalSimTime = CompletionTime[num_customers-1]
ProbOfWaiting = NumWaitingCust/num_customers
UtilizationOfATM1 = sum(ServiceTime1)/ATM1[num_customers-1]
UtilizationOfATM2 = sum(ServiceTime2)/ATM2[num_customers-1]
AverageTIS = sum(TimeInSystem)/num_customers
print("Average waiting time: ",AvgWaitingTime)
print("Number of customers who had to wait: ",NumWaitingCust)
print("The total time of the simulation: ",TotalSimTime)
print("The probability that a customer will have to wait: ",ProbOfWaiting)
print("Utilization of ATM1: ",UtilizationOfATM1)
print("Utilization of ATM2: ",UtilizationOfATM2)
print("Maximum number in the queue: ",maxInQueue)
print("Average time in the system: ",AverageTIS)
print()
#histogram for waiting time
plt.hist(WaitingTime, bins=20, edgecolor='black')
plt.title('Histogram of Waiting Time')
plt.xlabel('Waiting Time (minutes)')
plt.ylabel('Frequency')
plt.show()
#print table
num_elements = 15
headers = ["Customer","InterArrival Time", "Arrival Time", "Service Start Time", "Waiting Time", "Service Time", "Completion Time", "Time In System", "ATM1", "ATM2"]
data = list(zip(Customers[:num_elements],InterArrivalTime[:num_elements], ArrivalTime[:num_elements], StartTime[:15], WaitingTime[:num_elements],
                ServiceTime[:num_elements], CompletionTime[:num_elements], TimeInSystem[:num_elements], ATM1[:num_elements], ATM2[:num_elements]))
table = tabulate(data, headers, tablefmt="fancy_grid")
print(table)

