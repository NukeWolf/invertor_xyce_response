import pandas as pd
from matplotlib import pyplot as plt
import subprocess
import os.path

from config import *
from util import format_frequency


# Run Xyce Sim
if (not os.path.isfile(RESULTS_FILENAME)):
    out = subprocess.check_output(["xyce", CIR_FILENAME])
    print(out)


# Get simulation parameters
df = pd.read_table(OUTPUT_STEP_PARAMETERS_FILENAME,sep="\s+", skipfooter=1)

simulation_parameters = []

for index, row in df.iterrows():
    parameters = {}
    for column_name in df.columns:
        if column_name != "STEP":
            parameters[column_name] = row[column_name]
    simulation_parameters.append(parameters)

print(simulation_parameters)

# Plot results
df = pd.read_csv(RESULTS_FILENAME)
split_runs = []

# Initialize variables to keep track of the split indices
start_index = 0

# Iterate through and split seperate transient analysis runs.
for index, row in df.iterrows():
    timestamp = row['TIME']
    if timestamp == 0.0 and index != 0:
        split_runs.append(df.iloc[start_index:index])
        start_index = index
# Last Run
split_runs.append(df.iloc[start_index:])



# Plotting
NUM_PLOTS = PLOT_ROWS * PLOT_COLS
figure, axis = plt.subplots(PLOT_ROWS, PLOT_COLS) 

index = 0
print(split_runs)

# Iterate through every run and corresponding parameters
for parameter, rows in zip(simulation_parameters,split_runs):
    if index >= NUM_PLOTS:
        continue

    num_cols = range(1,rows.shape[1])
    time_vals = rows.iloc[:,0]
    voltage_lines = [rows.iloc[:,x] for x in num_cols]
    row = index // PLOT_COLS
    col = index - row * PLOT_COLS
    
    title = "\n"
    for key in parameter:
        if key == "FREQUENCY":
            parameter[key] = format_frequency(parameter[key])
        title += f"{key}: {parameter[key]} "
    axis[row,col].set_title(title,fontsize=10)
    
    for line in voltage_lines:
        axis[row,col].plot(time_vals, line, label = line.name) 
    index+=1


axis[0,0].legend() 
plt.show()




# waveform_root_name = "pwl_waveform"
# VDD = 5
# cycle_count = 5
# frequencies = [1e+2,1e+3,1e+4,1e+5,1e+6,1e+7,1e+8,1e+9]

# parameters = pd.DataFrame(columns=['freq','trans','waveform_file','output_file'])

# for frequency in frequencies:
#     filename = f"{waveform_root_name}-{frequency}.csv"
#     transient_timing = ((1/ frequency) / 5)
    
#     generate_pwl_csv(filename, frequency, transient_timing,cycle_count=cycle_count, vdd=VDD)
    
#     parameters = parameters._append({
#         'freq': frequency,
#         'trans': transient_timing,
#         'waveform_file' : filename,
#         'output_file': f"{frequency}-response.csv"
#     }, ignore_index=True)

# print(parameters)
# parameters.to_csv("parameters.csv", index=False, sep=' ')