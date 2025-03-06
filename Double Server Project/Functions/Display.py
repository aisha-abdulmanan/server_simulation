# OUTPUT FUNCTIONS
def display_outputs(self, test_name, run_name):
    print("-------------------------------------------------------------------------------")
    print(f"Simulation: {test_name} - {run_name}")
    print(f"    Arrival times = {self.g_arrival_times}")
    print(f"    Service times = {self.g_service_times}")
    print("---------------------------------------------------------------------------------")

    N = len(self.events)
    end_time = self.events[N-1][0]

    print("N =", N, " (number of successive events)")
    print("T(N) =", end_time, " (simulation end time)")

    display_Counters(self)
    display_Performance_Measures(self)
    display_other_Measures(self)

    print("\n\n")



def display_Counters(self):
    print("\nStatistical Counters: ")
    print("  1. Total area under Q(t) =", round(self.total_area_Qt, 2))
    print("  2. Total area under B1(t) =", round(self.total_area_Bt1, 2))
    print("  3. Total area under B2(t) =", round(self.total_area_Bt2, 2))
    print("  4. Total server 1's idle times =", self.get_total_s1_idles())
    print("  5. Total server 2's idle times =", self.get_total_s2_idles())
    print("  6. Total served customers = ", self.total_served)
    print("  7. Total discarded customers =", self.total_discarded)

def display_Performance_Measures(self):
    print("\nMeasures of Performance: ")
    print(f"  1. Average of Customers in the Queue:            q_hat(n) = {self.calc_qn()} ")
    print(f"  2. Expected Average Delay:                       d_hat(n) = {self.calc_avg_delay()}")
    print(f"  3. Expected Utilization of the Server 1:         u1_hat(n) = {self.calc_s1_utilization()}")
    print(f"  4. Expected Utilization of the Server 2:         u2_hat(n) = {self.calc_s2_utilization()}")

def display_other_Measures(self):
    print("\nOther Measures: ")
    print("  1. Mean server 1 idle time:", self.get_mean_s1_idle_time())
    print("  2. Mean server 2 idle time:", self.get_mean_s2_idle_time())
    print("  3. Probability of Idle time of server 1:", self.get_prob_Idle_s1())
    print("  4. Probability of Idle time of server 2:", self.get_prob_Idle_s2())
    print("  5. Probability of a Customer has to wait:", self.get_prob_C_wait())
    print("  6. Average time the customer spends in the system:", self.get_avg_time_spent_in_system())
