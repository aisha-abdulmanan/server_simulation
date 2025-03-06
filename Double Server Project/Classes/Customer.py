class Customer:
    def __init__(self, arrival_time,  waiting_time, service_start_time, service_time, departure_time):
        self.arrival_time = round(arrival_time, 2)
        self.waiting_time = round(waiting_time, 2)
        self.service_start_time = round(service_start_time, 2)
        self.service_time = round(service_time, 2)
        self.departure_time = round(departure_time, 2)
        self.time_spent_in_system = round(self.waiting_time + self.service_time, 2)

    def __str__(self):
        return f'\n Arrival Time:---------------{self.arrival_time} ' \
               f'\n Waiting Time:---------------{self.waiting_time} ' \
               f'\n Service Start Time:---------{self.service_start_time}' \
               f'\n Service Time:---------------{self.service_time}' \
               f'\n Departure Time:-------------{self.departure_time}' \
               f'\n Time Spent in the System:---{self.time_spent_in_system}'

