import json
from watson_developer_cloud import VisualRecognitionV3
import numpy as np
import cv2
import os
from zipfile import ZipFile
import requests
import argparse

ZIP_DIR = '/Applications/MAMP/htdocs/zips'

if not os.path.exists(ZIP_DIR):
	os.mkdir(ZIP_DIR)

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", required=True,
	help="input video")
ap.add_argument("-g", "--gps", required=True,
	help="geotag file")
args = vars(ap.parse_args())


body_cascade = cv2.CascadeClassifier('case.xml')
cap = cv2.VideoCapture(args['input'])

with open('api.key', 'r') as api:
	KEY = api.read()

visual_recognition = VisualRecognitionV3(
    '2018-09-16',
    iam_apikey=KEY)

with open(args['gps'], 'r') as gps:
	while(True):
		ret, img = cap.read()
		img = cv2.resize(img, (1280, 720))

		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

		bodies = body_cascade.detectMultiScale(gray, 1.3, 5)

		counter = 0
		for (x,y,w,h) in bodies:
			cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
			roi_gray = gray[y:y+h, x:x+w]
			roi_color = img[y:y+h, x:x+w]
			cv2.imshow('Drone Input', img)
			cv2.imwrite(os.path.join(ZIP_DIR, 'file_{0}.jpg'.format(counter)), roi_color)
			counter += 1

		with ZipFile('batch.zip', 'w') as myzip:
			for file in os.listdir(ZIP_DIR):
				myzip.write(os.path.join(ZIP_DIR, file))

		with open('batch.zip', 'rb') as images_file:
		    classes = visual_recognition.classify(
		        images_file,
		        threshold='0.7',
		        classifier_ids=["default"]).get_result()

		    flagged_images = []
		    for img in classes["images"]:
		    	for c in img["classifiers"][0]["classes"]:
		    		if c["class"] == "person":
		    			flagged_images.append(img["image"])

		    # TODO: Add 'geotagging'
		    if len(flagged_images) != 0:
				print "Adding images"
				image = flagged_images[0]
				gps_loc = gps.readline().split('\n')[0]
				gps_loc = gps_loc.split(', ')
				path = image.split('/')
				new_path = os.path.join("zips/", path[5])
				payload = {'lat' : str(gps_loc[0]), 'lng' : str(gps_loc[1]), 'img' : new_path}
				r = requests.post("http://localhost:3000/newmark", data=payload)

cv2.destroyAllWindows()
