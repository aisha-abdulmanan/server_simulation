from prettytable import PrettyTable

def create_snapshots_table(self):
    myTable = PrettyTable(["Clock", "System state", "Statistical Counters"])

    # for clock = 0:
    myTable = initialize_row(self, myTable)

    # for (clock = first arrival) onwards
    for i, event in zip(range(len(self.events)), self.events):
        clock = event[0]
        f_event = self.future_events[i]
        event_type = f"<{event[1]}, C#{event[2]}>"
        ss = self.Bt_values[i]
        Qt = self.Qt_values[i]
        q_arrival = self.q_arrivals_list[i]
        discarded = self.discarded_list[i]
        num_delay = self.num_delay_list[i]
        area_Bt = self.total_area_Bt_list[i]
        area_Qt = self.total_area_Qt_list[i]
        total_delay = self.total_delay_event_list[i]

        myTable.add_row([f"Clock: {clock}\nEL: {f_event}\n\n{event_type}",

                         f"Server status: {ss}\nNo. in Queue: {Qt}\n"
                         f"Times of Arrival: {q_arrival}\nDiscarded = {discarded}",

                         f"Number Delayed: {num_delay}\nTotal delay: {total_delay}\n"
                         f"Area under B(t) = {area_Bt}\nArea under Q(t) = {area_Qt}"])

        myTable.add_row(['-' * x for x in [25, 40, 25]])

    return myTable


def initialize_row(self, myTable):
    clock = ss = Qt = num_delay = total_delay = area_Bt = area_Qt = 0
    q_arrival = discarded = []
    f_event = f"[A: {self.g_arrival_times[0]}, D: inf]"
    event_type = f"<None>"

    myTable.add_row([f"Clock: {clock}\nEL: {f_event}\n\n{event_type}",

                     f"Server status: {ss}\nNo. in Queue: {Qt}\n"
                     f"Times of Arrival: {q_arrival}\nDiscarded = {discarded}",

                     f"Number Delayed: {num_delay}\nTotal delay: {total_delay}\n"
                     f"Area under B(t) = {area_Bt}\nArea under Q(t) = {area_Qt}"])

    myTable.add_row(['-' * x for x in [25, 40, 25]])

    return myTable
