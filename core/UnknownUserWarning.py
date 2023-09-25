import tkinter as tk
import os

core_working_directory = os.path.dirname(os.path.realpath(__file__))

def ok():
    file = open(core_working_directory + "\\unknownUserWarningUpdate.txt", "w")
    file.writelines(str(1))
    file.close()
    root.destroy()

root = tk.Tk()
root.minsize(300, 150)
root.maxsize(300, 150)
root.title("Attendance")

ErrorLabel = tk.Label(root, text = "User with this name dosen't exist.")
ErrorLabel.place(x = 70, y = 40)

OkButton = tk.Button(root, text = "ok", command = ok)
OkButton.place(x = 140, y = 80)

root.mainloop()