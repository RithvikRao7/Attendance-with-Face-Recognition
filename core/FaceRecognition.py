import os
import pickle
import shutil
import cv2
import face_recognition as fr

core_working_directory = os.path.dirname(os.path.realpath(__file__))
database_working_directory = os.path.dirname(core_working_directory) + "\\faceData"
presentee_working_directory = os.path.dirname(core_working_directory) + "\\temp"

if len(os.listdir(database_working_directory + "\\images")) == 0:
    os.system("start /min cmd /c python \"" + core_working_directory +  "\\DatabaseEmpty.py\"")

    file = open(core_working_directory + "\\progressUpdate.txt", "w")
    file.writelines([str(100), "\n", "Database is empty!!!"])
    file.close()

    exit(0)

file = open(core_working_directory + "\\progressUpdate.txt", "w")
file.writelines([str(10), "\n", "Clearing temp folder..."])
file.close()

for file_name in os.listdir(presentee_working_directory):
    file_path = os.path.join(presentee_working_directory,file_name)
    try:
        if os.path.isfile(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    except Exception as e:
        print(e)

file = open(core_working_directory + "\\progressUpdate.txt", "w")
file.writelines([str(20), "\n", "Setting up camera..."])
file.close()

try:
    faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    video_capture = cv2.VideoCapture(0)

    imgCount = 0

    file = open(core_working_directory + "\\progressUpdate.txt", "w")
    file.writelines([str(40), "\n", "Capturing Images..."])
    file.close()

    while imgCount < 7:
        ret, frame = video_capture.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor = 1.1,
            minNeighbors = 5,
            minSize = (30, 30),
            flags = cv2.CASCADE_SCALE_IMAGE
        )

        try:
            if len(faces) != 1:
                continue
        except:
            continue

        cv2.imwrite(os.path.join(presentee_working_directory, "img" + str(imgCount) + ".jpg"), frame.copy())

        key = cv2.waitKey(1) & 0xFF

        imgCount += 1

        file = open(core_working_directory + "\\progressUpdate.txt", "w")
        file.writelines([str(40 + imgCount), "\n", "Capturing Images(" + str(imgCount) + "/7)"])
        file.close()
finally:
    video_capture.release()
    cv2.destroyAllWindows()

file = open(core_working_directory + "\\progressUpdate.txt", "w")
file.writelines([str(50), "\n", "Importing Database..."])
file.close()

result_ratio = {}
personCount = 1
for person in os.listdir(os.path.join(database_working_directory, "encodings")):
    file = open(core_working_directory + "\\progressUpdate.txt", "w")
    file.writelines([str(60), "\n", "Checking Face Encodes(" + str(personCount) + "/" + str(len(os.listdir(os.path.join(database_working_directory, "encodings")))) + ")"])
    file.close()

    file = open(os.path.join(database_working_directory, "encodings", person),"rb")
    person_encodings = pickle.load(file)
    file.close()

    TrueCount = 0
    FalseCount = 0
    ResultCount = 1
    for image in os.listdir(presentee_working_directory):
        presentee_img = fr.load_image_file(os.path.join(presentee_working_directory, image))

        try:
            presentee_img_encoding = fr.face_encodings(presentee_img)[0]
            if len(presentee_img_encoding) == 0:
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

                break
        except Exception:
            continue

        result = fr.compare_faces(person_encodings, presentee_img_encoding, tolerance = 0.4)
        for arr in result:
            for recognise in arr:
                if recognise:
                    TrueCount += 1
                else:
                    FalseCount += 1
            ResultCount += len(arr)
    result_ratio[person[:-13]] = (TrueCount - FalseCount)/ResultCount

    personCount += 1

file = open(core_working_directory + "\\progressUpdate.txt", "w")
file.writelines([str(80), "\n", "Displaying Output"])
file.close()

presentee = max(result_ratio, key = lambda x: result_ratio[x])

if result_ratio[presentee] >= 0.9:
    os.system("start /min cmd /c python \"" + core_working_directory + "\\FaceRecognitionOutput.py\" " + presentee)
else:
    os.system("start /min cmd /c python \"" + core_working_directory + "\\CouldNotRecognise.py\"")

file = open(core_working_directory + "\\progressUpdate.txt", "w")
file.writelines([str(90), "\n", "Clearing temp folder"])
file.close()

for file_name in os.listdir(presentee_working_directory):
    file_path = os.path.join(presentee_working_directory,file_name)
    try:
        if os.path.isfile(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    except Exception as e:
        print(e)

file = open(core_working_directory + "\\progressUpdate.txt", "w")
file.writelines([str(100), "\n", "Finished"])
file.close()