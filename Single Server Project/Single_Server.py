import numpy as np
from math import inf

from Classes.class_Queue import Queue
from Classes.class_Customer import Customer
from Functions.Display_func import *
from Functions.Export_func import *
from Functions.Snapshot_func import create_snapshots_table
from Functions.Plot_func import *

class Single_Server_Queueing_System:
    def __init__(self, inter_arrival_times, arrival_times, service_times, Tn=None):
        self.Q = Queue(5)                           # capacity of queue is 5
        self.Customers = []                         # list of Customers (obj)
        self.discarded_entities = []                # list of discarded arrivals
        self.Tn = Tn                                # stores the value of Tn (desired end time) if given

        # system state
        self.clock = 0
        self.server_status = 0

        # Statistical Counters
        self.total_area_Qt = 0
        self.total_area_Bt = 0
        self.total_delays = 0
        self.total_idles = 0

        # Other Counters for number of customers
        self.total_served = 0
        self.total_waited = 0

        # LISTS of generated (IAT, AT, ST) / server idle times
        self.g_inter_arrival_times = inter_arrival_times
        self.g_service_times = service_times
        self.g_arrival_times = arrival_times
        self.idle_times = []

        # LISTS of Event--related matters
        self.events = []                            # list of events (time, type, customer #)
        self.future_events = []                     # list of future events (next_A, next_D) per event
        self.q_arrivals_list = []                   # list of customer arrivals in queue per event time
        self.discarded_list = []                    # list of discarded arrivals per event
        self.discarded_CNum_list = []               # list of discarded C# per event
        self.num_delay_list = []                    # list of number of customer delays (cumulative) per event time
        self.delay_time_list = []                   # list of delay time per event time
        self.total_delay_event_list = []            # list of total delay time (cumulative) per event time

        # LISTS of Server/Queue--related matters
        self.Bt_values = []                         # list of Server status per event time
        self.Qt_values = []                         # list of Queue size per event time
        self.customer_server_list = []              # list of customer currently being served per event time
        self.customers_queue_list = []              # list of customers currently waiting per event time
        self.total_area_Qt_list = []                # list of total area Q(t) per event time
        self.total_area_Bt_list = []                # list of total area B(t) per event time

        # used when specific end time is given
        self.extended_time = 0                      # departure(prev_customer) - Tn (if Tn is given)
        self.total_unserved = 0                     # no. of unserved customers in queue after Tn

    def run_simulation(self):
        # initialization
        n_A = 0                               # number of arrivals
        next_A = self.g_arrival_times[n_A]    # initial arrival time
        service = self.g_service_times[n_A]         # initial service time
        next_D = inf                          # initial departure time
        current_customer = 0
        total_delay_per_event = 0
        discarded_CNum = []

        server = "operating"                  # will be updated if there's an indicated Tn (simulation end time)

        while True:
            prev_clock = self.clock
            delay_per_event = 0

            # Timing Routine
            next_event = min(next_A, next_D)
            self.clock = next_event

            # Checking Tn (desired simulation end time if given)
            if self.Tn is not None:
                if next_event >= self.Tn:
                    if next_event == next_A or server == "done":
                        break
                    else:
                        # finish serving the current customer at the server before ending
                        self.extended_time = round(next_D - self.Tn, 2)
                        self.total_unserved = self.Q.size
                        server = "done"

            # Event Routine
            if next_event == inf:    # no arrival / no departure
                break
            elif next_event == next_A and next_A != next_D:
                n_A += 1
                self.events.append((self.clock, 'Arrival', n_A))

                # check the server's status
                if self.server_status == 0:
                    current_customer = n_A
                    next_D = self.server_process(next_A, service)

                else:
                    if not self.Q.is_Full():
                        self.Q.enqueue(next_A, service, n_A)
                        self.total_waited += 1
                    else:
                        self.discarded_entities.append(next_A)
                        discarded_CNum.append(n_A)

            elif next_event == next_D:
                self.events.append((self.clock, 'Departure', current_customer))
                self.total_served += 1

                if self.Q.size > 0 and server == "operating":
                    # process the first customer in line
                    A, service, current_customer = self.Q.dequeue()
                    next_D = self.server_process(A, service)
                    delay_per_event = round(self.clock - A, 2)
                    total_delay_per_event += delay_per_event
                else:
                    self.server_status = 0
                    current_customer = 0
                    next_D = inf


            # per event
            self.calc_area_Bt_Qt(prev_clock)
            self.update_event_details(current_customer, delay_per_event, total_delay_per_event, discarded_CNum)


            # updating next arrival / future event list
            next_A = self.g_arrival_times[n_A] if n_A != len(self.g_arrival_times) else inf
            service = self.g_service_times[n_A] if next_A != inf else 0
            self.future_events.append(f"[A: {next_A}, D: {next_D}]")


    def server_process(self, arrival, service):

        self.server_status = 1
        service_start_time = self.clock
        wait_time = max(0, service_start_time - arrival)
        next_D = round(service_start_time + service, 2)

        self.total_delays += wait_time
        self.update_server_idles(arrival)
        self.create_customer(arrival, service, self.clock, next_D, wait_time)

        return next_D

    def update_server_idles(self, arrival):
        if len(self.Customers) > 0:
            prev_customer = self.Customers[-1]
            server_idle_time = max(0, arrival - prev_customer.departure_time)
        else:
            server_idle_time = arrival

        self.idle_times.append(server_idle_time)
        self.total_idles += server_idle_time

    def calc_area_Bt_Qt(self, prev_clock):
        dt = self.clock - prev_clock

        if prev_clock == 0:
            Qt = Bt = 0
        else:
            Qt = self.Qt_values[-1]
            Bt = self.Bt_values[-1]

        # calculation
        self.total_area_Qt += Qt * dt
        self.total_area_Bt += Bt * dt

        # storing the results
        self.total_area_Qt_list.append(round(self.total_area_Qt, 2))
        self.total_area_Bt_list.append(round(self.total_area_Bt, 2))

    def update_event_details(self, customer_server, delay_per_event, total_delay_per_event, discarded_CNum):
        # for Numerical values (Bt & Qt)
        self.Bt_values.append(self.server_status)
        self.Qt_values.append(self.Q.size)

        # for Descriptive values (Bt & Qt)
        self.customer_server_list.append(customer_server)
        self.customers_queue_list.append(self.Q.customer_nums.copy())

        # for snapshots
        self.q_arrivals_list.append(self.Q.arrivals.copy())
        self.num_delay_list.append(self.total_waited)
        self.delay_time_list.append((round(delay_per_event, 2)))
        self.total_delay_event_list.append(round(total_delay_per_event, 2))
        self.discarded_list.append(self.discarded_entities.copy())
        self.discarded_CNum_list.append(discarded_CNum.copy())

    def create_customer(self, arrival, service, service_start, departure, wait):
        newCustomer = Customer(arrival, service, wait, service_start, departure)
        self.Customers.append(newCustomer)


    # PRINTING / EXPORTING DISPLAY
    def get_outputs(self, test_name, run_name):
        #display_outputs(self, test_name, run_name)

        # Exporting Simulation Details to various files
        export_output_screen(self, f'Outputs/{test_name}/{test_name}_3runs_Statistics.txt', test_name, run_name)
        export_simulation_details(self, f'Outputs/{test_name}/Simulation_Data/{test_name}-{run_name}_simulation_data.xlsx')
        export_snapshots_table(create_snapshots_table(self), f'Outputs/{test_name}/Snapshots/{test_name}-{run_name}_snapshots_data.txt')
        export_customer_simulation_data(self, f'Outputs/{test_name}/Customer_Data/{test_name}-{run_name}_customer_data.txt')

    # PLOTTING RESULTS
    def plot(self):
        plot_graph(self)


    # CALCULATIONS (Statistics)
    def calc_avg_delay(self):
        return round(self.total_delays / self.total_served, 2)

    def calc_qn(self):
        Tn = self.events[-1][0]
        return round(self.total_area_Qt / Tn, 2)

    def calc_utilization(self):
        Tn = self.events[-1][0]
        return round(self.total_area_Bt / Tn, 2)

    def get_total_discarded(self):
        return len(self.discarded_entities)

    def get_mean_waiting_time(self):
        return round(self.total_delays / self.total_served, 2)

    def get_mean_idle_time(self):
        return round(self.total_idles / self.total_served, 2)

    def get_avg_time_spent_in_system(self):
        total_time_spent = 0
        for customer in self.Customers:
            total_time_spent += customer.time_spent_in_system
        return round(total_time_spent / self.total_served, 2)

    def calc_prob_C_wait(self):
        total_customer_waited = 0            # total of customer who has a waiting time
        for customer in self.Customers:
            total_customer_waited += (1 if customer.waiting_time > 0 else 0)
        return round(total_customer_waited / self.total_served, 2)

    def calc_prob_Idle_server(self):
        Tn = self.events[-1][0]
        return round(self.total_idles / Tn, 2)






