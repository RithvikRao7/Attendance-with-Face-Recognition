import tkinter as tk
import os
import time

core_working_directory = os.path.dirname(os.path.realpath(__file__))
database_working_directory = os.path.dirname(core_working_directory) + "\\faceData"

root = tk.Tk()
root.minsize(500, 300)
root.maxsize(500, 300)
root.title("Attendance")

def login():
    RegisterButton["state"] = "disabled"
    LoginButton["state"] = "disabled"

    foundBool = False

    for person in os.listdir(database_working_directory + "\\images"):
        if person == nameEntryVar.get():
            foundBool = True

    #if not foundBool:
    #    os.system("start /min cmd /c python \"" + core_working_directory + "\\UnknownUserWarning.py\"")

    #    file = open(core_working_directory + "\\UnknownUserWarningUpdate.txt", "w")
    #    file.writelines(str(0))
    #    file.close()

    #    while True:
    #        file = open(core_working_directory + "\\UnknownUserWarningUpdate.txt", "r")
    #        try:
    #            value = int(file.readline())
    #        except Exception:
    #            continue
    #        file.close()
    #
    #        if value == 1:
    #            break
    #
    #    file = open(core_working_directory + "\\UnknownUserWarningUpdate.txt", "w")
    #    file.writelines(str(0))
    #    file.close()
    #    
    #    RegisterButton["state"] = "normal"
    #    LoginButton["state"] = "normal"
    #    return

    os.system("start /min cmd /c python \"" + core_working_directory + "\\FaceRecognition.py\" " + nameEntryVar.get() + " --cpus -1")
    os.system("start /min cmd /c python \"" + core_working_directory +  "\\Progress.py\"")

    file = open(core_working_directory + "\\previewUpdate.txt","w")
    file.writelines(str(0))
    file.close()

    file = open(core_working_directory + "\\progressUpdate.txt", "w")
    file.writelines([str(0), "\n", "Booting..."])
    file.close()

    while True:
        file = open(core_working_directory + "\\progressUpdate.txt", "r")
        try:
            value = int(file.readline())
            progress_info = file.readline()
        except Exception:
            continue
        file.close()

        if value == 100:
            time.sleep(0.3)

            file = open(core_working_directory + "\\progressUpdate.txt", "w")
            file.writelines([str(0), "\n", "Booting..."])
            file.close()

            file = open(core_working_directory + "\\previewUpdate.txt","w")
            file.writelines(str(1))
            file.close()

            break

    RegisterButton["state"] = "normal"
    LoginButton["state"] = "normal"

def register():
    if nameEntryVar.get() == "":
        return

    RegisterButton["state"] = "disabled"
    LoginButton["state"] = "disabled"
    
    for person in os.listdir(database_working_directory + "\\images"):
        if person == nameEntryVar.get():
            os.system("start /min cmd /c python \"" + core_working_directory + "\\SameUserWarning.py\"")

            file = open(core_working_directory + "\\sameUserWarningUpdate.txt", "w")
            file.writelines("null")
            file.close()
            
            while True:
                file = open(core_working_directory + "\\sameUserWarningUpdate.txt", "r")
                try:
                    value = file.readline()
                except Exception:
                    continue
                file.close()

                if value == "no":
                    RegisterButton["state"] = "normal"
                    LoginButton["state"] = "normal"
                    return
                elif value == "yes":
                    break
            
            file = open(core_working_directory + "\\sameUserWarningUpdate.txt", "w")
            file.writelines("null")
            file.close()

            break
    
    os.system("start /min cmd /c python \"" + core_working_directory + "\\RegisterFace.py\" " + nameEntryVar.get() + " --cpus -1")
    os.system("start /min cmd /c python \"" + core_working_directory +  "\\Progress.py\"")

    file = open(core_working_directory + "\\previewUpdate.txt","w")
    file.writelines(str(0))
    file.close()

    file = open(core_working_directory + "\\progressUpdate.txt", "w")
    file.writelines([str(0), "\n", "Booting..."])
    file.close()

    while True:
        file = open(core_working_directory + "\\progressUpdate.txt", "r")
        try:
            value = int(file.readline())
            progress_info = file.readline()
        except Exception:
            continue
        file.close()

        if value == 100:
            time.sleep(0.3)

            file = open(core_working_directory + "\\progressUpdate.txt", "w")
            file.writelines([str(0), "\n", "Booting..."])
            file.close()

            file = open(core_working_directory + "\\previewUpdate.txt","w")
            file.writelines(str(1))
            file.close()

            break
        
        time.sleep(0.1)

    NameEntry.delete(0,tk.END)
    NameEntry.insert(0,"")

    RegisterButton["state"] = "normal"
    LoginButton["state"] = "normal"

nameEntryVar = tk.StringVar()

canvas = tk.Canvas(root)

NameLabel = tk.Label(root, text = "Name:")
NameLabel.place(x = 150, y = 100)

NameEntry = tk.Entry(root, textvariable = nameEntryVar)
NameEntry.place(x = 200, y = 100)

LoginButton = tk.Button(root, text = "login", command = login)
LoginButton.place(x = 180, y = 130)

RegisterButton = tk.Button(root, text = "register", command = register)
RegisterButton.place(x = 240, y = 130)

root.mainloop()