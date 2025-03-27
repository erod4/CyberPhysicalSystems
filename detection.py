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

    #detect the markers
    corners, ids, rejected =detector.detectMarkers(gray)
    if ids is not None:
        for marker_corners in corners:
            pts = marker_corners.reshape((4, 2)).astype(int)
            cv2.polylines(frame, [pts], isClosed=True, color=(0, 255, 0), thickness=2)

    # Display the frame with detected markers
    cv2.imshow('Detected Markers', frame)
    
    # Press 'q' to exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        return False
    return True

