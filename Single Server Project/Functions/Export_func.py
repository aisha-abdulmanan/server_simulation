import pandas as pd

# OUTPUT File (MS EXCEL)
def export_simulation_details(system, filename):
    data_sheet1 = {
        'IAT': system.g_inter_arrival_times,
        'AT': system.g_arrival_times,
        'ST': system.g_service_times
    }

    data_sheet2 = {
        'AT': [],
        'WT': [],
        'SST': [],
        'ST': [],
        'DT': [],
        ' ': [],
        'TSS': [],
        'server IT': system.idle_times
    }
    for customer in system.Customers:
        data_sheet2['AT'].append(customer.arrival_time)
        data_sheet2['WT'].append(customer.waiting_time)
        data_sheet2['SST'].append(customer.service_start_time)
        data_sheet2['ST'].append(customer.service_time)
        data_sheet2['DT'].append(customer.departure_time)
        data_sheet2[' '].append(" ")
        data_sheet2['TSS'].append(customer.time_spent_in_system)

    data_sheet3 = {
        'Clock': [],
        'Event Type': [],
        'Future Event': system.future_events,
        'B(t)': system.Bt_values,
        'Q(t)': system.Qt_values,
        'C# in Server': system.customer_server_list,
        'C# in Queue': system.customers_queue_list,
        'Discarded C#': system.discarded_CNum_list,
        ' ': [],
        'Area B(t)': system.total_area_Bt_list,
        'Area Q(t)': system.total_area_Qt_list
    }
    for event in system.events:
        data_sheet3['Clock'].append(event[0])
        data_sheet3['Event Type'].append([event[1], event[2]])
        data_sheet3[' '].append(" ")

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


# OUTPUT File (TEXT FILE)
def export_customer_simulation_data(system, filename):
    with open(filename, 'w') as f:    # with statement automatically closes the file
        f.write("Single Server Queuing System SIMULATION\n\n")
        for i, customer in zip(range(1, len(system.Customers) + 1), system.Customers):
            print(f'Customer {i}: ', customer, '\n', file=f)

def export_snapshots_table(snapshots_table, filename):
    with open(filename, 'w') as f:
        f.write("Simulation Process per Event\n\n")
        print(snapshots_table, file=f)

def export_output_screen(system, filename, test_name, run_name):
    with open(filename, 'a') as f:    # with statement automatically closes the file
        print("-------------------------------------------------------------------------------", file=f)
        print(f"Simulation: {test_name} - {run_name}", file=f)
        print(f"    Arrival times = {system.g_arrival_times}", file=f)
        print(f"    Service times = {system.g_service_times}", file=f)
        print("---------------------------------------------------------------------------------", file=f)

        N = len(system.events)
        end_time = system.events[N - 1][0]

        print("N =", N, " (number of successive events)", file=f)
        print("T(N) =", end_time, " (simulation end time)", file=f)

        # TOTAL STATISTICAL COUNTERS
        print("\nStatistical Counters: ", file=f)
        print("  1. Total area under Q(t) =", round(system.total_area_Qt, 2), file=f)
        print("  2. Total area under B(t) =", round(system.total_area_Bt, 2), file=f)
        print("  3. Total idle times =", round(system.total_idles, 2), file=f)
        print("  4. Total served customers = ", system.total_served, file=f)
        print("  5. Total discarded customers =", system.get_total_discarded(), file=f)
        if system.Tn is not None:
            print(f"  6. Total unserved customers = ", system.total_unserved, file=f)
            if system.extended_time != 0:
                print(f"  7. Total time (past clock: {system.Tn}): {system.extended_time}", file=f)

        # PERFORMANCE MEASURES
        print("\nMeasures of Performance: ", file=f)
        print(f"  1. Average of Customers in the Queue:    q hat (n) = {system.calc_qn()}", file=f)
        print(f"  2. Expected Average Delay:               d hat (n) = {system.calc_avg_delay()}", file=f)
        print(f"  3. Expected Utilization of the Server:   u hat (n) = {system.calc_utilization()}", file=f)

        # OTHER MEASURES
        print("\nOther Measures: ", file=f)
        print("  1. Mean server idle time:", system.get_mean_idle_time(), file=f)
        print("  2. Probability of Idle time of the server:", system.calc_prob_Idle_server(), file=f)
        print("  3. Probability of a Customer has to wait:", system.calc_prob_C_wait(), file=f)
        print("  4. Average time the customer spends in the system:", system.get_avg_time_spent_in_system(), file=f)

        f.write("\n\n")
