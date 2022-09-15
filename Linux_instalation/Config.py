import os
print("Welcome to instalation of Map of radioactivity. \n")
INPUT=input("Do you have all the python files installed in this folder (This folder+/python): (y/n)")
print(INPUT)
if INPUT=="y":
    THIS_FOLDER = os.path.dirname(os.path.abspath("__file__"))
    for i in ["Dots.bat", "Squares.bat", "Interactive.bat", "Grid.bat"]:
        if os.path.exists(THIS_FOLDER+"/"+i):
            print("The file "+i+" does exist")
            os.remove(THIS_FOLDER+"/"+i)
        else:
             print("The file "+i+" does not exist")
        with open(THIS_FOLDER+"/"+i,"a",encoding='utf-8') as file:
            if i=="Dots.bat":
                file.write("qgis --nologo --project "+THIS_FOLDER+"/Map_of_radioactivity-Slovenia.qgz --code "+ THIS_FOLDER+"/Full_version-dots.py")
            if i=="Squares.bat":
                file.write("qgis --nologo --project "+THIS_FOLDER+"/Map_of_radioactivity-Slovenia.qgz --code "+ THIS_FOLDER+"/Full_version-squares.py")
            if i=="Grid.bat":
               file.write("qgis --nologo --project "+THIS_FOLDER+"/Map_of_radioactivity-Slovenia.qgz --code "+ THIS_FOLDER+"/Full_version-grid.py")
            if i=="Interactive.bat":
               file.write("qgis --nologo --project "+THIS_FOLDER+"/Map_of_radioactivity-Slovenia.qgz --code "+ THIS_FOLDER+"/Interactive_version.py")
if INPUT=="n":
    THIS_FOLDER=input("Enter the folder, were the python files are installed:")
    for i in ["Dots.bat", "Squares.bat", "Interactive.bat", "Grid.bat"]:
        if os.path.exists(THIS_FOLDER+"/"+i):
            os.remove(THIS_FOLDER+"/"+i)
            print("The file "+i+" does exist")
        else:
             print("The file "+i+" does not exist")
        with open(THIS_FOLDER+"/"+i,"a",encoding='utf-8') as file:
            if i=="Dots.bat":
                file.write("qgis --nologo --project "+THIS_FOLDER+"/Map_of_radioactivity-Slovenia.qgz --code "+ THIS_FOLDER+"/Full_version-dots.py")
            if i=="Squares.bat":
                file.write("qgis --nologo --project "+THIS_FOLDER+"/Map_of_radioactivity-Slovenia.qgz --code "+ THIS_FOLDER+"/Full_version-squares.py")
            if i=="Grid.bat":
               file.write("qgis --nologo --project "+THIS_FOLDER+"/Map_of_radioactivity-Slovenia.qgz --code "+ THIS_FOLDER+"/Full_version-grid.py")
            if i=="Interactive.bat":
               file.write("qgis --nologo --project "+THIS_FOLDER+"/Map_of_radioactivity-Slovenia.qgz --code "+ THIS_FOLDER+"/Interactive_version.py")
