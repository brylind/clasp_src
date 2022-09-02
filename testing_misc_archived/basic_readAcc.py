import board
import adafruit_adxl34x
from time import time
import busio

def main():

	# dat = [[1,2,3,4]]
	# dat.append([5,6,7,8])


	i2c = busio.I2C(board.SCL, board.SDA)
	accel = adafruit_adxl34x.ADXL345(address=0x53, i2c=i2c)
	SR=100
	accel.DataRate=SR
	s = 3	# seconds of recording

	# dat=[['Time_s', 'accx_g','accy_g','accz_g']]
	dat=[]
	# dat.append('Time_s'+','+'accx_g'+','+'accy_g'+','+'accz_g \n')
	start = time()
	t_end = time()+s
	while time() < t_end:
		dat.append([time(), accel.acceleration[0], accel.acceleration[1], accel.acceleration[2]])

	print('Done Recording \n')
	print(len(dat),'\n \n')
	init_SR = 1/(dat[1][0]-dat[0][0])
	total_SR = len(dat)/(dat[-1][0]-dat[0][0])
	print(f'Total time recording took place: {dat[-1][0]-dat[0][0]} \n')
	print(f'Sample rate for initial points: {init_SR} \n')
	print(f'Sample rate for entire file: {total_SR}')


main()
