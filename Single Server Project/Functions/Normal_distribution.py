import numpy as np


# Random Number Generator (Normal Distribution)
def generate_random_number(mean, std_dev):
    num = np.round(np.random.normal(mean, std_dev), 1)
    return num if num > 0 else generate_random_number(mean, std_dev)


def generate_inter_arrival_times(mean, std_dev, num_customers):
    inter_arrival_times = []
    for n in range(num_customers):
        inter_arrival_times.append(generate_random_number(mean, std_dev))
    return inter_arrival_times


def generate_service_times(mean, std_dev, num_customers):
    service_times = []
    for n in range(num_customers):
        service_times.append(generate_random_number(mean, std_dev))
    return service_times


def generate_arrival_times(inter_arrival_times):
    arrival_time = 0
    arrival_times = []
    for time in inter_arrival_times:
        arrival_time = round(arrival_time + time, 2)
        arrival_times.append(arrival_time)

    return arrival_times
