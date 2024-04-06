import pandas as pd
from matplotlib import pyplot as plt
import subprocess

# PWL Generator
def generate_pwl_csv(filename, frequency, transient_timing, cycle_count=5, vdd=0.7, gnd=0):
    """
    Generates a PWL CSV file with the given frequency and transient timing.

    Parameters:
        filename (str): The name of the PWL CSV file to be generated.
        frequency (float): The frequency of the waveform.
        transient_timing (float): The transient timing (in seconds).
        cycle_count (int): Amount of activations

    Returns:
        None
    """
    # Generate time points
    period = 1 / frequency
    time_points = []
    voltage_values = []
    # Generate voltage values (example sinusoidal waveform)
    for x in range(cycle_count):
        start_time = period*x
        half_time = start_time + (period/2)
        
        time_points.append(start_time)
        time_points.append(start_time + transient_timing)
        time_points.append(half_time)
        time_points.append(half_time + transient_timing)
        
        voltage_values.append(gnd)
        voltage_values.append(vdd)
        voltage_values.append(vdd)
        voltage_values.append(gnd)
        
    # Create a DataFrame with time and voltage columns
    pwl_df = pd.DataFrame({'Time': time_points, 'Voltage': voltage_values})

    # Write DataFrame to CSV
    pwl_df.to_csv(filename, index=False, header=None, sep=' ')

    print(f"PWL CSV file '{filename}' generated successfully.")

# Example usage:
filename = "pwl_waveform.csv"
frequency = 2e+9  # Hz
transient_timing = ((1/ frequency) / 5)

generate_pwl_csv(filename, frequency, transient_timing,vdd=1)


# Run Xyce Sim
cir_file = "invertor_freq_response.cir"
out = subprocess.check_output(["xyce", cir_file])
print(out)



df = pd.read_csv("invertor_freq_response.cir.csv")
num_cols = range(1,df.shape[1])

x_vals = df.iloc[:,0]
lines = [df.iloc[:,x] for x in num_cols]
  
# plot lines 
for line in lines:
    plt.plot(x_vals, line, label = line.name) 

plt.legend() 
plt.show()
