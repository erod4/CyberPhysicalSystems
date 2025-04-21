# detection.py

import cv2
import numpy as np
from picamera2 import Picamera2
from libcamera import Transform
import os 
CAMERA_WIDTH    =   640
CAMERA_HEIGHT   =   480
HORIZONTAL_FOV  =   60
VERTICAL_FOV    =   40
# --- PiCamera2 setup ---
picam2 = None

def VIDEO_INIT():
    global picam2
    picam2 = Picamera2()
    config = picam2.create_preview_configuration(
        main={"size": (CAMERA_WIDTH, CAMERA_HEIGHT)},
        controls={"FrameDurationLimits": (10000, 10000)}  # 10000 μs = 100 FPS max

    )
    config["transform"] = Transform(vflip=True, hflip=True)
    picam2.configure(config)
    picam2.start()

def VIDEO_DEINIT():
    cv2.destroyAllWindows()
    # picam2.stop()  # if you ever want to fully shut the camera

# --- OpenCV AprilTag detector setup ---
# Make sure your cv2.__version__ >= "4.7.0"
aruco_dict  = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_APRILTAG_36h11)
aruco_params = cv2.aruco.DetectorParameters()
at_detector = cv2.aruco.ArucoDetector(aruco_dict, aruco_params)

def PROCESS_FRAME():
    """
    Captures one frame, detects AprilTags, draws debug info, and returns:
        (detected: bool, x: int, y: int)
    """
    # 1) Grab frame & convert to BGR + gray
    frame = picam2.capture_array()
    frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    gray      = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2GRAY)

    # 2) Detect AprilTags
    corners, ids, _ = at_detector.detectMarkers(gray)

    if ids is not None and len(ids) > 0:
        # Just use the first detected tag (or pick by id)
        c = corners[0].reshape((4, 2))
        x = int(c[:, 0].mean())
        y = int(c[:, 1].mean())
        detected = True

        # Draw the quad and center
        for i in range(4):
            p1 = tuple(c[i].astype(int))
            p2 = tuple(c[(i + 1) % 4].astype(int))
            cv2.line(frame_bgr, p1, p2, (0, 255, 0), 2)
        cv2.circle(frame_bgr, (x, y), 4, (0, 0, 255), -1)
    else:
        x, y, detected = 0, 0, False

    if os.environ.get("DISPLAY") is not None:
        cv2.imshow("AprilTag Detection", frame_bgr)
        cv2.waitKey(1)

    # 4) Return flag + coordinates
    return [detected, x, y]
