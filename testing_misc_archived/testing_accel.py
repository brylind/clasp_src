import board
import busio
import adafruit_adxl34x
from time import time
import socket
import datetime

def main():
	i2c = busio.I2C(board.SCL, board.SDA)
	accel = adafruit_adxl34x.ADXL345(address=0x53, i2c=i2c)
	sample_rate = 500

	s = 30	# seconds of recording

	device_hostname = socket.gethostname()
	launch_time = datetime.datetime.now()
	timestr = launch_time.strftime("%Y_%m_%d_%H_%M_%S")

	micPath = (os.path.join(cwd,
		f'TESTDATA_{device_hostname}_accData_{timestr}.csv'))
	f = open(micPath, 'a+')
	f.write('Time_s' + ',' + 'accx_mps2' + ',' + 'accy_mps2' + ',' + 'accz_mps2' '\n')

	start = time()
	try:
		while (time()-start) < s:
			f.write(str(time()) + ',' + str(chan.voltage) + '\n')
			sleep(1/sample_rate)
		f.close()
	except KeyboardInterrupt:
		# f.close()
		print('\n Done Writing \n')
	except:
		print(f'ERROR at {time()}')
		pass

if __name__ == "__main__":
	main()