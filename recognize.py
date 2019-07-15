# import library
import cv2
import numpy as np
import matplotlib.pyplot as plt
import pickle

capture = cv2.VideoCapture(0)

haar_cascade = cv2.CascadeClassifier('cascades/haarcascade_frontalface_alt2.xml')
eyes_cascade = cv2.CascadeClassifier('cascades/haarcascade_eye.xml')

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainner.yml')

labels = {}
with open('labels.pickle', 'rb') as f:
    og_labels = pickle.load(f)
    labels = {v:k for k, v in og_labels.items()}


while(True):
    # Capture frame by frame
    rect, frame = capture.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = haar_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)
    for (x, y, w, h) in faces:
        # Region of interest(ROI)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]
        # img_item = 'lafa.png'
        # img_item_color = '5.jpg'
        # cv2.imwrite(img_item, roi_gray)
        # cv2.imwrite(img_item_color, roi_color)

        # recognize? deep learned model predict keras tensorflow pytorch scikit learn
        id_, conf = recognizer.predict(roi_gray)
        color = (255, 255, 255)
        stroke = 2
        if conf >=45 and conf<=85:
            # print(labels[id_])
            font = cv2.FONT_HERSHEY_SIMPLEX
            name = labels[id_]
            cv2.putText(frame, name, (x, y), font, 1, color, stroke, cv2.LINE_AA)
        else:
            cv2.putText(frame, 'Unknown', (x, y), font, 1, color, stroke, cv2.LINE_AA)


        color = (255, 0, 0) # BGR
        stroke = 2
        end_cord_x = x+w
        end_cord_y = y+h
        cv2.rectangle(frame, (x, y), (end_cord_x, end_cord_y), color, stroke)

        subitems = eyes_cascade.detectMultiScale(roi_gray)
        for (ex,ey,ew,eh) in subitems:
        	cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

    # Display the resulting frame
    cv2.imshow('Frame', frame)
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break
    
# when everything done, release the capture
capture.release()
cv2.destroyAllWindows()