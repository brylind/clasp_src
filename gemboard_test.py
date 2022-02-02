# Mic Recording Script
#HEY BRYCE!
import os

from adafruit_ads1x15.analog_in import AnalogIn
from adafruit_ads1x15.ads1x15 import Mode
import adafruit_ads1x15.ads1115 as ADS

from time import time, sleep
import datetime
import board
import busio
import pandas as pd
import numpy as np

i2c = busio.I2C(board.SCL, board.SDA)   # I'm using this line instead after setting the baudrate manually in /boot/config.txt

ads = ADS.ADS1115(i2c)
ads.data_rate = 475
ads.gain = 1
#ads.mode = Mode.CONTINUOUS

chan = AnalogIn(ads, ADS.P0, ADS.P1) #differential voltage, channels 0 & 1 specified by JFA on his Github



#timestr = launch_time.strftime("%Y_%m_%d_%H_%M_%S")
#micPath = "/home/pi/infrasound/dataFiles/micData" + timestr + ".csv"
#f = open(micPath,'a+')
dat = []
#looptime = time()
    #try:

s = 300 # seconds of recording
launch_time = datetime.datetime.now()
print(f'Start time = {launch_time} \n Duration = {s}s \n Reading...\n')

act_duration = 0.0000
start = time()

while (time()-start) < s:
	#print(time(), chan.voltage)	# this printing statement slow the code WAAAAY too much
	dat.append([time(), chan.voltage])
	#act_duration = time()-start
	sleep(0.0025)		# sleep set to make a sampling rate of 1/.004 = 250
data = pd.DataFrame(dat,columns = ['Time','Signal'])
#print(data)
data.to_csv("testingmic.csv",header=['Time (s)','Signal (V)'])

os.system('cd ~/Documents/glinda2_proto/gitcodes; git add testingmic.csv; git commit -m "autopush data from pi"; git push')


