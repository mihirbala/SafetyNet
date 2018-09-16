import json
from watson_developer_cloud import VisualRecognitionV3
import numpy as np
import cv2
import os
from zipfile import ZipFile
import requests

ZIP_DIR = 'zips'

if not os.path.exists(ZIP_DIR):
	os.mkdir(ZIP_DIR)

body_cascade = cv2.CascadeClassifier('case.xml')
cap = cv2.VideoCapture("test_footage.mp4")

with open('api.key', 'r') as api:
	KEY = api.read()

visual_recognition = VisualRecognitionV3(
    '2018-09-16',
    iam_apikey=KEY)

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
	    
	    flagged_images = []
	    for img in classes["images"]:
	    	for c in img["classifiers"][0]["classes"]:
	    		if c["class"] == "person":
	    			flagged_images.append(c["image"])

	    # TODO: Add 'geotagging'
	    for image in flagged_images:
	        gps_loc = [35.802887, 139.094066]
	        payload = {'lat' : str(gps_loc[0]), 'lng' : str(gps_loc[1]), 'img' : image}
	        r = requests.post("http://localhost:3000/newmark", data=payload)

cv2.destroyAllWindows()
