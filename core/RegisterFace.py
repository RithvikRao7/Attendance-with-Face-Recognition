import face_recognition as fr
import cv2
import os
import shutil
import sys
import copy
import pickle

core_working_directory = os.path.dirname(os.path.realpath(__file__))
database_working_directory = os.path.dirname(core_working_directory) + "\\faceData"

name = sys.argv[1]
imgCount = 0
encoding_file = 0
encodings = []
createBool = False

file = open(core_working_directory + "\\progressUpdate.txt", "w")
file.writelines([str(20), "\n", "Checking Database..."])
file.close()

if os.path.exists(os.path.join(database_working_directory, "images", name)):
    for x in os.listdir(os.path.join(database_working_directory, "images", name)):
        file = x[:-4]
        if file[-2].isalpha():
            if imgCount < int(file[-1]):
                imgCount = int(file[-1]) + 1
        elif imgCount < int(file[-2:]):
            imgCount = int(file[-2:]) + 1
    encoding_file = open(os.path.join(database_working_directory, "encodings", name + "_encoding.txt"),"rb")
    encodings = pickle.load(encoding_file)
    encoding_file.close()
    encoding_file = open(os.path.join(database_working_directory, "encodings", name + "_encoding.txt"),"wb")
else:
    os.mkdir(os.path.join(database_working_directory, "images", name))
    encoding_file = open(os.path.join(database_working_directory, "encodings", name + "_encoding.txt"),'wb')
    createBool = True

file = open(core_working_directory + "\\progressUpdate.txt", "w")
file.writelines([str(40), "\n", "Setting up camera..."])
file.close()

firstImgCount = imgCount

try:
    faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    video_capture = cv2.VideoCapture(0)
    
    camera_width = video_capture.get(cv2.CAP_PROP_FRAME_WIDTH)
    camera_height = video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT)

    file = open(core_working_directory + "\\progressUpdate.txt", "w")
    file.writelines([str(60), "\n", "Capturing Images..."])
    file.close()

    tempCount = 0
    
    while tempCount < 15:
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

        tempFrame = copy.deepcopy(frame)

        try:
            if len(faces) > 1:
                file = open(core_working_directory + "\\progressUpdate.txt", "w")
                file.writelines([str(60 + tempCount), "\n", "Capturing Images(" + str(tempCount) + "/15). Multiple Faces Detected, please move out of the frame"])
                file.close()
                continue
            elif len(faces) != 1:
                file = open(core_working_directory + "\\progressUpdate.txt", "w")
                file.writelines([str(60 + tempCount), "\n", "Capturing Images(" + str(tempCount) + "/15). No Faces Detected, try moving your head a bit"])
                file.close()
                continue
        except:
            continue

        # Draw a rectangle around the faces
        for (x, y, w, h) in faces:
            cv2.rectangle(tempFrame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        cv2.imwrite(os.path.join(database_working_directory, "images", name, "img" + str(imgCount) + ".jpg"), frame.copy())
        imgCount += 1
        tempCount += 1

        key = cv2.waitKey(1) & 0xFF

        file = open(core_working_directory + "\\progressUpdate.txt", "w")
        file.writelines([str(60 + tempCount), "\n", "Capturing Images(" + str(tempCount) + "/15)"])
        file.close()
finally:
    video_capture.release()
    cv2.destroyAllWindows()

file = open(core_working_directory + "\\progressUpdate.txt", "w")
file.writelines([str(75), "\n", "Encoding Face Values..."])
file.close()

temp_encodings = []

tempCount = 1
FailCount = 0
for image in os.listdir(os.path.join(database_working_directory, "images", name))[firstImgCount:imgCount]:
    load_image = fr.load_image_file(os.path.join(database_working_directory, "images", name, image))
    try:
        temp_encodings.append(fr.face_encodings(load_image)[0])
    except:
        file = open(core_working_directory + "\\progressUpdate.txt", "w")
        file.writelines([str(75 + tempCount), "\n", "Encoding Face Values(" + str(tempCount) + "/15) Failed!!!"])
        file.close()
        tempCount += 1
        FailCount += 1

        if FailCount >= 4:
            file = open(core_working_directory + "\\encodingFailedUpdate.txt", "w")
            file.writelines(str(0))
            file.close()

            os.system("start /min cmd /c python \"" + core_working_directory +  "\\EncodingFailed.py\"")

            while True:
                file = open(core_working_directory + "\\encodingFailedUpdate.txt", "r")
                try:
                    value = int(file.readline())
                except Exception:
                    continue
                file.close()

                if value == 1:
                    break

                file = open(core_working_directory + "\\encodingFailedUpdate.txt", "w")
                file.writelines(str(0))
                file.close()

                if createBool:
                    file = open(core_working_directory + "\\progressUpdate.txt", "w")
                    file.writelines([str(95), "\n", "Deleting Images Taken"])
                    file.close()

                    shutil.rmtree(database_working_directory + "\\images\\" + name)
                    encoding_file.close()
                    os.unlink(database_working_directory + "\\encodings\\" + name + "_encoding.txt")
    
                    file = open(core_working_directory + "\\progressUpdate.txt", "w")
                    file.writelines([str(100), "\n", "Registraion Failed"])
                    file.close()

                    exit(0)

        continue

    file = open(core_working_directory + "\\progressUpdate.txt", "w")
    file.writelines([str(75 + tempCount), "\n", "Encoding Face Values(" + str(tempCount) + "/15)"])
    file.close()
    tempCount += 1

file = open(core_working_directory + "\\progressUpdate.txt", "w")
file.writelines([str(90), "\n", "Saving Face Encodes..."])
file.close()

encodings.append(temp_encodings)

pickle.dump(encodings, encoding_file)

encoding_file.close()

file = open(core_working_directory + "\\progressUpdate.txt", "w")
file.writelines([str(100), "\n", "Finished"])
file.close()