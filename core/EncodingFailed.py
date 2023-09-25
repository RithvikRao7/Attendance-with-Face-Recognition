import tkinter as tk
import os

core_working_directory = os.path.dirname(os.path.realpath(__file__))

def ok():
    file = open(core_working_directory + "\\encodingFailedUpdate.txt", "w")
    file.writelines(str(1))
    file.close()
    root.destroy()

root = tk.Tk()
root.minsize(400, 150)
root.maxsize(400, 150)
root.title("Attendance")

ErrorLabel = tk.Label(root, text = "Too many Failures during encoding, due to lighting issues.\nMake sure the light source is on your face, not behind your face.")
ErrorLabel.place(x = 30, y = 40)

OkButton = tk.Button(root, text = "ok", command = ok)
OkButton.place(x = 180, y = 80)

root.mainloop()