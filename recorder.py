import cv2
import os
from detector import detect_objects

def capture():
   # Initializing capture & source 
    cap = cv2.VideoCapture(0)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')  # Codec for AVI files
    out = cv2.VideoWriter('Camera-01-footage.mp4', fourcc, 20.0, (640, 480))

    # Creating loop to view footage
    while (cap.isOpened):
        ret, frame = cap.read()
        detected_frame = detect_objects(frame)
        
        # Viewing the footage 
        cv2.imshow("Camera-01",frame)

        # Output code(saves the footage)
        if ret == True:
            out.write(frame)    
        if cv2.waitKey(1) &0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
