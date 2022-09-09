import os

import board
import busio
import adafruit_adxl34x
from time import time, sleep
import socket
import datetime
import traceback

def main():
	i2c = busio.I2C(board.SCL, board.SDA)
	accel = adafruit_adxl34x.ADXL345(address=0x53, i2c=i2c)
	SR=800
	accel.DataRate=SR
	s = 30	# seconds of recording

	device_hostname = socket.gethostname()
	launch_time = datetime.datetime.now()
	timestr = launch_time.strftime("%Y_%m_%d_%H_%M_%S")

	cwd = os.getcwd()
	micPath = (os.path.join(cwd, 'test_data',
		f'TESTDATA_{device_hostname}_accData_{timestr}.csv'))
	f = open(micPath, 'a+')
	f.write('Time_s' + ',' + 'accx_mps2' + ',' + 'accy_mps2' + ',' + 'accz_mps2' '\n')
	time_end = time()+s
	dat=[]
	try:
		while (time()) < time_end:
			dat.append([time(), accel.acceleration[0], accel.acceleration[1], accel.acceleration[2]])
			sleep(1/sample_rate)
		for d in dat:
			f.write(str(d[0]) + ',' + str(d[1]) + ',' + str(d[2]) + ',' + str(d[3]) + '\n')
		f.close()
	except KeyboardInterrupt:
		# f.close()
		print('\n Done Writing \n')
	except:
		print(f'ERROR at {time()} \n {traceback.format_exc()}')
		pass

if __name__ == "__main__":
	main()