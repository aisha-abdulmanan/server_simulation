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

def generate_arrival_times(inter_arrival_times):
        # calculating for each customer's ARRIVAL TIME
        arrival_times = []
        arrival_time = 0
        for time in inter_arrival_times:
            arrival_time = arrival_time + time
            arrival_times.append(round(arrival_time, 2))
        return arrival_times



def generate_service_times(mean, std_dev, num_customers):
    service_times = []
    for n in range(num_customers):
        service_times.append(generate_random_number(mean, std_dev))
    return service_times