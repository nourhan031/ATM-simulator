import random
import numpy as np
import math
import matplotlib.pyplot as plt
from tabulate import tabulate


class ATMSystem:
    def __init__(self, num_customers):
        self.num_customers = num_customers
        self.Customers = []
        self.InterArrivalTime = []
        self.ArrivalTime = []
        self.StartTime = []
        self.WaitingTime = []
        self.ServiceTime = []
        self.CompletionTime = []
        self.TimeInSystem = []
        self.ATM1 = []
        self.ATM2 = []
        self.ServiceTime1 = []
        self.ServiceTime2 = []
        self.maxInQueue = 0

    def generate_IAT(self):
        return np.random.uniform(0, 5)

    def generate_ST(self):
        return np.random.normal(2, 0.5)

    def simulate(self):
        for i in range(self.num_customers):
            self.Customers.append(i + 1)
            IAT = self.generate_IAT()
            IAT = math.floor(IAT * 10) / 10
            self.InterArrivalTime.append(IAT)
            if i == 0:  # Customer 1
                self.ArrivalTime.append(IAT)
                self.StartTime.append(self.ArrivalTime[i])
                self.WaitingTime.append(0)
                ST = self.generate_ST()
                ST = math.floor(ST * 10) / 10
                self.ServiceTime.append(ST)
                self.ServiceTime1.append(ST)
                self.CompletionTime.append(self.StartTime[i] + self.ServiceTime[i])
                self.TimeInSystem.append(self.CompletionTime[i] - self.ArrivalTime[i])
                self.ATM1.append(self.CompletionTime[i])
                self.ATM2.append(0)
            else:
                self.ArrivalTime.append(self.ArrivalTime[i - 1] + self.InterArrivalTime[i])
                atm = min(self.ATM1[i - 1], self.ATM2[i - 1])
                self.StartTime.append(max(self.ArrivalTime[i], atm))
                self.WaitingTime.append(self.StartTime[i] - self.ArrivalTime[i])
                ST = self.generate_ST()
                ST = math.floor(ST * 10) / 10
                self.ServiceTime.append(ST)
                if atm == self.ATM1[i - 1]:
                    self.ServiceTime1.append(ST)
                    self.CompletionTime.append(self.StartTime[i] + self.ServiceTime[i])
                    self.ATM1.append(self.CompletionTime[i])
                    self.ATM2.append(self.ATM2[i - 1])
                else:
                    self.ServiceTime2.append(ST)
                    self.CompletionTime.append(self.StartTime[i] + self.ServiceTime[i])
                    self.ATM2.append(self.CompletionTime[i])
                    self.ATM1.append(self.ATM1[i - 1])
                self.TimeInSystem.append(self.CompletionTime[i] - self.ArrivalTime[i])

        self.calculate_statistics()

    def calculate_statistics(self):
        c = 0
        for i in range(self.num_customers):
            if self.WaitingTime[i] > 0:
                c = c + 1
            else:
                self.maxInQueue = max(c, self.maxInQueue)
                c = 0

        AvgWaitingTime = sum(self.WaitingTime) / self.num_customers
        NumWaitingCust = sum(1 for wt in self.WaitingTime if wt > 0)
        TotalTime = max(self.CompletionTime)
        TotalSimTime = self.CompletionTime[self.num_customers - 1]
        ProbOfWaiting = NumWaitingCust / self.num_customers
        UtilizationOfATM1 = sum(self.ServiceTime1) / self.ATM1[self.num_customers - 1]
        UtilizationOfATM2 = sum(self.ServiceTime2) / self.ATM2[self.num_customers - 1]
        AverageTIS = sum(self.TimeInSystem) / self.num_customers

        print("Average waiting time: ", AvgWaitingTime)
        print("Number of customers who had to wait: ", NumWaitingCust)
        print("The total time of the simulation: ", TotalSimTime)
        print("The probability that a customer will have to wait: ", ProbOfWaiting)
        print("Utilization of ATM1: ", UtilizationOfATM1)
        print("Utilization of ATM2: ", UtilizationOfATM2)
        print("Maximum number in the queue: ", self.maxInQueue)
        print("Average time in the system: ", AverageTIS)
        print()

        # Histogram for waiting time
        plt.hist(self.WaitingTime, bins=20, edgecolor='black')
        plt.title('Histogram of Waiting Time')
        plt.xlabel('Waiting Time (minutes)')
        plt.ylabel('Frequency')
        plt.show()

        # Print table
        num_elements = 15
        headers = ["Customer", "InterArrival Time", "Arrival Time", "Service Start Time", "Waiting Time",
                   "Service Time", "Completion Time", "Time In System", "ATM1", "ATM2"]
        data = list(
            zip(self.Customers[:num_elements], self.InterArrivalTime[:num_elements], self.ArrivalTime[:num_elements],
                self.StartTime[:15], self.WaitingTime[:num_elements],
                self.ServiceTime[:num_elements], self.CompletionTime[:num_elements], self.TimeInSystem[:num_elements],
                self.ATM1[:num_elements], self.ATM2[:num_elements]))
        table = tabulate(data, headers, tablefmt="fancy_grid")
        print(table)


atm_system = ATMSystem(num_customers=10000)
atm_system.simulate()
