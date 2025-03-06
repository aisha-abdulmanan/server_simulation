class Queue:
    def __init__(self, capacity):
        self.capacity = capacity
        self.size = 0
        self.arrivals = []
        self.services = []
        self.customer_nums = []

    def enqueue(self, arrival, service, customer_num):
        if self.is_Full():
            print("Overflow Error")
        else:
            self.arrivals.append(arrival)
            self.services.append(service)
            self.customer_nums.append(customer_num)
            self.size += 1

    def dequeue(self):
        if self.is_Empty():
            print("Underflow Error")
            return 0
        else:
            arrival = self.arrivals.pop(0)
            service = self.services.pop(0)
            customer_num = self.customer_nums.pop(0)
            self.size -= 1
            return arrival, service, customer_num

    def peek(self):
        return self.arrivals[0], self.services[0], self.customer_nums[0]

    def is_Empty(self):
        return True if self.size == 0 else False

    def is_Full(self):
        return True if self.size == self.capacity else False

