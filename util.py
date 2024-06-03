import pandas as pd
# PWL Generator
def generate_pwl_csv(filename, frequency, transient_timing, cycle_count=5, vdd=5, gnd=0):
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

def format_frequency(frequency):
    if frequency >= 1e9:  # If frequency is greater than or equal to 1 GHz
        formatted_frequency = f'{frequency / 1e9:.2f} GHz'
    elif frequency >= 1e6:  # If frequency is greater than or equal to 1 MHz
        formatted_frequency = f'{frequency / 1e6:.2f} MHz'
    else:
        formatted_frequency = f'{frequency} Hz'
    return formatted_frequency