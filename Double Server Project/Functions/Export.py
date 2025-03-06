import pandas as pd

# OUTPUT File (MS EXCEL)
def export_simulation_details(self, filename):
    data_sheet1 = {
        'IAT': self.g_inter_arrival_times,
        'AT': self.g_arrival_times,
        'ST': self.g_service_times
        }

    data_sheet2 = {
        'AT': [],
        'Server': self.server_used,
        'WT': [],
        'SST': [],
        'ST': [],
        'DT': [],
        '': [],
        'TSS': [],
        's1 IT': self.total_s1_idle_times,
        's2 IT': self.total_s2_idle_times
        }
    for customer in self.Customers:
        data_sheet2['AT'].append(customer.arrival_time)
        data_sheet2['WT'].append(customer.waiting_time)
        data_sheet2['SST'].append(customer.service_start_time)
        data_sheet2['ST'].append(customer.service_time)
        data_sheet2['DT'].append(customer.departure_time)
        data_sheet2[''].append('')
        data_sheet2['TSS'].append(customer.time_spent_in_system)

    data_sheet3 = {
        'Clock': [],
        'Event Type': [],
        'Future Event List': self.future_event_list,
        'B1(t)': self.Bt1_values,
        'B2(t)': self.Bt2_values,
        'Q(t)': self.Qt_values,
        'C# in S1': self.customer_in_s1_list,
        'C# in S2': self.customer_in_s2_list,
        'C# in Line': self.q_customer_list,
        'Discarded C#': self.discarded_CNums_list,
        '': [],
        'Area Bt1': self.total_area_Bt1_list,
        'Area Bt2': self.total_area_Bt2_list,
        'Area Qt': self.total_area_Qt_list
        }
    for event in self.events:
        data_sheet3['Clock'].append(event[0])
        data_sheet3['Event Type'].append([event[1], event[2]])
        data_sheet3[''].append('')

    # creating Excel sheets
    df1 = pd.DataFrame(data_sheet1)
    df2 = pd.DataFrame(data_sheet2)
    df3 = pd.DataFrame(data_sheet3)

    # reset the index and add 1 to each value  (adjusting index)
    df1.index = df1.index + 1
    df2.index = df2.index + 1
    df3.index = df3.index + 1

    # renaming the Excel sheets
    with pd.ExcelWriter(filename) as writer:
        df1.to_excel(writer, sheet_name='Generated Inputs', index=True)
        df2.to_excel(writer, sheet_name='Simulation Details', index=True)
        df3.to_excel(writer, sheet_name='Event Details', index=True)


# TEXT FILE
def export_customer_data(self, filename):
    with open(filename, 'w') as f:  # with statement automatically closes the file
        f.write("Double Server Queuing System SIMULATION\n\n")
        for i, customer in zip(range(1, len(self.Customers)+1), self.Customers):
            print(f'Customer {i}: ', customer, '\n', file=f)

        f.write("\nTotal Idles of Server 1\n")
        f.write(f"  {self.total_s1_idles}\n")
        f.write("Total Idles of Server 2\n")
        f.write(f"  {self.total_s2_idles}\n")

def export_snapshots_table(snapshots_table, filename):
    with open(filename, 'w') as f:
        f.write("Simulation Process per Event\n\n")
        print(snapshots_table, file=f)

def export_output_screen(self, filename, test_name, run_name):
    with open(filename, 'a') as f:
        print("-------------------------------------------------------------------------------", file=f)
        print(f"Simulation: {test_name} - {run_name}", file=f)
        print(f"    Arrival times = {self.g_arrival_times}", file=f)
        print(f"    Service times = {self.g_service_times}", file=f)
        print("---------------------------------------------------------------------------------", file=f)

        N = len(self.events)
        end_time = self.events[N-1][0]

        print("N =", N, " (number of successive events)", file=f)
        print("T(N) =", end_time, " (simulation end time)", file=f)

        # TOTAL STATISTICAL COUNTERS
        print("\nStatistical Counters: ", file=f)
        print("  1. Total area under Q(t) =", round(self.total_area_Qt, 2), file=f)
        print("  2. Total area under B1(t) =", round(self.total_area_Bt1, 2), file=f)
        print("  3. Total area under B2(t) =", round(self.total_area_Bt2, 2), file=f)
        print("  4. Total server 1's idle times =", self.get_total_s1_idles(), file=f)
        print("  5. Total server 2's idle times =", self.get_total_s2_idles(), file=f)
        print("  6. Total served customers = ", self.total_served, file=f)
        print("  7. Total discarded customers =", self.total_discarded, file=f)

        # PERFORMANCE MEASURES
        print("\nMeasures of Performance: ", file=f)
        print("  1. Average of Customers in the Queue:          q_hat(n) =", self.calc_qn(), file=f)
        print("  2. Expected Average Delay:                     d_hat(n) =", self.calc_avg_delay(), file=f)
        print("  3. Expected Utilization of the Server 1:       u1_hat(n) =", self.calc_s1_utilization(), file=f)
        print("  4. Expected Utilization of the Server 2:       u2_hat(n) =", self.calc_s2_utilization(), file=f)

        # OTHER MEASURES
        print("\nOther Measures: ", file=f)
        print("  1. Mean server 1 idle time:", self.get_mean_s1_idle_time(), file=f)
        print("  2. Mean server 2 idle time:", self.get_mean_s2_idle_time(), file=f)
        print("  3. Probability of Idle time of server 1:", self.get_prob_Idle_s1(), file=f)
        print("  4. Probability of Idle time of server 2:", self.get_prob_Idle_s2(), file=f)
        print("  5. Probability of a Customer has to wait:", self.get_prob_C_wait(), file=f)
        print("  6. Average time customer spends in the system:", self.get_avg_time_spent_in_system(), file=f)

        print("\n\n", file=f)
