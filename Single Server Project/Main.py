# ABDULMANAN, SITTIE AISHA C.  (CSC133)
# Program: Single-Server Queueing System

import os
import sys
from Single_Server import *
from Functions.Normal_distribution import *


def OutputFolderExists(test_name):
    # Check if the destination path of the outputs are created prior to proceeding to the program
    folders = ["Customer_Data", "Simulation_Data", "Snapshots"]
    for folder in folders:
        output_path = f"Outputs/{test_name}/{folder}"
        if os.path.exists(output_path):
            continue
        else:
            print(f"ERROR: Path for output file doesn't exist\n"
                  f"Make sure '{test_name}' subfolders all exist.\n"
                  f"- Outputs/{test_name}/{folders[0]}\n"
                  f"- Outputs/{test_name}/{folders[1]}\n"
                  f"- Outputs/{test_name}/{folders[2]}\n")
            sys.exit()
    return True

def simulation_run(test_name, run_name, IAT_mean, IAT_std_dev, ST_mean, ST_std_dev, num_samples):
    # generating values for INTER_ARRIVAL and SERVICE TIMES
    inter_arrival_times = generate_inter_arrival_times(IAT_mean, IAT_std_dev, num_samples)
    service_times = generate_service_times(ST_mean, ST_std_dev, num_samples)
    arrival_times = generate_arrival_times(inter_arrival_times)

    # Create and run SIMULATION
    q1_system = Single_Server_Queueing_System(inter_arrival_times, arrival_times, service_times)
    q1_system.run_simulation()
    q1_system.get_outputs(test_name, run_name)
    # q1_system.plot()

def test1():
    # Parameters (IAT = ST)
    IAT_mean = ST_mean = 5
    IAT_std_dev = ST_std_dev = 1.0
    num_samples = 200

    test = "Test1"
    runs = 3

    if OutputFolderExists(test):
        for i in range(runs):
            simulation_run(test, f"run{i + 1}", IAT_mean, IAT_std_dev, ST_mean, ST_std_dev, num_samples)
    else:
        sys.exit()

def test2():
    # Parameters (IAT > ST)
    IAT_mean = 10
    ST_mean = 3
    IAT_std_dev = 1
    ST_std_dev = 1
    num_samples = 200

    test = "Test2"
    runs = 3

    if OutputFolderExists(test):
        for i in range(runs):
            simulation_run(test, f"run{i + 1}", IAT_mean, IAT_std_dev, ST_mean, ST_std_dev, num_samples)

def test3():
    # Parameters (IAT < ST)
    IAT_mean = 3
    ST_mean = 10
    IAT_std_dev = 1
    ST_std_dev = 1
    num_samples = 200

    test = "Test3"
    runs = 3

    if OutputFolderExists(test):
        for i in range(runs):
            simulation_run(test, f"run{i + 1}", IAT_mean, IAT_std_dev, ST_mean, ST_std_dev, num_samples)


# MAIN
test1()
test2()
test3()


print("\n\n------------------------------------------------------")
print("For further information, check the following files: ")
print(f"  1. 'Outputs/TestName_#runs_Statistics.txt")
print(f"  2. 'Outputs/TestName-RunName_simulation_data.xlsx'")
print(f"  3. 'Outputs/TestName-RunName_customer_data.txt'")
print(f"  4. 'Outputs/TestName-RunName_snapshots_data.txt'")
print("------------------------------------------------------\n")
