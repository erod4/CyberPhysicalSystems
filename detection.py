import cv2
import numpy as np
from picamera2 import Picamera2

picam2 = None
face_cascade = None

def VIDEO_INIT():
    global picam2, face_cascade
    # Initialize the Picamera2 instance
    picam2 = Picamera2()
    config = picam2.create_preview_configuration(main={"size": (640, 480)})
    picam2.configure(config)
    picam2.start()
    
    # Load the Haar cascade for frontal face detection
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    if face_cascade.empty():
        raise Exception("Could not load face cascade classifier.")

def VIDEO_DEINIT():
    global picam2
    # picam2.stop()
    cv2.destroyAllWindows()

def PROCESS_FRAME():
    # global picam2, face_cascade
    frame = picam2.capture_array()

    # convert from RGB to BGR for OpenCV
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    
    # Convert the frame to grayscale 
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)
    parameters =cv2.aruco.DetectorParameters()

    #create ArUco detector
    detector = cv2.aruco.ArucoDetector(aruco_dict,parameters)
a,b,c=[x,y,z]
    #detect the markers
    corners, ids, rejected =detector.detectMarkers(gray)
    x,y =-1,-1
    if ids is not None:
        for marker_corners in corners:
            #extract coordinate pairs for top right, top left, bottom left, bottom right
            TR,TL,BL,BR=marker_corners.reshape((4,2)).astype(int)

            #calculate center (x,y) coordinates
            x=(TR[0]+BL[0])/2
            y=(TR[1]+BL[1])/2
            
            pts = marker_corners.reshape((4, 2)).astype(int)
            cv2.polylines(frame, [pts], isClosed=True, color=(0, 255, 0), thickness=2)
            # draw a dot at (x,y) center
            cv2.circle(frame, (int(x), int(y)), 5, (0, 0, 255), -1)
    # Display the frame with detected markers
    cv2.imshow('Detected Markers', frame)
    cv2.waitKey(1)

    return [(x!=-1 and y!=-1), x,y]
    
    
    

