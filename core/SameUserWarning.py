import tkinter as tk
import os

core_working_directory = os.path.dirname(os.path.realpath(__file__))

def yes():
    file = open(core_working_directory + "\\sameUserWarningUpdate.txt", "w")
    file.writelines("yes")
    file.close()
    root.destroy()

def no():
    file = open(core_working_directory + "\\sameUserWarningUpdate.txt", "w")
    file.writelines("no")
    file.close()
    root.destroy()

root = tk.Tk()
root.minsize(500, 150)
root.maxsize(500, 150)
root.title("Attendance")

QuestionLabel = tk.Label(root, text = "User with same name exists.\nDo you want to add more photos to this username for improving face recognition?")
QuestionLabel.place(x = 30, y = 30)

YesButton = tk.Button(root, text = "yes", command = yes)
YesButton.place(x = 210, y = 80)

NoButton = tk.Button(root, text = "no", command = no)
NoButton.place(x = 260, y = 80)

root.mainloop()