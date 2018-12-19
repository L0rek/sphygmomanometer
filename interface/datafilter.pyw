import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from tkinter.filedialog import *

fs = 1/0.025  # Sampling frequency
# Generate the time vector properly

filename = "data21_24.txt"
file = open(filename, "r")
file.readline()
data_list=np.array([0, 0, 0], dtype='float32')
for line in file:
    line = line.split("\t")
    line = np.array([float(line[0]), float(line[1]), float(line[2])])
    data_list = np.vstack([data_list, line])
file.close()

signalp = data_list[1:, 1]
signall = data_list[1:, 2]
output=np.array(data_list[1:])
#plt.plot(t, signalp, label='pressure')
#plt.plot(t, signall, label='illuminance')

fc = 3  # Cut-off frequency of the filter
fl= 0.4
w1 = fl / (fs / 2) # Normalize the frequency
w2 = fc / (fs / 2) # Normalize the frequency
b, a = signal.butter(4, (w1,w2), 'bandpass')

output[0:,2]=(signal.filtfilt(b, a, signall)) #-output[0:,1]*0.20
file = open("out_"+filename, "w")
file.write("time [ms]\tPressure [Hgmm]\tilluminance [lux]\n")
for row in output:
    file.write(np.array2string(row, formatter={'float_kind': lambda x: "%.2f" % x}, precision=3, separator=' \t ').replace('[', '').replace(']', '') + "\n")
file.close()
output[0:,1]=(signal.filtfilt(b, a, signalp))
plt.subplot(221)
plt.title('pressure')
plt.plot(data_list[1:,0], data_list[1:,1], label='filtered pressure')
plt.subplot(222)
plt.title('illuminance')
plt.plot(data_list[1:,0], data_list[1:,2], label='filtered pressure')
plt.subplot(223)
plt.title('filtered pressure')
plt.plot(output[0:,0], output[0:,1], label='filtered pressure')
plt.subplot(224)
plt.title('filtered illuminance')
plt.plot(output[0:,0], output[0:,2], label='filtered illuminance')
plt.show()