import json
from watson_developer_cloud import VisualRecognitionV3
import numpy as np
import cv2
import os
from zipfile import ZipFile

ZIP_DIR = 'zips'

if not os.path.exists(ZIP_DIR):
	os.mkdir(ZIP_DIR)

body_cascade = cv2.CascadeClassifier('case.xml')
cap = cv2.VideoCapture("test_footage.mp4")

with open('../api.key', 'r') as api:
	KEY = api.read()
print KEY
visual_recognition = VisualRecognitionV3(
    '2018-09-15',
    iam_apikey='dFY891_ScRYAqVjkL6CON1D8qBINC7PJgwg-ZvMarHzG')

while(True):
	ret, img = cap.read()
	img = cv2.resize(img, (1280, 720))

	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

	bodies = body_cascade.detectMultiScale(gray, 1.3, 5)
	
	counter = 0
	for (x,y,w,h) in bodies:
		#cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
		roi_gray = gray[y:y+h, x:x+w]
		roi_color = img[y:y+h, x:x+w]
		cv2.imwrite(os.path.join(ZIP_DIR, 'file_{0}.jpg'.format(counter)), roi_color)
		counter += 1

	with ZipFile('batch.zip', 'w') as myzip:
		for file in os.listdir(ZIP_DIR):
			myzip.write(os.path.join(ZIP_DIR, file))

	with open('batch.zip', 'rb') as images_file:
	    classes = visual_recognition.classify(
	        images_file,
	        threshold='0.6',
	        classifier_ids=["default"]).get_result()
	
	gps_loc = [35.802887, 139.094066]


	#cv2.imshow('img',img)
	#cv2.waitKey(0)

cv2.destroyAllWindows()