# PRINTING RESULT
def display_outputs(self, test_name, run_name):
    print("-------------------------------------------------------------------------------")
    print(f"Simulation: {test_name} - {run_name}")
    print(f"    Arrival times = {self.g_arrival_times}")
    print(f"    Service times = {self.g_service_times}")
    print("---------------------------------------------------------------------------------")

    N = len(self.events)
    end_time = self.events[N - 1][0]

    print("N =", N, " (number of successive events)")
    print("T(N) =", end_time, " (simulation end time)")

    display_total_Counters(self)
    display_Measures_Performance(self)
    display_other_Measures(self)


def display_total_Counters(self):
    print("\nStatistical Counters: ")
    print("  1. Total area under Q(t) =", round(self.total_area_Qt, 2))
    print("  2. Total area under B(t) =", round(self.total_area_Bt, 2))
    print("  3. Total server idles =", round(self.total_idles, 2))
    print("  4. Total served customers =", self.total_served)
    print("  5. Total discarded customers =", self.get_total_discarded())
    if self.Tn is not None:
        print("  6. Total unserved customers =", self.total_unserved)
        if self.extended_time != 0:
            print(f"  7. Total time (past clock: {self.Tn}): {self.extended_time}")

def display_Measures_Performance(self):
    print("\nMeasures of Performance: ")
    print(f"  1. Average of Customers in the Queue:    q hat (n) = {self.calc_qn()}")
    print(f"  2. Expected Average Delay:               d hat (n) = {self.calc_avg_delay()}")
    print(f"  3. Expected Utilization of the Server:   u hat (n) = {self.calc_utilization()}")

def display_other_Measures(self):
    print("\nOther Measures: ")
    print("  1. Mean server idle time:", self.get_mean_idle_time())
    print("  2. Probability of Idle time of the server:", self.calc_prob_Idle_server())
    print("  3. Probability of a Customer has to wait:", self.calc_prob_C_wait())
    print("  4. Average time the customer spends in the system:", self.get_avg_time_spent_in_system())



