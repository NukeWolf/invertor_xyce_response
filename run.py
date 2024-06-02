import pandas as pd
from matplotlib import pyplot as plt
import subprocess
import os.path

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
    


# Run Xyce Sim
result_file_name = "result"
cir_file = "invertor_freq_response.cir"
if (not os.path.isfile("result.prn")):
    out = subprocess.check_output(["xyce", cir_file])
    print(out)

df = pd.read_table("invertor_freq_response.cir.res",sep="\s+")
print(df)


# Plot results
df = pd.read_csv("invertor_freq_response.cir.csv")
print(df)
num_cols = range(1,df.shape[1])

x_vals = df.iloc[:,0]
lines = [df.iloc[:,x] for x in num_cols]
  
  
  
figure, axis = plt.subplots(2, 2) 

# plot lines 
for line in lines:
    plt.plot(x_vals, line, label = line.name) 

plt.legend() 
plt.show()
