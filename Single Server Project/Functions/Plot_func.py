import matplotlib.pyplot as plt

def plot_graph(self):
    clocks = []
    for event in self.events:
        clocks.append(event[0])

    bar_width = [clocks[i+1] - clocks[i] for i in range(len(clocks) - 1)]
    bar_width.append(bar_width[-1])

    plt.figure(figsize=(12, 7))

    # Plot Clock vs Queue Length
    plt.subplot(2, 3, 1)            # row, column, index
    plt.bar(clocks, self.Qt_values, color='blue', width=bar_width, align='edge')
    plt.title('Number of People in Queue over Time')
    plt.xlabel('Clock (Time)')
    plt.ylabel('Number of People in Queue')
    plt.yticks(range(6))             # limit of Queue line is 5
    plt.grid(True)

    # Plot Clock vs Server Status
    plt.subplot(2, 3, 2)
    plt.bar(clocks, self.Bt_values, color='green', width=bar_width, align='edge')
    plt.title('Server Status over Time')
    plt.xlabel('Clock (Time)')
    plt.ylabel('Server Status')
    plt.yticks([0, 1])
    plt.grid(True)

    # Plot Clock vs Delay_time
    plt.subplot(2, 3, 3)
    plt.bar(clocks, self.delay_time_list, color='violet', width=bar_width, align='edge')
    plt.title('Delay over Time')
    plt.xlabel('Clock (Time)')
    plt.ylabel('Delay Time')
    plt.grid(True)

    plt.tight_layout()
    plt.show()
