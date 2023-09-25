import tkinter as tk

root = tk.Tk()
root.minsize(360, 150)
root.maxsize(360, 150)
root.title("Attendance")

nameLabel = tk.Label(root, width = 50, height = 6, text = "Database is empty!!!")
nameLabel.grid(row = 1, column = 1)

root.mainloop()