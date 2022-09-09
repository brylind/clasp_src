# Mic Recording Script
#DOES THIS SHOW  - 3/11 2:55
import os
import urllib.request


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

	cwd = os.getcwd()
	# I'm using this line instead after setting the baudrate manually in /boot/config.txt
	i2c = busio.I2C(board.SCL, board.SDA)

	ads = ADS.ADS1115(i2c)
	sample_rate = 250
	ads.data_rate = sample_rate		# 8, 16, 32, 64, 128, 250, 475, 860
	ads.gain = 1
	ads.mode = Mode.CONTINUOUS

	chan = AnalogIn(ads, ADS.P0, ADS.P1)		# differential voltage, channels 0 & 1 specified by JFA on his Github
	s = 10		# seconds of recording

# --------------------------------------------------------------------
## testing with writing directly to file (instead of temporarily storing in "dat")
	device_hostname = socket.gethostname()
	launch_time = datetime.datetime.now()
	timestr = launch_time.strftime("%Y_%m_%d_%H_%M_%S")
	# micPath = (f'/home/pi/glinda_main/dataFiles/mic/'
	# 	f'{device_hostname}_micData_{timestr}.csv')
	micPath = (os.path.join(cwd,'test_data',
		f'TESTDATA_{device_hostname}_micData_{timestr}.csv'))
	f = open(micPath, 'a+')
	f.write('Time_s' + ',' + 'Signal_V' + '\n')

# TODO: try doing f.append instead of opening, writing, closing

	start = time()
	try:
		while (time()-start) < s:
			if ads._conversion_complete()==1:	# testing this
				ads.get_last_result()
				f.write(str(time()) + ',' + str(chan.voltage) + '\n')
			else:
				pass
			# sleep(1/sample_rate)
		f.close()
	except KeyboardInterrupt:
		# f.close()
		print('\n Done Writing \n')
	except:
		print(f'ERROR at {time()}')
		pass

# --------------------------------------------------------------------


# --------------------------------------------------------------------
# testing with writing to a temporary variable first
# 	dat = []
# 	start = time()
# 	try:
# 		while (time()-start) < s:
# 			dat.append([time(), chan.voltage])
# 			sleep(1/sample_rate)
#
# 		####################### used for testing
# 		data = pd.DataFrame(dat,columns = ['Time','Signal']) 	# used this for testing - BL
# 		data.to_csv("testingmic.csv", header=['Time_s', 'Signal_V'])  # used for testing - BL
# 		sleep(2)
#
# 		os.system('git add "testingmic.csv"; git commit -m "added testingmic.csv"; git push')
# 		quit()
#
# 	except KeyboardInterrupt:
# 		# f.close()
# 		print('\n Done Writing \n')
# 	except:
# 		print(f'ERROR at {time()}')
# 		pass
# --------------------------------------------------------------------

if __name__ == '__main__':
	mic()









