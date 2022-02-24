# Mic Recording Script
#HEY BRYCE!

def mic():
	from adafruit_ads1x15.analog_in import AnalogIn
	from adafruit_ads1x15.ads1x15 import Mode
	import adafruit_ads1x15.ads1115 as ADS

	from time import time, sleep
	import datetime
	import board
	import busio
	import socket

	# I'm using this line instead after setting the baudrate manually in /boot/config.txt
	i2c = busio.I2C(board.SCL, board.SDA)

	ads = ADS.ADS1115(i2c)
	ads.data_rate = 475		# 8, 16, 32, 64, 128, 250, 475, 860
	ads.gain = 1
	ads.mode = Mode.CONTINUOUS

	chan = AnalogIn(ads, ADS.P0, ADS.P1)		# differential voltage, channels 0 & 1 specified by JFA on his Github
	s = 2		# seconds of recording

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
	launch_time = datetime.datetime.now()
	print(f'Start time = {launch_time} \n Duration = {s}s \n Reading...\n')

	# act_duration = 0.0000	# used for testing - BL

	try:
		while 1:
			for j in range(80):
				start = time()
				print(f'Start time = {launch_time} \n Duration = {s}s \n Reading...\n')
				while (time()-start) < s:
					# print(time(), chan.voltage)	# this printing statement slow the code WAAAAY too much
					dat.append([time(), chan.voltage])
					# act_duration = time()-start	# used for testing - BL
					# sleep(0.0025)		# used for testing - BL

				# data = pd.DataFrame(dat,columns = ['Time','Signal']) # used this for testing - BL
				for d in dat:
					f.write(str(d[0]) + ',' + str(d[1]) + '\n')
				dat = []
				f.close()
				# print(data)	# used this for testing - BL
				launch_time = datetime.datetime.now()
				timestr = launch_time.strftime("%Y_%m_%d_%H_%M_%S")
				micPath = (f'/home/pi/Documents/glinda2_proto/dataFiles/{device_hostname}_data/'
					f'{device_hostname}_micData_{timestr}.csv')
	except KeyboardInterrupt:
		f.close()
		print('\n Done Writing \n')
	except:
		print('ERROR')
		pass
# data.to_csv("testingmic.csv",header=['Time (s)','Signal (V)']) # used for testing - BL

# used this for testing - BL
# os.system('cd ~/Documents/glinda2_proto/gitcodes; git add testingmic.csv; git commit -m "autopush data from pi"; git push')


if __name__ == '__main__':
	mic()








