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

		ys=[]
		for i in lines:
			for ii in i:
				ys += [ii[1],ii[3]]
		min_y = min(ys)
		max_y = 810
		new_lines=[]
		line_dict={}

		for idx,i in enumerate(lines):
			for xyxy in i:
				x_coords = (xyxy[0],xyxy[2])
				y_coords = (xyxy[1],xyxy[3])
				A = vstack([x_coords,ones(len(x_coords))]).T
				m, b = lstsq(A, y_coords)[0]

				x1 = (min_y-b)/m
				x2 = (max_y-b)/m

				line_dict[idx] = [m, b, [int(x1), min_y, int(x2), max_y]]
				new_lines.append([int(x1), min_y, int(x2), max_y])

		final_lanes = {}

		for idx in line_dict:
			final_lanes_copy = final_lanes.copy()
			m = line_dict[idx][0]
			b = line_dict[idx][1]
			line = line_dict[idx][2]

			if len(final_lanes) == 0:
				final_lanes[m] = [ [m, b, line] ]

			else:
				found_copy = False
				for other_ms in final_lanes_copy:

					if not found_copy:
						if(abs(other_ms*1.1) > abs(m) > abs(other_ms*0.9)):
							if(abs(final_lanes_copy))

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
		print("FPS:".format(1/time.time()-last_time))
		last_time=time.time()

		cv2.imshow('window',new)
	#	cv2.imshow('window',cv2.cvtColor(screen, cv2.COLOR_BGR2RGB))
		if cv2.waitKey(25) & 0xFF==ord('q'):
			cv2.destroyAllWindows()
			break

main()
