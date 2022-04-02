# Mic Recording Script
#DOES THIS SHOW  - 3/11 2:55


def mic():
	from adafruit_ads1x15.analog_in import AnalogIn
	from adafruit_ads1x15.ads1x15 import Mode
	import adafruit_ads1x15.ads1115 as ADS
	import pandas as pd


	from time import time, sleep
	import datetime
	import board
	import busio
	import socket
	import sys
	import urllib.request

	# I'm using this line instead after setting the baudrate manually in /boot/config.txt
	i2c = busio.I2C(board.SCL, board.SDA)

	ads = ADS.ADS1115(i2c)
	sample_rate = 250
	ads.data_rate = sample_rate		# 8, 16, 32, 64, 128, 250, 475, 860
	ads.gain = 1
	ads.mode = Mode.CONTINUOUS

	chan = AnalogIn(ads, ADS.P0, ADS.P1)		# differential voltage, channels 0 & 1 specified by JFA on his Github
	s = 20		# seconds of recording

	device_hostname = socket.gethostname()
	launch_time = datetime.datetime.now()
	timestr = launch_time.strftime("%Y_%m_%d_%H_%M_%S")
	try:
		urllib.request.urlopen('http://google.com', None, timeout=5.1)
		internet = ''
	except:
		internet = 'NOINT_'
	micPath = (f'/home/pi/glinda_main/dataFiles/mic/'
		f'{internet}{device_hostname}_micData_{timestr}.csv')
	f = open(micPath, 'a+')
	dat = []
	try:
		while True:
			start = time()
			while (time()-start) < s:
				dat.append([time(), chan.voltage, internet])
				sleep(1/sample_rate)
			############################################## used for testing
			# data = pd.DataFrame(dat,columns = ['Time','Signal']) # used this for testing - BL
			# data.to_csv("testingmic.csv", header=['Time (s)', 'Signal (V)'])  # used for testing - BL
			# quit()
			##################################################################
			f.write('Time_s' + ',' + 'Signal_V' + ',' + 'Internet_status' + '\n')
			for d in dat:
				f.write(str(d[0]) + ',' + str(d[1]) + ',' + str(d[2]) + '\n')
			dat = []
			f.close()
			launch_time = datetime.datetime.now()
			timestr = launch_time.strftime("%Y_%m_%d_%H_%M_%S")
			try:
				urllib.request.urlopen('http://google.com', None, timeout=5.1)
				internet = ''
			except:
				internet = 'NOINT_'
			micPath = (f'/home/pi/glinda_main/dataFiles/mic/'
				f'{internet}{device_hostname}_micData_{timestr}.csv')
			f = open(micPath, 'a+')			

	except KeyboardInterrupt:
		f.close()
		print('\n Done Writing \n')
	except:
		print(f'ERROR at {time()}')
		pass


if __name__ == '__main__':
	mic()









