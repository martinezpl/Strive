import cv2
import numpy as np
import matplotlib.pyplot as plt

# Encapsulate all the logic to detect faces and eyes in a function and apply it to live video using you webcam
def detect_face_eyes(image, face_classifier, eye_classifier):
    # Convert the image to grayscale
    img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Using the classifiers detect all faces on the image
    faces = face_classifier.detectMultiScale(img_gray, minNeighbors = 7)

    # Otherwise draw a rectangle on each face that has been detected
    for (x,y,w,h) in faces:
        face = img_gray[y:y+h, x:x+w]
        eyes = eye_classifier.detectMultiScale(face, minNeighbors = 7)
        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(image, (x+ex,y+ey), (x+ex+ew, y+ey+eh), (255,0,0), 2)
        cv2.rectangle(image, (x,y), (x+w, y+h), (0,255,0), 2)

    return image

if __name__ == "__main__":
    cap = cv2.VideoCapture(0)

    # FOR RECORDING
    #width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) + 0.5)
    #height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) + 0.5)
    #size = (width, height)
    #fourcc = cv2.VideoWriter_fourcc(*'XVID')
    #out = cv2.VideoWriter('test.avi', fourcc, 20.0, size)

    cv2.namedWindow('preview')
    cv2.moveWindow("preview", 2000, 100)

    face_classifier = cv2.CascadeClassifier('Haarcascades/haarcascade_frontalface_default.xml')
    eye_classifier = cv2.CascadeClassifier('Haarcascades/haarcascade_eye.xml')

    # try to get the first frame
    if cap.isOpened(): 
        rval, frame = cap.read()
    else:
        rval = False

    while rval:
        frame_f = detect_face_eyes(frame, face_classifier, eye_classifier)
        cv2.imshow("preview", frame_f)
        rval, frame = cap.read()
        #out.write(frame_f)
        key = cv2.waitKey(20)
        if key == 27:  # exit on ESC
            break

    cap.release()
    #out.release()
    cv2.destroyWindow("preview")
