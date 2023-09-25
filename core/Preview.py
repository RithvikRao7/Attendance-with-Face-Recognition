import cv2
import os
import time

core_working_directory = os.path.dirname(os.path.realpath(__file__))

prev_value = 1

try:
    faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    video_capture = cv2.VideoCapture(0)
    
    while True:
        file = open(core_working_directory + "\\previewUpdate.txt","r")
        try:
            value = int(file.readline())
        except Exception:
            continue
        file.close()
        if value == 0 and value == prev_value:
            time.sleep(0.3)
            prev_value = value
            continue
        elif value == 0 and value != prev_value:
            video_capture.release()
            cv2.destroyAllWindows()
            prev_value = value
            continue
        elif value == 1 and value != prev_value:
            video_capture = cv2.VideoCapture(0)
        
        prev_value = value

        # Capture frame-by-frame
        ret, frame = video_capture.read()

        frame = cv2.resize(frame, (960, 1080))

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor = 1.1,
            minNeighbors = 5,
            minSize = (30, 30),
            flags = cv2.CASCADE_SCALE_IMAGE
        )

        # Draw a rectangle around the faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        cv2.imshow('Video', frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('l'):
            os.system("start /min cmd /c python \"" + core_working_directory + "\\UI.py\" --cpus -1")
        elif key == ord('e'):
            break
        
finally:
    video_capture.release()
    cv2.destroyAllWindows()