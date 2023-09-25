import os

main_working_directory = os.path.dirname(os.path.realpath(__file__))
core_working_directory = os.path.dirname(main_working_directory) + "\\core"

decision = input("Do you want to Reset Update Files (y/n): ")
while True:
    if decision == "n":
        exit(0)
    elif decision == "y":
        break
    decision = input("Enter only valid options (y/n): ")

file = open(core_working_directory + "\\previewUpdate.txt","w")
file.writelines(str(1))
file.close()

file = open(core_working_directory + "\\progressUpdate.txt","w")
file.writelines([str(0), "\n", "Booting..."])
file.close()

file = open(core_working_directory + "\\sameUserWarningUpdate.txt", "w")
file.writelines("null")
file.close()

file = open(core_working_directory + "\\unknownUserWarningUpdate.txt", "w")
file.writelines(str(0))
file.close()

file = open(core_working_directory + "\\encodingFailedUpdate.txt", "w")
file.writelines(str(0))
file.close()

print("Update Files have been reset")