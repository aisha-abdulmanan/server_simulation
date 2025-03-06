# server_simulation

## Program Overview:
- Written in Python for readability.
- Requires libraries (pandas, prettytable, matplotlib) for exporting data.
- Organized into multiple folders and files for better structure (readable & modifiable):
  - 3 class files (Queue, Customer, Single_Server/Double_Server) in folder *<b>Classes</b>*
  - 5 function files (Normal_distribution, Display, Export, Snapshot, Plot) in folder *<b>Functions</b>*
## Inputs:
Both the two main programs accept data in two ways:
1. <b>Pre-defined data</b>: Provide arrays for inter-arrival times, service times, and arrival times.
2. <b>Random generation</b>: Specify means and standard deviations for inter-arrival and service times. The system will generate them based on a normal distribution and calculate arrival times.
## Outputs:
- Generates detailed information about the simulation.
- Saves output files to a separate folder named *<b>Outputs</b>*.
  - Subfolders are created for each test name and output type.
  - There are 3 subfolders for each test folder: 
    - <b>Customer_Data</b> - provides details about the customer 
    - <b>Simulation_Data</b> – provides details about the overall simulation process
    - <b>Snapshots</b> – provides details every clock time
  - Creating new test folders requires including subfolders to prevent errors.
  - Existing files are overwritten during program execution.
  - The <b>Outputs</b> folder can be emptied of files, but not deleted. Deleting it will cause errors during program execution.
## Plotting:
- Plotting functionality is disabled by default.
- Shows 3 graphs in one window:
  - Number of People in Queue over time
  - Server Status over time
  - Delay over time
- Multiple test runs will display graphs one at a time. Close the current graph to view the 
next.
