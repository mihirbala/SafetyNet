import cv2
import time

hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
cap = cv2.VideoCapture("test_footage.mp4")
while True:
    r, frame = cap.read()
    if r:
        start_time = time.time()
        
        frame = cv2.resize(frame,(1280, 720)) # Downscale to improve frame rate
        #print frame.shape
        #quit()
        frame_1 = frame[0:360, 0:640]
        frame_2 = frame[0:360, 640:1280]
        frame_3 = frame[360:720, 0:640]
        frame_4 = frame[360:720, 640:1280]

        gray_frame_1 = cv2.cvtColor(frame_1, cv2.COLOR_RGB2GRAY) # HOG needs a grayscale image
        gray_frame_2 = cv2.cvtColor(frame_2, cv2.COLOR_RGB2GRAY)
        gray_frame_3 = cv2.cvtColor(frame_3, cv2.COLOR_RGB2GRAY)
        gray_frame_4 = cv2.cvtColor(frame_4, cv2.COLOR_RGB2GRAY)

        rects_1, weights_1 = hog.detectMultiScale(gray_frame_1, winStride=(2, 2), scale=1.5)
        rects_2, weights_2 = hog.detectMultiScale(gray_frame_1, winStride=(2, 2), scale=1.5)
        rects_3, weights_3 = hog.detectMultiScale(gray_frame_1, winStride=(2, 2), scale=1.5)
        rects_4, weights_4 = hog.detectMultiScale(gray_frame_1, winStride=(2, 2), scale=1.5)

        # Measure elapsed time for detections
        end_time = time.time()
        print("Elapsed time:", end_time-start_time)

        for i, (x, y, w, h) in enumerate(rects_1):
            if weights_1[i] < 0.7:
                continue
            cv2.rectangle(frame, (x,y), (x+w,y+h),(0,255,0),2)
        for i, (x, y, w, h) in enumerate(rects_2):
            if weights_2[i] < 0.7:
                continue
            cv2.rectangle(frame, (x,y+640), (x+w,y+640+h),(0,255,0),2)
        for i, (x, y, w, h) in enumerate(rects_3):
            if weights_3[i] < 0.7:
                continue
            cv2.rectangle(frame, (x+360,y), (x+360+w,y+h),(0,255,0),2)
        for i, (x, y, w, h) in enumerate(rects_4):
            if weights_4[i] < 0.7:
                continue
            cv2.rectangle(frame, (x+360,y+640), (x+360+w,y+640+h),(0,255,0),2)

        cv2.imshow("preview", frame)
    k = cv2.waitKey(1)
    if k & 0xFF == ord("q"): # Exit condition
        break
