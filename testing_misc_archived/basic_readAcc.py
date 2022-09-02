import board
import adafruit_adxl34x
from time import time
import busio

def main():

	i2c = busio.I2C(board.SCL, board.SDA)
	accel = adafruit_adxl34x.ADXL345(address=0x53, i2c=i2c)
	accel.DataRate=3200
	s = 20	# seconds of recording

	dat=[]
	dat.append('Time_s'+','+'accx_g'+','+'accy_g'+','+'accz_g')
	start = time()
	t_end = time()+s
	while time() < t_end:
		dat.append(time(), accel.acceleration[0], accel.acceleration[1], accel.acceleration[2])
	print('Done Recording \n')
	init_SR = 1/(dat[2,1]-dat[1,1])
	total_SR = height(dat)/(dat[-1,1]-dat[0,1])
	print(f'Total time recording took place: {dat[-1,1]-dat[0.1]}')
	print(f'Sample rate for initial points: {init_SR} \n')
	print(f'Sample rate for entire file: {total_SR}')


main()
