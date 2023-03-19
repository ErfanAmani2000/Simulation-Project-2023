import random
import math
import pandas as pd
import numpy as np


class InsuranceCenterSimulation:

    def __init__(self, simulation_time):
        self.simulation_time = simulation_time
        self.sorted_fel = None
        self.current_event = None
        self.car = None
        self.future_event_list = list()
        self.data = dict()
        self.state = dict()
        self.day_state = "Normal"
        self.clock = 0
        self.paired = 0
        self.trace_list = []
        self.param = {'arrival_time': 2, 'Waiting in Parking': 30, 'Capacity': 40, 'N1': 2, 'N2': 3, 'N3': 2, 'N4': 1,
                      'LB': 5, 'M': 6, 'UB': 7, 'S2': 6, 'S3': 9, 'S4': 8, 'S6': 15, 'rain_probabilty': 0.1}
        # triangular dist. is for opening case, and S2: Picturing, S3: Assessment, S4: Finishing case, S6: Compliant 

    def data_def(self):
        self.data['Cars'] = dict()
        """ 
        Cars dictionary is implemented to track each car's entrance time, service time.
        """
        # The dictionary below is needed to store the last time for which each queue has changed in length.
        self.data['Last Time Queue Length Changed'] = dict()
        self.data['Last Time Queue Length Changed']['Taking Picture Queue'] = 0
        self.data['Last Time Queue Length Changed']['Opening Case Queue'] = 0
        self.data['Last Time Queue Length Changed']['Assessment Queue'] = 0
        self.data['Last Time Queue Length Changed']['Finishing Case Queue'] = 0
        self.data['Last Time Queue Length Changed']['Parking Lot Queue'] = 0
        self.data['Last Time Queue Length Changed']['Complaint Queue'] = 0
        self.data['Last Time Queue Length Changed']['Paired Car Queue'] = 0
        self.data['Last Time Queue Length Changed']['Outside the Area Queue'] = 0

        # The dictionary below is needed to store all Cars' data in each queue
        self.data['Queue Cars'] = dict()
        self.data['Queue Cars']['Taking Picture Queue'] = dict()
        self.data['Queue Cars']['Opening Case Queue'] = dict()
        self.data['Queue Cars']['Assessment Queue'] = dict()
        self.data['Queue Cars']['Finishing Case Queue'] = dict()
        self.data['Queue Cars']['Parking Lot Queue'] = dict()
        self.data['Queue Cars']['Complaint Queue'] = dict()
        self.data['Queue Cars']['Paired Car Queue'] = dict()
        self.data['Queue Cars']['Outside the Area Queue'] = dict()

        # The dictionary below is needed to store the last length of each queue.
        self.data['Last Queue Length'] = dict()
        self.data['Last Queue Length']['Taking Picture Queue'] = 0
        self.data['Last Queue Length']['Opening Case Queue'] = 0
        self.data['Last Queue Length']['Assessment Queue'] = 0
        self.data['Last Queue Length']['Finishing Case Queue'] = 0
        self.data['Last Queue Length']['Parking Lot Queue'] = 0
        self.data['Last Queue Length']['Complaint Queue'] = 0
        self.data['Last Queue Length']['Paired Car Queue'] = 0
        self.data['Last Queue Length']['Outside the Area Queue'] = 0

        # The dictionary below is needed to store the last time for which each server status has been changed.
        self.data['Last Time Server Status Changed'] = dict()
        self.data['Last Time Server Status Changed']['Picture Taker'] = 0
        self.data['Last Time Server Status Changed']['Filer'] = 0
        self.data['Last Time Server Status Changed']['Assesser'] = 0
        self.data['Last Time Server Status Changed']['Complaint'] = 0

        # The dictionary below is needed to store the last server status.
        self.data['Last Server Status'] = dict()
        self.data['Last Server Status']['Picture Taker'] = 0
        self.data['Last Server Status']['Filer'] = 0
        self.data['Last Server Status']['Assesser'] = 0
        self.data['Last Server Status']['Complaint'] = 0

        # The dictionary below is needed to store the maximum length of each queue during the simulation.
        self.data['Maximum Queue Length'] = dict()
        self.data['Maximum Queue Length']['Taking Picture Queue'] = 0
        self.data['Maximum Queue Length']['Opening Case Queue'] = 0
        self.data['Maximum Queue Length']['Assessment Queue'] = 0
        self.data['Maximum Queue Length']['Finishing Case Queue'] = 0
        self.data['Maximum Queue Length']['Parking Lot Queue'] = 0
        self.data['Maximum Queue Length']['Complaint Queue'] = 0
        self.data['Maximum Queue Length']['Paired Car Queue'] = 0
        self.data['Maximum Queue Length']['Outside the Area Queue'] = 0

        # The dictionary below is needed to store the maximum waiting time of Cars in each queue during the simulation.
        self.data['Maximum Waiting time'] = dict()
        self.data['Maximum Waiting time']['Taking Picture Queue'] = 0
        self.data['Maximum Waiting time']['Opening Case Queue'] = 0
        self.data['Maximum Waiting time']['Assessment Queue'] = 0
        self.data['Maximum Waiting time']['Finishing Case Queue'] = 0
        self.data['Maximum Waiting time']['Parking Lot Queue'] = 0
        self.data['Maximum Waiting time']['Complaint Queue'] = 0
        self.data['Maximum Waiting time']['Paired Car Queue'] = 0
        self.data['Maximum Waiting time']['Outside the Area Queue'] = 0

        # Cumulative statistics that are necessary to assess the system performance measures.
        self.data['Cumulative Stats'] = dict()
        self.data['Cumulative Stats']['Picture Taker'] = 0
        self.data['Cumulative Stats']['Filer'] = 0
        self.data['Cumulative Stats']['Assesser'] = 0
        self.data['Cumulative Stats']['Complaint'] = 0

        # This specific dictionary in cumulative stats is assigned to store area under each queue length curve.
        self.data['Cumulative Stats']['Area Under Queue Length Curve'] = dict()
        self.data['Cumulative Stats']['Area Under Queue Length Curve']['Taking Picture Queue'] = 0
        self.data['Cumulative Stats']['Area Under Queue Length Curve']['Opening Case Queue'] = 0
        self.data['Cumulative Stats']['Area Under Queue Length Curve']['Assessment Queue'] = 0
        self.data['Cumulative Stats']['Area Under Queue Length Curve']['Finishing Case Queue'] = 0
        self.data['Cumulative Stats']['Area Under Queue Length Curve']['Parking Lot Queue'] = 0
        self.data['Cumulative Stats']['Area Under Queue Length Curve']['Complaint Queue'] = 0
        self.data['Cumulative Stats']['Area Under Queue Length Curve']['Paired Car Queue'] = 0
        self.data['Cumulative Stats']['Area Under Queue Length Curve']['Outside the Area Queue'] = 0

        # This specific dictionary in cumulative stats is assigned to store area under waiting time for Cars in each queue.
        self.data['Cumulative Stats']['Area Under Waiting time'] = dict()
        self.data['Cumulative Stats']['Area Under Waiting time']['Taking Picture Queue'] = 0
        self.data['Cumulative Stats']['Area Under Waiting time']['Opening Case Queue'] = 0
        self.data['Cumulative Stats']['Area Under Waiting time']['Assessment Queue'] = 0
        self.data['Cumulative Stats']['Area Under Waiting time']['Finishing Case Queue'] = 0
        self.data['Cumulative Stats']['Area Under Waiting time']['Parking Lot Queue'] = 0
        self.data['Cumulative Stats']['Area Under Waiting time']['Complaint Queue'] = 0
        self.data['Cumulative Stats']['Area Under Waiting time']['Paired Car Queue'] = 0
        self.data['Cumulative Stats']['Area Under Waiting time']['Outside the Area Queue'] = 0

        # This specific dictionary in cumulative stats is assigned to store area under each server busy time.
        self.data['Cumulative Stats']['Area Under Server Busy time'] = dict()
        self.data['Cumulative Stats']['Area Under Server Busy time']['Picture Taker'] = 0
        self.data['Cumulative Stats']['Area Under Server Busy time']['Filer'] = 0
        self.data['Cumulative Stats']['Area Under Server Busy time']['Assesser'] = 0
        self.data['Cumulative Stats']['Area Under Server Busy time']['Complaint'] = 0

    def starting_state(self):
        # State variables declaration
        self.state['Taking Picture Queue'] = 0
        self.state['Opening Case Queue'] = 0
        self.state['Assessment Queue'] = 0
        self.state['Finishing Case Queue'] = 0
        self.state['Parking Lot Queue'] = 0
        self.state['Complaint Queue'] = 0
        self.state['Paired Car Queue'] = 0
        self.state['Outside the Area Queue'] = 0
        self.state['Picture Taker Server Status'] = 0
        self.state['Filer Server Status'] = 0
        self.state['Assessor Server Status'] = 0
        self.state['Complaint Server Status'] = 0

        # Data: will save every essential data
        self.data_def()

        # FEL initialization, and Starting events that initialize the simulation
        self.future_event_list.append({'Event Type': 'Car Entry Event', 'Event Time': 0, 'Car': [1, 0]})
        # number of car; guilty?
        return self.state, self.future_event_list, self.data

    @staticmethod
    def exponential(beta: float) -> float:
        """
        param lambda_param: mean parameter of exponential distribution
        return: random variate that conforms to exponential distribution
        """
        r = np.random.exponential(scale=beta)
        return r

    @staticmethod
    def triangular(LB: float, M: float, UB: float) -> float:
        r = np.random.triangular(left=LB, mode=M, right=UB)
        return r

    @staticmethod
    def uniform(a: float, b: float) -> float:
        """
        param a: lower bound for uniform dist.
        param b: upper bound for uniform dist.
        return: random variate that obey uniform dist.
        """
        r = random.random()
        return a + (b - a) * r

    @staticmethod
    def discrete_uniform(a: int, b: int) -> int:
        """
        param a: lower bound for discrete uniform dist.
        param b: upper bound for discrete uniform dist.
        return: random variate that obey discrete uniform dist.
        """
        r = random.random()
        for inc in range(a, b + 1):
            if (r < (inc + 1) / (b - a + 1)) and (r >= inc / (b - a + 1)):
                print(r)
                return inc

    def data_server_calculater(self, name: str):
        """
         This function is supposed to calculate area under each server busy time.
         param data: the dictionary that store every essential data
         param name: each server name, whether is expert, amateur or technical
         """
        self.data['Cumulative Stats']['Area Under Server Busy time'][name] += self.state[
                  '{} Server Status'.format(name)] * (self.clock - self.data['Last Time Server Status Changed'][name])
        self.data['Last Time Server Status Changed'][name] = self.clock

    def data_queue_calculater(self, name: str, temp=0):
        """
         This function is supposed to calculate area under each queue length curve,
         and also the maximum queue length.
         """
        self.data['Cumulative Stats']['Area Under Queue Length Curve']['{}'.format(name)] += (self.state[
            '{}'.format(name)]) * (self.clock - self.data['Last Time Queue Length Changed']['{}'.format(name)])
        self.data['Last Time Queue Length Changed']['{}'.format(name)] = self.clock
        self.data['Maximum Queue Length']['{}'.format(name)] = max(self.data['Maximum Queue Length']['{}'.format(name)],
                                                                   (self.state['{}'.format(name)]))

    def car_entry_event(self):
        self.data['Cars'][self.car[0]] = [self.clock, 0, 0, 1, 0,
                                          self.paired]  # Arrival time, Car Type, Has Complaint, Is Paired, Is complete case?, paired after calling pairing function?

        if (self.clock >= 1440 * math.floor(self.clock / 1440)) and (
                self.clock <= 1440 * math.floor(self.clock / 1440) + 600):
            self.paired = 0
            new_car = [self.car[0] + 1, 0]
            event_time = self.clock + self.exponential(self.param["arrival_time"])
            new_event = {'Event Type': 'Car Entry Event', 'Event Time': event_time, 'Car': new_car}
            self.future_event_list.append(new_event)

        if (random.random() < 0.3) and (self.data['Cars'][self.car[0]][5] == 0):
            self.data['Cars'][self.car[0]][3] = 0

            if self.state['Outside the Area Queue'] > 0:
                self.data['Last Queue Length']['Outside the Area Queue'] = self.state['Outside the Area Queue']
                self.state['Outside the Area Queue'] += 1
                self.data['Queue Cars']['Outside the Area Queue'][self.car[0]] = [self.clock, 0]
                self.data_queue_calculater('Outside the Area Queue')
            else:
                self.data['Last Queue Length']['Parking Lot Queue'] = self.state['Parking Lot Queue']
                self.state['Parking Lot Queue'] += 1
                self.data['Queue Cars']['Parking Lot Queue'][self.car[0]] = [self.clock, 0]
                self.data_queue_calculater('Parking Lot Queue')

                event_time = self.clock + self.exponential(self.param['Waiting in Parking'])
                new_event = {'Event Type': 'Pairing Car', 'Event Time': event_time, 'Car': [self.car[0], 0]}
                self.future_event_list.append(new_event)
        else:
            if self.state['Outside the Area Queue'] > 0:
                self.data['Last Queue Length']['Outside the Area Queue'] = self.state['Outside the Area Queue']
                self.state['Outside the Area Queue'] += 2
                self.data['Queue Cars']['Outside the Area Queue'][self.car[0]] = [self.clock, 0]
                self.data_queue_calculater('Outside the Area Queue')
            else:
                if self.state['Taking Picture Queue'] < self.param['Capacity']:
                    if self.state['Paired Car Queue'] > 0:
                        self.data['Last Queue Length']['Paired Car Queue'] = self.state['Paired Car Queue']
                        self.state['Paired Car Queue'] -= 2
                        first_car_in_queue = min(self.data['Queue Cars']['Paired Car Queue'],
                                                 key=self.data['Queue Cars']['Paired Car Queue'].get)
                        self.data['Queue Cars']['Paired Car Queue'].pop(first_car_in_queue, None)
                        self.data_queue_calculater('Paired Car Queue')

                        if self.state['Picture Taker Server Status'] == self.param['N1']:
                            self.data['Last Queue Length']['Taking Picture Queue'] = self.state['Taking Picture Queue']
                            self.state['Taking Picture Queue'] += 2
                            self.data['Queue Cars']['Taking Picture Queue'][first_car_in_queue] = [self.clock, 0]
                            self.data_queue_calculater('Taking Picture Queue')
                        else:
                            self.data['Last Server Status']['Picture Taker'] = self.state['Picture Taker Server Status']
                            self.data_server_calculater('Picture Taker')
                            self.state['Picture Taker Server Status'] += 1

                            event_time = self.clock + self.exponential(self.param['S2'])
                            new_event = {'Event Type': 'Filing Entrance Event', 'Event Time': event_time,
                                         'Car': [first_car_in_queue, 1]}
                            self.future_event_list.append(new_event)
                    else:
                        if self.state['Picture Taker Server Status'] == self.param['N1']:
                            self.data['Last Queue Length']['Taking Picture Queue'] = self.state['Taking Picture Queue']
                            self.state['Taking Picture Queue'] += 2
                            self.data['Queue Cars']['Taking Picture Queue'][self.car[0]] = [self.clock, 0]
                            self.data_queue_calculater('Taking Picture Queue')
                        else:
                            self.data['Last Server Status']['Picture Taker'] = self.state['Picture Taker Server Status']
                            self.data_server_calculater('Picture Taker')
                            self.state['Picture Taker Server Status'] += 1

                            event_time = self.clock + self.exponential(self.param['S2'])
                            new_event = {'Event Type': 'Filing Entrance Event', 'Event Time': event_time,
                                         'Car': [self.car[0], 1]}
                            self.future_event_list.append(new_event)
                else:
                    self.data['Last Queue Length']['Outside the Area Queue'] = self.state['Outside the Area Queue']
                    self.state['Outside the Area Queue'] += 2
                    self.data['Queue Cars']['Outside the Area Queue'][self.car[0]] = [self.clock, 0]
                    self.data_queue_calculater('Outside the Area Queue')

    def pairing_Cars(self):
        self.paired = 1
        first_car_in_queue = min(self.data['Queue Cars']['Parking Lot Queue'],
                                 key=self.data['Queue Cars']['Parking Lot Queue'].get)
        self.data['Cars'][first_car_in_queue][3] = 1

        self.data['Last Queue Length']['Parking Lot Queue'] = self.state['Parking Lot Queue']
        self.state['Parking Lot Queue'] -= 1
        self.data['Queue Cars']['Parking Lot Queue'].pop(first_car_in_queue, None)
        self.data_queue_calculater('Parking Lot Queue')

        if self.state['Taking Picture Queue'] < self.param['Capacity']:
            if self.state['Picture Taker Server Status'] == self.param['N1']:
                self.data['Last Queue Length']['Taking Picture Queue'] = self.state['Taking Picture Queue']
                self.state['Taking Picture Queue'] += 2
                self.data['Queue Cars']['Taking Picture Queue'][first_car_in_queue] = [self.clock, 0]
                self.data_queue_calculater('Taking Picture Queue')
            else:
                self.data['Last Server Status']['Picture Taker'] = self.state['Picture Taker Server Status']
                self.data_server_calculater('Picture Taker')
                self.state['Picture Taker Server Status'] += 1

                event_time = self.clock + self.exponential(self.param['S2'])
                new_event = {'Event Type': 'Filing Entrance Event', 'Event Time': event_time,
                             'Car': [first_car_in_queue, 1]}
                self.future_event_list.append(new_event)
        else:
            self.data['Last Queue Length']['Paired Car Queue'] = self.state['Paired Car Queue']
            self.state['Paired Car Queue'] += 2
            self.data['Queue Cars']['Paired Car Queue'][first_car_in_queue] = [self.clock, 0]
            self.data_queue_calculater('Paired Car Queue')

    def filing_entrance_event(self):
        if self.data['Cars'][self.car[0]][4] == 1:
            self.state['Assesser Server Status'] -= 1
            self.data['Last Server Status']['Assesser'] = self.state['Assesser Server Status']
            self.data_server_calculater('Assesser')

            if self.state['Assessment Queue'] > 0:
                self.data['Last Queue Length']['Assessment Queue'] = self.state['Assessment Queue']
                self.state['Assessment Queue'] -= 2
                first_car_in_queue = min(self.data['Queue Cars']['Assessment Queue'],
                                         key=self.data['Queue Cars']['Assessment Queue'].get)
                self.data['Queue Cars']['Assessment Queue'].pop(first_car_in_queue, None)
                self.data_queue_calculater('Assessment Queue')

                self.data['Last Server Status']['Assesser'] = self.state['Assesser Server Status']
                self.data_server_calculater('Assesser')
                self.state['Assesser Server Status'] += 1

                if (random.random() <= 0.1) and (self.data['Cars'][first_car_in_queue][2] == 0):
                    self.data['Cars'][first_car_in_queue][2] = 1
                    event_time = self.clock + self.exponential(self.param["S3"])
                    new_event = {'Event Type': 'Complaint Entrance Event', 'Event Time': event_time,
                                 'Car': [first_car_in_queue, 1]}
                    self.future_event_list.append(new_event)
                else:
                    self.data['Cars'][first_car_in_queue][4] = 1
                    event_time = self.clock + self.exponential(self.param["S3"])
                    new_event = {'Event Type': 'Filing Entrance Event', 'Event Time': event_time,
                                 'Car': [first_car_in_queue, 1]}
                    self.future_event_list.append(new_event)

            if self.state['Filer Server Status'] == self.param["N2"]:
                self.data['Last Queue Length']['Finishing Case Queue'] = self.state['Finishing Case Queue']
                self.state['Finishing Case Queue'] += 2
                self.data['Queue Cars']['Finishing Case Queue'][self.car[0]] = [self.clock, 0]
                self.data_queue_calculater('Finishing Case Queue')
            else:
                self.data['Last Server Status']['Filer'] = self.state['Filer Server Status']
                self.data_server_calculater('Filer')
                self.state['Filer Server Status'] += 1

                event_time = self.clock + self.exponential(self.param["S4"])
                new_event = {'Event Type': 'Exit From System', 'Event Time': event_time, 'Car': [self.car[0], 1]}
                self.future_event_list.append(new_event)
        else:
            self.state['Picture Taker Server Status'] -= 1
            self.data['Last Server Status']['Picture Taker'] = self.state['Picture Taker Server Status']
            self.data_server_calculater('Picture Taker')

            if self.state['Taking Picture Queue'] > 0:
                self.data['Last Queue Length']['Taking Picture Queue'] = self.state['Taking Picture Queue']
                self.state['Taking Picture Queue'] -= 2
                first_car_in_queue = min(self.data['Queue Cars']['Taking Picture Queue'],
                                         key=self.data['Queue Cars']['Taking Picture Queue'].get)
                self.data['Queue Cars']['Taking Picture Queue'].pop(first_car_in_queue, None)
                self.data_queue_calculater('Taking Picture Queue')

                self.data['Last Server Status']['Picture Taker'] = self.state['Picture Taker Server Status']
                self.data_server_calculater('Picture Taker')
                self.state['Picture Taker Server Status'] += 1

                self.data['Cars'][first_car_in_queue][4] = 0
                event_time = self.clock + self.exponential(self.param['S2'])
                new_event = {'Event Type': 'Filing Entrance Event', 'Event Time': event_time,
                             'Car': [first_car_in_queue, 1]}
                self.future_event_list.append(new_event)

                if self.state['Paired Car Queue'] > 0:
                    self.data['Last Queue Length']['Paired Car Queue'] = self.state['Paired Car Queue']
                    self.state['Paired Car Queue'] -= 2
                    first_car_in_queue = min(self.data['Queue Cars']['Paired Car Queue'],
                                             key=self.data['Queue Cars']['Paired Car Queue'].get)
                    self.data['Queue Cars']['Paired Car Queue'].pop(first_car_in_queue, None)
                    self.data_queue_calculater('Paired Car Queue')

                    self.data['Last Queue Length']['Taking Picture Queue'] = self.state['Taking Picture Queue']
                    self.state['Taking Picture Queue'] += 2
                    self.data['Queue Cars']['Taking Picture Queue'][first_car_in_queue] = [self.clock, 0]
                    self.data_queue_calculater('Taking Picture Queue')
                else:
                    if self.state['Outside the Area Queue'] > 0:
                        first_car_in_queue = min(self.data['Queue Cars']['Outside the Area Queue'],
                                                 key=self.data['Queue Cars']['Outside the Area Queue'].get)
                        if self.data['Cars'][first_car_in_queue][3] == 1:
                            self.data['Last Queue Length']['Outside the Area Queue'] = self.state[
                                'Outside the Area Queue']
                            self.state['Outside the Area Queue'] -= 2
                            self.data['Queue Cars']['Outside the Area Queue'].pop(first_car_in_queue, None)
                            self.data_queue_calculater('Outside the Area Queue')

                            self.data['Last Queue Length']['Taking Picture Queue'] = self.state['Taking Picture Queue']
                            self.state['Taking Picture Queue'] += 2
                            self.data['Queue Cars']['Taking Picture Queue'][first_car_in_queue] = [self.clock, 0]
                            self.data_queue_calculater('Taking Picture Queue')
                        else:
                            self.data['Last Queue Length']['Outside the Area Queue'] = self.state[
                                'Outside the Area Queue']
                            self.state['Outside the Area Queue'] -= 1
                            self.data['Queue Cars']['Outside the Area Queue'].pop(first_car_in_queue, None)
                            self.data_queue_calculater('Outside the Area Queue')

                            self.data['Last Queue Length']['Parking Lot Queue'] = self.state['Parking Lot Queue']
                            self.state['Parking Lot Queue'] += 1
                            self.data['Queue Cars']['Parking Lot Queue'][first_car_in_queue] = [self.clock, 0]
                            self.data_queue_calculater('Parking Lot Queue')

                            event_time = self.clock + self.exponential(self.param['Waiting in Parking'])
                            new_event = {'Event Type': 'Pairing Car', 'Event Time': event_time,
                                         'Car': [first_car_in_queue, 0]}
                            self.future_event_list.append(new_event)

            if self.state['Finishing Case Queue'] > 0:
                if self.state['Filer Server Status'] == self.param["N2"]:
                    self.data['Last Queue Length']['Opening Case Queue'] = self.state['Opening Case Queue']
                    self.state['Opening Case Queue'] += 2
                    self.data['Queue Cars']['Opening Case Queue'][self.car[0]] = [self.clock, 0]
                    self.data_queue_calculater('Opening Case Queue')
                else:
                    self.data['Last Server Status']['Filer'] = self.state['Filer Server Status']
                    self.data_server_calculater('Filer')
                    self.state['Filer Server Status'] += 1

                    event_time = self.clock + self.exponential(self.param["S4"])
                    new_event = {'Event Type': 'Exit From System', 'Event Time': event_time, 'Car': [self.car[0], 1]}
                    self.future_event_list.append(new_event)
            else:
                if self.state['Filer Server Status'] == self.param["N2"]:
                    self.data['Last Queue Length']['Opening Case Queue'] = self.state['Opening Case Queue']
                    self.state['Opening Case Queue'] += 2
                    self.data['Queue Cars']['Opening Case Queue'][self.car[0]] = [self.clock, 0]
                    self.data_queue_calculater('Opening Case Queue')
                else:
                    self.data['Last Server Status']['Filer'] = self.state['Filer Server Status']
                    self.data_server_calculater('Filer')
                    self.state['Filer Server Status'] += 1

                    event_time = self.clock + self.triangular(LB=self.param['LB'], M=self.param['M'],
                                                              UB=self.param['UB'])
                    new_event = {'Event Type': 'Assessment Entrance Event', 'Event Time': event_time,
                                 'Car': [self.car[0], 1]}
                    self.future_event_list.append(new_event)

    def Assessment_entrance_event(self):
        if self.data['Cars'][self.car[0]][2] == 0:
            self.state['Filer Server Status'] -= 1
            self.data['Last Server Status']['Filer'] = self.state['Filer Server Status']
            self.data_server_calculater('Filer')

            if self.state['Finishing Case Queue'] > 0:
                self.data['Last Queue Length']['Finishing Case Queue'] = self.state['Finishing Case Queue']
                self.state['Finishing Case Queue'] -= 2
                first_car_in_queue = min(self.data['Queue Cars']['Finishing Case Queue'],
                                         key=self.data['Queue Cars']['Finishing Case Queue'].get)
                self.data['Queue Cars']['Finishing Case Queue'].pop(first_car_in_queue, None)
                self.data_queue_calculater('Finishing Case Queue')
            else:
                if self.state['Opening Case Queue'] > 0:
                    self.data['Last Queue Length']['Opening Case Queue'] = self.state['Opening Case Queue']
                    self.state['Opening Case Queue'] -= 2
                    first_car_in_queue = min(self.data['Queue Cars']['Opening Case Queue'],
                                             key=self.data['Queue Cars']['Opening Case Queue'].get)
                    self.data['Queue Cars']['Opening Case Queue'].pop(first_car_in_queue, None)
                    self.data_queue_calculater('Opening Case Queue')

            if self.state['Assesser Server Status'] == self.param["N3"]:
                self.data['Last Queue Length']['Assessment Queue'] = self.state['Assessment Queue']
                self.state['Assessment Queue'] += 2
                self.data['Queue Cars']['Assessment Queue'][self.car[0]] = [self.clock, 0]
                self.data_queue_calculater('Assessment Queue')
            else:
                self.data['Last Server Status']['Filer'] = self.state['Assesser Server Status']
                self.data_server_calculater('Assesser')
                self.state['Assesser Server Status'] += 1

                if random.random() <= 0.1:
                    self.data['Cars'][self.car[0]][2] = 1
                    event_time = self.clock + self.exponential(self.param["S3"])
                    new_event = {'Event Type': 'Complaint Entrance Event', 'Event Time': event_time,
                                 'Car': [self.car[0], 1]}
                    self.future_event_list.append(new_event)
                else:
                    self.data['Cars'][self.car[0]][4] = 1
                    event_time = self.clock + self.exponential(self.param["S3"])
                    new_event = {'Event Type': 'Filing Entrance Event', 'Event Time': event_time,
                                 'Car': [self.car[0], 1]}
                    self.future_event_list.append(new_event)

        else:
            self.state['Complaint Server Status'] -= 1
            self.data['Last Server Status']['Complaint'] = self.state['Complaint Server Status']
            self.data_server_calculater('Complaint')

            if self.state['Complaint Queue'] > 0:
                self.data['Last Queue Length']['Complaint Queue'] = self.state['Complaint Queue']
                self.state['Complaint Queue'] -= 2
                first_car_in_queue = min(self.data['Queue Cars']['Complaint Queue'],
                                         key=self.data['Queue Cars']['Complaint Queue'].get)
                self.data['Queue Cars']['Complaint Queue'].pop(first_car_in_queue, None)
                self.data_queue_calculater('Complaint Queue')

            if self.state['Assesser Server Status'] == self.param["N3"]:
                self.data['Last Queue Length']['Assessment Queue'] = self.state['Assessment Queue']
                self.state['Assessment Queue'] += 2
                self.data['Queue Cars']['Assessment Queue'][self.car[0]] = [self.clock, 0]
                self.data_queue_calculater('Assessment Queue')
            else:
                self.data['Last Server Status']['Filer'] = self.state['Assesser Server Status']
                self.data_server_calculater('Assesser')
                self.state['Assesser Server Status'] += 1

                self.data['Cars'][self.car[0]][4] = 1
                event_time = self.clock + self.exponential(self.param["S3"])
                new_event = {'Event Type': 'Filing Entrance Event', 'Event Time': event_time, 'Car': [self.car[0], 1]}
                self.future_event_list.append(new_event)

    def complaint_entrance_event(self):
        self.data['Last Server Status']['Assesser'] = self.state['Assesser Server Status']
        self.data_server_calculater('Assesser')
        self.state['Assesser Server Status'] -= 1

        if self.state['Assessment Queue'] > 0:
            self.data['Last Queue Length']['Assessment Queue'] = self.state['Assessment Queue']
            self.state['Assessment Queue'] -= 2
            first_car_in_queue = min(self.data['Queue Cars']['Assessment Queue'],
                                     key=self.data['Queue Cars']['Assessment Queue'].get)
            self.data['Queue Cars']['Assessment Queue'].pop(first_car_in_queue, None)
            self.data_queue_calculater('Assessment Queue')

            self.data['Last Server Status']['Assesser'] = self.state['Assesser Server Status']
            self.data_server_calculater('Assesser')
            self.state['Assesser Server Status'] += 1

            if (random.random() <= 0.1) and (self.data['Cars'][first_car_in_queue][2] == 0):
                self.data['Cars'][first_car_in_queue][2] = 1
                event_time = self.clock + self.exponential(self.param["S3"])
                new_event = {'Event Type': 'Complaint Entrance Event', 'Event Time': event_time,
                             'Car': [first_car_in_queue, 1]}
                self.future_event_list.append(new_event)
            else:
                self.data['Cars'][first_car_in_queue][4] = 1
                event_time = self.clock + self.exponential(self.param["S3"])
                new_event = {'Event Type': 'Filing Entrance Event', 'Event Time': event_time,
                             'Car': [first_car_in_queue, 1]}
                self.future_event_list.append(new_event)

        if self.state['Complaint Server Status'] == self.param["N4"]:
            self.data['Last Queue Length']['Complaint Queue'] = self.state['Complaint Queue']
            self.state['Complaint Queue'] += 2
            self.data['Queue Cars']['Complaint Queue'][self.car[0]] = [self.clock, 0]
            self.data_queue_calculater('Complaint Queue')
        else:
            self.data['Last Server Status']['Complaint'] = self.state['Complaint Server Status']
            self.data_server_calculater('Complaint')
            self.state['Complaint Server Status'] += 1

            event_time = self.clock + self.exponential(self.param["S6"])
            new_event = {'Event Type': 'Assessment Entrance Event', 'Event Time': event_time, 'Car': [self.car[0], 1]}
            self.future_event_list.append(new_event)

    def check_day_state(self):
        day_number = math.floor(self.clock / 1440) + 1
        probabilty_of_rain = random.random()
        if probabilty_of_rain >= self.param["rain_probabilty"][day_number]:
            self.param['arrival_time'] = 1.5
        else:
            self.param['arrival_time'] = 2

    def exit_system(self):
        self.data['Last Server Status']['Filer'] = self.state['Filer Server Status']
        self.data_server_calculater('Filer')
        self.state['Filer Server Status'] -= 1

        if self.state['Finishing Case Queue'] > 0:
            self.data['Last Queue Length']['Finishing Case Queue'] = self.state['Finishing Case Queue']
            self.state['Finishing Case Queue'] -= 2
            first_car_in_queue = min(self.data['Queue Cars']['Finishing Case Queue'],
                                     key=self.data['Queue Cars']['Finishing Case Queue'].get)
            self.data['Queue Cars']['Finishing Case Queue'].pop(first_car_in_queue, None)
            self.data_queue_calculater('Finishing Case Queue')

            self.data['Cars'][first_car_in_queue][4] == 1
            self.data['Last Server Status']['Filer'] = self.state['Filer Server Status']
            self.data_server_calculater('Filer')
            self.state['Filer Server Status'] += 1

            event_time = self.clock + self.exponential(self.param["S4"])
            new_event = {'Event Type': 'Exit From System', 'Event Time': event_time, 'Car': [first_car_in_queue, 1]}
            self.future_event_list.append(new_event)

        else:
            if self.state['Opening Case Queue'] > 0:
                self.data['Last Queue Length']['Opening Case Queue'] = self.state['Opening Case Queue']
                self.state['Opening Case Queue'] -= 2
                first_car_in_queue = min(self.data['Queue Cars']['Opening Case Queue'],
                                         key=self.data['Queue Cars']['Opening Case Queue'].get)
                self.data['Queue Cars']['Opening Case Queue'].pop(first_car_in_queue, None)
                self.data_queue_calculater('Opening Case Queue')

                self.data['Cars'][first_car_in_queue][4] == 0
                self.data['Last Server Status']['Filer'] = self.state['Filer Server Status']
                self.data_server_calculater('Filer')
                self.state['Filer Server Status'] += 1

                event_time = self.clock + self.triangular(LB=self.param['LB'], M=self.param['M'], UB=self.param['UB'])
                new_event = {'Event Type': 'Assessment Entrance Event', 'Event Time': event_time,
                             'Car': [first_car_in_queue, 1]}
                self.future_event_list.append(new_event)

    def simulation(self, trace_creator=False) -> dict:
        """
        This function is meant to do the simulation by help of introduced events.
        return: data and state dictionary will be returned after one replication is done.
        """

        self.starting_state()

        while self.clock < self.simulation_time:
            self.sorted_fel = sorted(self.future_event_list, key=lambda x: x['Event Time'])
            try:
                self.current_event = self.sorted_fel[0]  # find imminent event
            except IndexError:
                self.clock = 1440 * math.floor(self.clock / 1440) + 1440
                event_time = self.clock + self.exponential(self.param["arrival_time"])
                if random.random() <= 0.3:
                    new_event = {'Event Type': 'Car Entry Event', 'Event Time': event_time, 'Car': [self.car[0] + 1, 0]}
                else:
                    new_event = {'Event Type': 'Car Entry Event', 'Event Time': event_time, 'Car': [self.car[0] + 1, 1]}
                self.future_event_list.append(new_event)
                continue
            self.clock = self.current_event['Event Time']  # advance time to current event time
            self.car = self.current_event['Car']  # find the car of that event

            if self.clock < self.simulation_time:  # the if block below is ganna call proper event function for that event type
                if self.current_event['Event Type'] == 'Car Entry Event':
                    self.car_entry_event()

                elif self.current_event['Event Type'] == 'Assessment Entrance Event':
                    self.Assessment_entrance_event()

                elif self.current_event['Event Type'] == 'Filing Entrance Event':
                    self.filing_entrance_event()

                elif self.current_event['Event Type'] == 'Complaint Entrance Event':
                    self.complaint_entrance_event()

                elif self.current_event['Event Type'] == 'Pairing Car':
                    self.pairing_Cars()

                elif self.current_event['Event Type'] == 'Exit From System':
                    self.exit_system()

                elif self.current_event['Event Type'] == 'Change Day Event':
                    self.change_day_event()

                self.future_event_list.remove(self.current_event)

            else:  # if simulation time is passed after simulation end time, so FEL must be cleared
                self.future_event_list.clear()

            if trace_creator:  # This code block is supposed to create trace for each current event and append it to the trace list
                trace_data = list(self.state.values())
                trace_data.insert(0, round(self.clock, 3))
                trace_data.insert(0, self.current_event)
                fel_copy = self.sorted_fel.copy()

                while len(fel_copy) > 0:  # Filling trace with events of future event list
                    trace_data.append(list(filter(None, fel_copy.pop(0).values())))
                self.trace_list.append(trace_data)

        return self.data, self.state, self.trace_list

    def trace_excel_maker(self):
        """
        This function is only meant to create a trace excel
        """
        self.simulation(trace_creator=True)
        trace = pd.DataFrame(self.trace_list)

        columns = list(self.state.keys())  # list of excel columns headers
        columns.insert(0, 'Clock')
        columns.insert(1, 'Current Event')
        columns.extend(
            [f'fel{i}' for i in range(1, trace.shape[1] - 13)])  # to add future event list to trace dataframe
        trace = pd.DataFrame(self.trace_list, columns=columns)
        trace.to_excel('C:/Users/Lenovo/Desktop/trace_dataframe.xlsx', engine='xlsxwriter')


## %%
ICS = InsuranceCenterSimulation(simulation_time=43300)
data, state, tr = ICS.simulation(trace_creator=True)
ICS.trace_excel_maker()
