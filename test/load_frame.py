import cv2

cap = cv2.VideoCapture('test_footage.mp4')

while(True):
    ret, frame = cap.read()
    frame = cv2.resize(frame, (1280, 720))
    #cv2.imshow('Frame', frame)
    #cv2.waitKey(0)
    cv2.imwrite('test_frame.jpg', frame)

