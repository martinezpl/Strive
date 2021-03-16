'''
Create a classifier to detect cars in an image
If at least one car was detected write Car Detected (in Green) on top of the image, otherwise write No car detected (in Red)
Save the image to disk
Show the image result inside the notebook
Make it work with a video
Put a bounding box around the cars detected
Get a higher resolution video and extract the car plates and save them to disk
'''
import cv2

def detect_cars(image, classifier):
    # Convert the image to grayscale
    img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Using the classifiers detect all cars on the image
    cars = classifier.detectMultiScale(img_gray, minNeighbors = 4, minSize = (20, 20))

    # Draw a rectangle on each car that has been detected
    for (x,y,w,h) in cars:
        cv2.rectangle(image, (x,y), (x+w, y+h), (0,255,0), 2)
        #cv2.putText(image, f"{w * h}", (x,y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 1)

    return image

if __name__ == "__main__":
    cap = cv2.VideoCapture('videos/video.avi')

    # FOR RECORDING
    #width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) + 0.5)
    #height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) + 0.5)
    #size = (width, height)
    #fourcc = cv2.VideoWriter_fourcc(*'XVID')
    #out = cv2.VideoWriter('test.avi', fourcc, 20.0, size)

    cv2.namedWindow('preview')
    cv2.moveWindow("preview", 2000, 100)

    car_classifier = cv2.CascadeClassifier('haarcascade_car.xml')

    while cap.isOpened():
        rval, frame = cap.read()
        frame_f = detect_cars(frame, car_classifier)
        cv2.imshow("preview", frame_f)
        #out.write(frame_f)
        key = cv2.waitKey(20)
        if key == 27:  # exit on ESC
            break

    cap.release()
    #out.release()
    cv2.destroyWindow("preview")
