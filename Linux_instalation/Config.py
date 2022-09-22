import os

def input_function():
    INPUT=input("Do you have all the python files installed in this folder (This folder+\python): (y/n)")
    if INPUT=="y" or INPUT=="Y":
        THIS_FOLDER = os.path.dirname(os.path.abspath("__file__"))
        for i in ["Dots.bat", "Squares.bat", "Interactive.bat", "Grid.bat"]:
            if os.path.exists(THIS_FOLDER+"/"+i):
                print("The file "+i+" does exist")
                os.remove(THIS_FOLDER+"/"+i)
            else:
                print("The file "+i+" does not exist")
            with open(THIS_FOLDER+"/"+i,"a",encoding='utf-8') as file:
                if i=="Dots.bat":
                    file.write("qgis --nologo --project "+THIS_FOLDER+"/Map_of_radioactivity-Slovenia.qgz --code "+ THIS_FOLDER+"/Programs/Full_version-dots.PY")
                if i=="Squares.bat":
                    file.write("qgis --nologo --project "+THIS_FOLDER+"/Map_of_radioactivity-Slovenia.qgz --code "+ THIS_FOLDER+"/Programs/Full_version-squares.PY")
                if i=="Grid.bat":
                    file.write("qgis --nologo --project "+THIS_FOLDER+"/Map_of_radioactivity-Slovenia.qgz --code "+ THIS_FOLDER+"/Programs/Full_version-grid.PY")
                if i=="Interactive.bat":
                    file.write("qgis --nologo --project "+THIS_FOLDER+"/Map_of_radioactivity-Slovenia.qgz --code "+ THIS_FOLDER+"/Programs/Interactive_version.PY")
    elif INPUT=="n" or INPUT=="N":
        THIS_FOLDER=input("Enter the folder, were the python files are installed:")
        if THIS_FOLDER=="":
            THIS_FOLDER=os.path.dirname(os.path.abspath("__file__"))
        for i in ["Dots.bat", "Squares.bat", "Interactive.bat", "Grid.bat"]:
            if os.path.exists(THIS_FOLDER+"/"+i):
                os.remove(THIS_FOLDER+"/"+i)
                print("The file "+i+" does exist")
            else:
                print("The file "+i+" does not exist")
            with open(THIS_FOLDER+"/"+i,"a",encoding='utf-8') as file:
                if i=="Dots.bat":
                    file.write("qgis --nologo --project "+THIS_FOLDER+"/Map_of_radioactivity-Slovenia.qgz --code "+ THIS_FOLDER+"/Programs/Full_version-dots.PY")
                if i=="Squares.bat":
                    file.write("qgis --nologo --project "+THIS_FOLDER+"/Map_of_radioactivity-Slovenia.qgz --code "+ THIS_FOLDER+"/Programs/Full_version-squares.PY")
                if i=="Grid.bat":
                    file.write("qgis --nologo --project "+THIS_FOLDER+"/Map_of_radioactivity-Slovenia.qgz --code "+ THIS_FOLDER+"/Programs/Full_version-grid.PY")
                if i=="Interactive.bat":
                    file.write("qgis --nologo --project "+THIS_FOLDER+"/Map_of_radioactivity-Slovenia.qgz --code "+ THIS_FOLDER+"/Programs/Interactive_version.PY")
    elif INPUT!="n" or INPUT!="y" or INPUT!="Y" or INPUT!="N":
        print("Invalid input, try again")
        input_function()

print("Welcome to instalation of Map of radioactivity. \n")
INPUT=input("Do you have all the python files installed in this folder (This folder+/python): (y/n)")
print(INPUT)
if INPUT=="y" or INPUT=="Y":
    THIS_FOLDER = os.path.dirname(os.path.abspath("__file__"))
    for i in ["Dots.bat", "Squares.bat", "Interactive.bat", "Grid.bat", "Live.bat"]:
        if os.path.exists(THIS_FOLDER+"/"+i):
            print("The file "+i+" does exist")
            os.remove(THIS_FOLDER+"/"+i)
        else:
             print("The file "+i+" does not exist")
        with open(THIS_FOLDER+"/"+i,"a",encoding='utf-8') as file:
            if i=="Dots.bat":
                file.write("qgis --nologo --project "+THIS_FOLDER+"/Map_of_radioactivity-Slovenia.qgz --code "+ THIS_FOLDER+"/Programs/Full_version-dots.py")
            if i=="Squares.bat":
                file.write("qgis --nologo --project "+THIS_FOLDER+"/Map_of_radioactivity-Slovenia.qgz --code "+ THIS_FOLDER+"/Programs/Full_version-squares.py")
            if i=="Grid.bat":
               file.write("qgis --nologo --project "+THIS_FOLDER+"/Map_of_radioactivity-Slovenia.qgz --code "+ THIS_FOLDER+"/Programs/Full_version-grid.py")
            if i=="Interactive.bat":
               file.write("qgis --nologo --project "+THIS_FOLDER+"/Map_of_radioactivity-Slovenia.qgz --code "+ THIS_FOLDER+"/Programs/Interactive_version.py")
            if i=="Live.bat":
               file.write("qgis --nologo --project "+THIS_FOLDER+"/Map_of_radioactivity-Slovenia.qgz --code "+ THIS_FOLDER+"/Programs/Live_update.py")
if INPUT=="n" or INPUT=="N":
    THIS_FOLDER=input("Enter the folder, were the python files are installed:")
    for i in ["Dots.bat", "Squares.bat", "Interactive.bat", "Grid.bat"]:
        if os.path.exists(THIS_FOLDER+"/"+i):
            os.remove(THIS_FOLDER+"/"+i)
            print("The file "+i+" does exist")
        else:
             print("The file "+i+" does not exist")
        with open(THIS_FOLDER+"/"+i,"a",encoding='utf-8') as file:
            if i=="Dots.bat":
                file.write("qgis --nologo --project "+THIS_FOLDER+"/Map_of_radioactivity-Slovenia.qgz --code "+ THIS_FOLDER+"/Programs/Full_version-dots.py")
            if i=="Squares.bat":
                file.write("qgis --nologo --project "+THIS_FOLDER+"/Map_of_radioactivity-Slovenia.qgz --code "+ THIS_FOLDER+"/Programs/Full_version-squares.py")
            if i=="Grid.bat":
               file.write("qgis --nologo --project "+THIS_FOLDER+"/Map_of_radioactivity-Slovenia.qgz --code "+ THIS_FOLDER+"/Programs/Full_version-grid.py")
            if i=="Interactive.bat":
               file.write("qgis --nologo --project "+THIS_FOLDER+"/Map_of_radioactivity-Slovenia.qgz --code "+ THIS_FOLDER+"/Programs/Interactive_version.py")
            if i=="Live.bat":
               file.write("qgis --nologo --project "+THIS_FOLDER+"/Map_of_radioactivity-Slovenia.qgz --code "+ THIS_FOLDER+"/Programs/Live_update.py")

elif INPUT!="n" or INPUT!="y" or INPUT!="Y" or INPUT!="N":
    print("Invalid input, try again")
    input_function()