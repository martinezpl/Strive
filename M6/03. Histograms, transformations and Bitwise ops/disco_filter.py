import cv2
import numpy as np

def disco_filter(frame, key):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, np.array([0, 0, 40]), np.array([180, 50, 255]))
    frame[mask == key] = np.random.randint(0, 255, 3)
    return frame

if __name__ == "__main__":
    keyo = 255

    cv2.namedWindow("preview")
    cv2.moveWindow("preview", 2000, 100)
    
    cap = cv2.VideoCapture(0)
    # FOR RECORDING
    #width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) + 0.5)
    #height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) + 0.5)
    #size = (width, height)
    #fourcc = cv2.VideoWriter_fourcc(*'XVID')
    #out = cv2.VideoWriter('dance.avi', fourcc, 20.0, size)
    
    if cap.isOpened():  # try to get the first frame
        rval, frame = cap.read()
    else:
        rval = False
    
    while rval:
        frame_f = disco_filter(frame, keyo)
        cv2.imshow("preview", frame_f)
        rval, frame = cap.read()
        #out.write(frame_f)
        key = cv2.waitKey(20)
        if key == 27:  # exit on ESC
            break

        if keyo:
            keyo = 0
        else:
            keyo = 255
    cap.release()
    #out.release()
    cv2.destroyWindow("preview")
