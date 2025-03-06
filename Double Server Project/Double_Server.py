from math import inf

from Classes.Customer import Customer
from Classes.Queue import Queue
from Functions.Display import *
from Functions.Export import *
from Functions.Snapshot import *
from Functions.Plot import *

class Double_Server_Queueing_System:
    def __init__(self, inter_arrival_times, arrival_times, service_times):
        self.Q = Queue(5)                          # capacity of queue line is set to 5
        self.Customers = []                        # list of Customers (obj)
        self.discarded_entities = []               # list of discarded arrivals
        self.discarded_CNums = []                  # list of discarded C#

        # system state
        self.clock = 0
        self.s1_status = 0
        self.s2_status = 0
        self.server_used = []

        # Statistical Counters
        self.total_area_Qt = 0
        self.total_area_Bt1 = 0
        self.total_area_Bt2 = 0
        self.total_delays = 0

        # Other Counters
        self.total_waited = 0                      # total no. of customer who waited in queue
        self.total_served = 0                      # total no. of customer who got served
        self.total_s1_service = 0                  # total service time of server 1
        self.total_s2_service = 0                  # total service time of server 2
        self.total_s1_idles = 0
        self.total_s2_idles = 0
        self.total_discarded = 0

        # LISTS of generated (IAT, AT, ST)
        self.g_inter_arrival_times = inter_arrival_times
        self.g_service_times = service_times
        self.g_arrival_times = arrival_times

        # LISTS of Servers' Idle Times
        self.total_s1_idle_times = []
        self.total_s2_idle_times = []

        # LISTS of Event--related matters
        self.events = []
        self.future_event_list = []
        self.q_arrival_list = []                   # customer arrivals in queue per event time
        self.num_delay_list = []                   # number of delays (cumulative) per event time
        self.delay_time_list = []                  # list of delay time per event time
        self.total_delay_event_list = []           # total delay (cumulative) per event time
        self.discarded_arrivals_list = []          # list of discarded arrivals per event time
        self.discarded_CNums_list = []             # list of discarded CNums per event time

        # LISTS of Server/Queue--related matters
        self.Bt1_values = []                       # server 1 status per event time
        self.Bt2_values = []                       # server 2 status per event time
        self.Qt_values = []                        # no. of customers in queue per event time
        self.customer_in_s1_list = []              # customer being served by server 1 per event time
        self.customer_in_s2_list = []              # customer being served by server 2 per event times
        self.q_customer_list = []                  # customers waiting per event time
        self.total_area_Qt_list = []
        self.total_area_Bt1_list = []
        self.total_area_Bt2_list = []

    def run_simulation(self):
        # initialization
        n_A = 0                                  # no. of arrival
        next_a = self.g_arrival_times[n_A]       # initial arrival time
        service = self.g_service_times[n_A]      # initial service time
        next_d1 = next_d2 = inf                  # initial departure times
        prev_d1 = prev_d2 = 0
        delay_per_event = 0
        total_delay_per_event = 0

        # for customer tracking
        customer_s1 = 0                          # current customer in server 1
        customer_s2 = 0                          # current customer in server 2

        while True:
            prev_clock = self.clock

            # Timing Routine
            next_event = min(next_a, next_d1, next_d2)
            self.clock = next_event

            # Event Routine
            if next_event == inf:   # no future arrival and all servers are vacant
                break

            elif next_event == next_a and next_a != min(next_d1, next_d2):
                n_A += 1
                self.events.append((self.clock, 'Arrival', n_A))

                # Server 1 is Free
                if self.s1_status == 0:
                    customer_s1 = n_A
                    next_d1 = self.server_process("server 1", next_a, service, prev_d1, prev_d2)

                # Server 2 is Free
                elif self.s2_status == 0:
                    customer_s2 = n_A
                    next_d2 = self.server_process("server 2", next_a, service, prev_d1, prev_d2)

                # Both Server are Busy
                else:
                    if not self.Q.is_Full():
                        self.Q.enqueue(next_a, service, n_A)
                        self.total_waited += 1
                    else:
                        self.discarded_entities.append(next_a)
                        self.discarded_CNums.append(n_A)
                        self.total_discarded += 1

            elif next_event == next_d1:
                self.events.append((self.clock, 'Departure', customer_s1))
                prev_d1 = next_d1
                self.total_served += 1

                if self.Q.size > 0:
                    Q_arrival, service, customer_s1 = self.Q.dequeue()
                    next_d1 = self.server_process("server 1", Q_arrival, service, prev_d1, prev_d2)
                    delay_per_event += self.clock - Q_arrival

                else:
                    self.s1_status = 0
                    customer_s1 = 0
                    next_d1 = inf

            elif next_event == next_d2:
                self.events.append((self.clock, 'Departure', customer_s2))
                prev_d2 = next_d2
                self.total_served += 1

                if self.Q.size > 0:
                    Q_arrival, service, customer_s2 = self.Q.dequeue()
                    next_d2 = self.server_process("server 2", Q_arrival, service, prev_d1, prev_d2)
                    delay_per_event = round(self.clock - Q_arrival, 2)
                    total_delay_per_event += delay_per_event
                else:
                    self.s2_status = 0
                    customer_s2 = 0
                    next_d2 = inf


            # per event
            self.calc_area_Bt_Qt(prev_clock)
            self.update_event_details(customer_s1, customer_s2, delay_per_event, total_delay_per_event)

            # updating next arrival / future event list
            next_a = self.g_arrival_times[n_A] if n_A != len(self.g_arrival_times) else inf
            service = self.g_service_times[n_A] if next_a != inf else 0
            self.future_event_list.append(f"[A: {next_a}, D1: {next_d1}, D2: {next_d2}]")


    def server_process(self, server, arrival, service, prev_d1, prev_d2):
        self.update_server_idle_times(arrival, prev_d1, prev_d2)
        self.server_used.append(server)

        if server == "server 1":
            self.s1_status = 1
            self.total_s1_service += service
        else:
            self.s2_status = 1
            self.total_s2_service += service

        service_start_time = self.clock
        departure = round(service_start_time + service, 2)
        wait_time = max(0, self.clock - arrival)
        self.total_delays += wait_time
        self.create_customer(arrival, service_start_time, service, departure, wait_time)

        return departure

    def update_server_idle_times(self, arrival, prev_d1, prev_d2):
        if len(self.server_used) > 0:
            prev_Customer = self.Customers[-1]
            if self.server_used[-1] == "server 1":
                s1_idle = (arrival - prev_d1) if self.s1_status == 0 else 0
                s2_idle = (arrival - prev_Customer.arrival_time) if self.s2_status == 0 else 0

            else:
                s1_idle = (arrival - prev_d1) if self.s1_status == 0 else 0
                s2_idle = (arrival - prev_d2) if self.s2_status == 0 else 0
        else:
            s1_idle = arrival
            s2_idle = arrival

        self.total_s1_idles += s1_idle
        self.total_s2_idles += s2_idle

        self.total_s1_idle_times.append(self.total_s1_idles)
        self.total_s2_idle_times.append(self.total_s2_idles)

    def calc_area_Bt_Qt(self, prev_clock):
        dt = self.clock - prev_clock

        if prev_clock == 0:
            Qt = Bt1 = Bt2 = 0
        else:
            Qt = self.Qt_values[-1]
            Bt1 = self.Bt1_values[-1]
            Bt2 = self.Bt2_values[-1]

        # calculation
        self.total_area_Qt += Qt * dt
        self.total_area_Bt1 += Bt1 * dt
        self.total_area_Bt2 += Bt2 * dt

        # storing the results
        self.total_area_Qt_list.append(round(self.total_area_Qt, 2))
        self.total_area_Bt1_list.append(round(self.total_area_Bt1, 2))
        self.total_area_Bt2_list.append(round(self.total_area_Bt2, 2))

    def update_event_details(self, customer_s1, customer_s2, delay_per_event, total_delay_per_event):
        # for Numerical values (Bt & Qt)
        self.Bt1_values.append(self.s1_status)
        self.Bt2_values.append(self.s2_status)
        self.Qt_values.append(self.Q.size)

        # for Descriptive values (Bt & Qt)
        self.customer_in_s1_list.append(customer_s1)
        self.customer_in_s2_list.append(customer_s2)
        self.q_customer_list.append(self.Q.customer_nums.copy())

        # for snapshots
        self.q_arrival_list.append(self.Q.arrivals.copy())
        self.num_delay_list.append(self.total_waited)
        self.delay_time_list.append(round(delay_per_event, 2))
        self.total_delay_event_list.append(round(total_delay_per_event, 2))
        self.discarded_arrivals_list.append(self.discarded_entities.copy())
        self.discarded_CNums_list.append(self.discarded_CNums.copy())

    def create_customer(self, arrival_time, service_start_time, service_time, departure_time, wait_time):
        newCustomer = Customer(arrival_time, wait_time, service_start_time,
                               service_time, departure_time)
        self.Customers.append(newCustomer)


    # PRINTING (Outputs)
    def get_results(self, test_name, run_name):
        #display_outputs(self, test_name, run_name)

        # Exporting Simulation Details to various files
        export_output_screen(self, f'Outputs/{test_name}/{test_name}_3runs_Statistics.txt', test_name, run_name)
        export_simulation_details(self, f'Outputs/{test_name}/Simulation_Data/{test_name}-{run_name}_simulation_data.xlsx')
        export_snapshots_table(create_snapshots_table(self), f'Outputs/{test_name}/Snapshots/{test_name}-{run_name}_snapshots_data.txt')
        export_customer_data(self, f'Outputs/{test_name}/Customer_Data/{test_name}-{run_name}_customer_data.txt')

    # PLOTTING RESULTS
    def plot(self):
        plot_graph(self)


    # CALCULATIONS (Statistics)
    def calc_avg_delay(self):
        return round((self.total_delays / self.total_served), 2)

    def calc_qn(self):
        Tn = self.events[-1][0]
        return round(self.total_area_Qt / Tn, 2)

    def calc_s1_utilization(self):
        Tn = self.events[-1][0]
        return round(self.total_area_Bt1 / Tn, 2)

    def calc_s2_utilization(self):
        Tn = self.events[-1][0]
        return round(self.total_area_Bt2 / Tn, 2)

    def get_total_delays(self):
        return round(self.total_delays, 2)

    def get_total_s1_idles(self):
        last_Customer = self.Customers[-1]
        return round((last_Customer.departure_time - self.total_s1_service), 2)

    def get_total_s2_idles(self):
        last_Customer = self.Customers[-1]
        return round((last_Customer.departure_time - self.total_s2_service), 2)

    def get_mean_waiting_time(self):
        return round(self.total_delays / self.total_served, 2)

    def get_mean_s1_idle_time(self):
        end_time = self.events[-1][0]
        return round((end_time - self.total_s1_service) / self.total_served, 2)

    def get_mean_s2_idle_time(self):
        end_time = self.events[-1][0]
        return round((end_time - self.total_s2_service) / self.total_served, 2)

    def get_avg_time_spent_in_system(self):
        total_time_spent_in_system = 0
        for customer in self.Customers:
            total_time_spent_in_system += customer.time_spent_in_system
        return round(total_time_spent_in_system / self.total_served, 2)

    def get_prob_C_wait(self):
        total_customer_waited = 0  # total of customer who has a waiting time
        for customer in self.Customers:
            total_customer_waited += (1 if customer.waiting_time > 0 else 0)

        return round(total_customer_waited / self.total_served, 2)

    def get_prob_Idle_s1(self):
        end_time = self.events[-1][0]
        return round((end_time - self.total_s1_service)/end_time, 2)

    def get_prob_Idle_s2(self):
        end_time = self.events[-1][0]
        return round((end_time - self.total_s2_service)/end_time, 2)





