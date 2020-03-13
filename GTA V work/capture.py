import numpy as np
from PIL import ImageGrab
import cv2
import time
from directkeys import PressKey, W, A, S, D, ReleaseKey
import pyautogui

def roi(img, vertices):
	mask = np.zeros_like(img)
	cv2.fillPoly(mask, vertices, 255)
	masked = cv2.bitwise_and(img,mask)
	return masked

def draw_lines(img, lines):
	try:
		for line in lines:
			coords= line[0]
			cv2.line(img, (coords[0],coords[1]), (coords[2],coords[3]), [255,255,255], 3)
	except:
		pass

def process_img(original_image):
	processed_img = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
	processed_img = cv2.Canny(processed_img, threshold1=200, threshold2=300)
	processed_img = cv2.GaussianBlur(processed_img,(5,5),0)

	vertices = np.array([[10,700],[10,400],[400,200],[800,200],[1000,400],[1000,700]])
	processed_img = roi(processed_img,[vertices])

	lines = cv2.HoughLinesP(processed_img, 1, np.pi/180, 180, np.array([]), 100, 5)
	draw_lines(processed_img, lines)

	return processed_img


def main():
	last_time=time.time()
	while(True):
		screen= np.array(ImageGrab.grab(bbox=(0,40,1024,810)))
		new=process_img(screen)
		# print('down')
		# PressKey(W)
		# time.sleep(3)
		# print('up')
		# ReleaseKey(W)
		#print("Loop took {} seconds".format(time.time()-last_time))
		last_time=time.time()

		cv2.imshow('window',new)
	#	cv2.imshow('window',cv2.cvtColor(screen, cv2.COLOR_BGR2RGB))
		if cv2.waitKey(25) & 0xFF==ord('q'):
			cv2.destroyAllWindows()
			break

main()
