import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from scipy.fft import rfft, rfftfreq




df_imported = pd.read_csv("~/Documents/OneDrive - Oklahoma A and M System/Research/Infrasound/GLINDA and Brandons work/testingmic.csv")
time = df_imported['Time (s)'].values
signal_ugly = df_imported['Signal (V)'].values
signal = signal_ugly-np.mean(signal_ugly)

firsttime = time[1]
lasttime = time[-1]

N = int(len(time))
sample_rate = len(time)/(lasttime - firsttime)

yf = rfft(signal)
xf = rfftfreq(N, sample_rate)

plt.plot(time,signal)
plt.show()

plt.plot(xf, np.abs(yf))
plt.grid()
plt.show()
