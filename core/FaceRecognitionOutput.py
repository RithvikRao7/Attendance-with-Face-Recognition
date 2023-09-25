import tkinter as tk
import sys

name = sys.argv[1]

root = tk.Tk()
root.minsize(350, 150)
root.maxsize(350, 150)
root.title("Attendance")

nameLabel = tk.Label(root, width = 50, height = 6)
nameLabel.grid(row = 1, column = 1)
nameLabel["text"] = "Hi " + name[0].upper() + name[1:] + ", your attendance is marked."

root.mainloop()