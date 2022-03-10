# Mic Recording Script
#DOES THIS SHOW  - 3/10 11:01
import sys


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

	# I'm using this line instead after setting the baudrate manually in /boot/config.txt
	i2c = busio.I2C(board.SCL, board.SDA)

	ads = ADS.ADS1115(i2c)
	sample_rate = 860
	ads.data_rate = sample_rate		# 8, 16, 32, 64, 128, 250, 475, 860
	ads.gain = 1
	ads.mode = Mode.CONTINUOUS

	chan = AnalogIn(ads, ADS.P0, ADS.P1)		# differential voltage, channels 0 & 1 specified by JFA on his Github
	s = 15		# seconds of recording

	device_hostname = socket.gethostname()
	launch_time = datetime.datetime.now()
	timestr = launch_time.strftime("%Y_%m_%d_%H_%M_%S")
	micPath = (f'/home/pi/Documents/glinda2_proto/dataFiles/{device_hostname}_data/'
		f'{device_hostname}_micData_{timestr}.csv')
	f = open(micPath, 'a+')
	dat = []
	#looptime = time()
		#try:

	# sleep(5)		# used for testing - BL
	#launch_time = datetime.datetime.now()
	#print(f'Start time = {launch_time} \n Duration = {s}s \n Reading...\n')

	#gain, native_sens = 107.38, 0.000022	# used for testing
	#act_duration = 0.0000	# used for testing - BL
	try:
		while True:
			#for j in range(80):
			start = time()
			#print(f'Start time = {launch_time} \n Duration = {s}s \n Reading...\n')
			while (time()-start) < s:
				# this printing statement slows the code WAAAAY too much. Only use for testing.
				# print(time(), gain*chan.voltage/native_sens) used for testing

				dat.append([time(), chan.voltage])
				# act_duration = time()-start	# used for testing - BL
				sleep(1/sample_rate)		# used for testing - BL

			data = pd.DataFrame(dat,columns = ['Time','Signal']) # used this for testing - BL
			data.to_csv("testingmic.csv", header=['Time (s)', 'Signal (V)'])  # used for testing - BL
			quit()

			# for d in dat:
			# 	f.write(str(d[0]) + ',' + str(d[1]) + '\n')
			# dat = []
			# f.close()
			# launch_time = datetime.datetime.now()
			# timestr = launch_time.strftime("%Y_%m_%d_%H_%M_%S")
			# micPath = (f'/home/pi/Documents/glinda2_proto/dataFiles/{device_hostname}_data/'
			# 	f'{device_hostname}_micData_{timestr}.csv')
			# f = open(micPath, 'a+')

	except KeyboardInterrupt:
		f.close()
		print('\n Done Writing \n')
	except:
		print(f'ERROR at {time()}')
		pass


# used this for testing - BL
# os.system('cd ~/Documents/glinda2_proto/gitcodes; git add testingmic.csv; git commit -m "autopush data from pi"; git push')

if __name__ == '__main__':
	mic()









