from prettytable import PrettyTable

def create_snapshots_table(self):
    myTable = PrettyTable(["Clock", "System state", "Statistical Counters"])

    # at clock 0
    myTable = initialize_row(self, myTable)

    # at (clock: first arrival) onwards
    for i, event in zip(range(len(self.events)), self.events):
        clock = event[0]
        event = f"[{event[1]}, C#{event[2]}]"
        f_event = self.future_event_list[i]
        s1_status = self.Bt1_values[i]
        s2_status = self.Bt2_values[i]
        Qt = self.Qt_values[i]
        q_arrival = self.q_arrival_list[i]
        discarded = self.discarded_arrivals_list[i]
        num_delay = self.num_delay_list[i]
        area_Bt1 = self.total_area_Bt1_list[i]
        area_Bt2 = self.total_area_Bt2_list[i]
        area_Qt = self.total_area_Qt_list[i]
        total_delay = self.total_delay_event_list[i]


        myTable.add_row([f"Clock: {clock}\nEL: {f_event}\n"
                         f"\nEvent: {event}",

                         f"Server 1 status: {s1_status}\nServer 2 status: {s2_status}\n"
                         f"No. in Queue: {Qt}\n"
                         f"Times of Arrival: {q_arrival}\nDiscarded: {discarded}",

                         f"Number Delayed: {num_delay}\nTotal delay: {total_delay}\n"
                         f"Area under B1(t) = {area_Bt1}\nArea under B2(t) = {area_Bt2}\n"
                         f"Area under Q(t) = {area_Qt}"])

        myTable.add_row(['-' * x for x in [35, 50, 25]])

    return myTable

def initialize_row(self, myTable):
    clock = s1_s = s2_s = Qt = num_delay = total_delay = area_Bt1 = area_Bt2 = area_Qt = 0
    q_arrival = discarded = []
    event = None
    f_event = f"[A: {self.g_arrival_times[0]}, D1: inf, D2: inf]"

    myTable.add_row([f"Clock: {clock}\nEL: {f_event}\n"
                     f"\nEvent: {event}",

                     f"Server 1 status: {s1_s}\nServer 2 status: {s2_s}\n"
                     f"No. in Queue: {Qt}\n"
                     f"Times of Arrival: {q_arrival}\nDiscarded: {discarded}",

                     f"Number Delayed: {num_delay}\nTotal delay: {total_delay}\n"
                     f"Area under B1(t) = {area_Bt1}\nArea under B2(t) = {area_Bt2}\n"
                     f"Area under Q(t) = {area_Qt}"])

    myTable.add_row(['-' * x for x in [35, 50, 25]])

    return myTable