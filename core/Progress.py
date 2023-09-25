import tkinter as tk
import tkinter.ttk as ttk
import os

core_working_directory = os.path.dirname(os.path.realpath(__file__))

root = tk.Tk()
root.title("Attendance")

condition = True

dummy = tk.Label(root)
dummy.grid(row = 0,column = 0)

progress = ttk.Progressbar(root, orient = tk.HORIZONTAL, length = 100, mode = "determinate")
progress.grid(row = 0, column = 1)

text = tk.Label(root)
text.grid(row = 1, column = 1)

def update_progress():
    global condition

    if condition:
        file = open(core_working_directory + "\\progressUpdate.txt", "r")
        try:
            value = int(file.readline())
            progress_info = file.readline()
        except:
            root.after(100, update_progress)
        progress["value"] = value
        text["text"] = progress_info

        root.update_idletasks()
        file.close()

        if value == 100:
            root.destroy()
            condition = False

        root.after(100, update_progress)

root.after(100, update_progress)

root.mainloop()