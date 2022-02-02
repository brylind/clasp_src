import os

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from scipy.fft import rfft, rfftfreq




#df_imported = pd.read_csv("~/Documents/OneDrive - Oklahoma A and M System/Research/Infrasound/GLINDA and Brandons work/testingmic.csv")
df_imported = pd.read_csv("~/Documents/Github/GLINDA2_testing/testingmic.csv")
time = df_imported['Time (s)'].values
signal_ugly = df_imported['Signal (V)'].values
signal = signal_ugly-np.mean(signal_ugly)

firsttime = time[1]
lasttime = time[-1]
totaltime=lasttime-firsttime

N = int(len(time))
sample_rate = len(time)/(lasttime - firsttime)

yf = rfft(signal)
xf = rfftfreq(N, 1/sample_rate)

plt.plot(time,signal)
plt.show()

#plt.semilogx(xf, np.abs(yf))
plt.plot(xf[100:-1], np.abs(yf)[100:-1])
plt.grid()
plt.show()

# does this show?

#os.system('cd ~/Documents/Github/GLINDA2_testing; git add .; git commit -m "auto push from Pycharm code"; git push')
