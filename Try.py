#
#IZDELAVA DATOTEK ZA DELO
# 
import numpy as np 
import os
import pandas as pd
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
print(THIS_FOLDER)
#THIS_FOLDER=THIS_FOLDER+"\Obdelava\\"
def Datasets(date):
    for i in ["Datafile.csv", "XS.csv","S.csv","L.csv","XL.csv"]:
        if os.path.exists(THIS_FOLDER + "\Data\Created\\"+i):
            with open(THIS_FOLDER+"\Data\Created\\"+i,'r+') as file:
                file.truncate(0)
                print("I have done "+i) 
    if os.path.exists(THIS_FOLDER + "\Data\Created\Datafile.csv"):
        os.remove(THIS_FOLDER + "\Data\Created\Datafile.csv")
    def Delete_existing(filename):
        if os.path.exists(THIS_FOLDER + "\\"+str(filename)):
            fo = open(THIS_FOLDER + "\\"+str(filename), "wb")
            fo.close()
            os.remove(THIS_FOLDER + "\\"+str(filename))
    dir_list=os.listdir(THIS_FOLDER+"\Created_layers")
    for i in dir_list:
        #print(os.path.splitext(i)[0][:6])
        if  os.path.splitext(i)[0][:6]=="output":
            os.remove(THIS_FOLDER+"\Created_layers"+"\\"+i)
            #print("Done with:" +str(i))"""
            
    for i in ["Datafile.csv", "XS.csv","S.csv","L.csv","XL.csv","MrežaXL.csv"]:
        Delete_existing("\Data\\"+i)
        #print("Done deleting previus.")
    dir_list = os.listdir(THIS_FOLDER)

    with open(THIS_FOLDER + "\Data\Created\Datafile.csv","a") as file :
        file.write("\"N;Date;Time;N [Decimal degrees];E [Decimal degrees];GPS uncertainty [m];h [m];Location provider;D [ÎĽSv/h];Standard deviation;Standard error of the mean value;CF;Number of measured points\".\n")
    #print("Creating new datafile")
    def Editing(filename):
        with open(THIS_FOLDER + "\\Data\\"+ filename, 'r') as file :
            filedata = file.read()
    # Replace the target string
        filedata = filedata.replace('\".\"', ';')
    # Write the file out again
        with open(THIS_FOLDER + "\Data\Created\Datafile.csv","a") as file :
            file.writelines(filedata[191:])
    file.close()

    dir_list = os.listdir(THIS_FOLDER+"\Data")

    for i in dir_list:
        if i.endswith(".csv") and i!=THIS_FOLDER+"\Data\Datafile.csv":
            #print("Start with:"+str(i))
            a=Editing(str(i))
            #print("Done with:" +str(i))
      
    data = np.loadtxt(THIS_FOLDER + "\Data\Created\Datafile.csv",delimiter=";", dtype=str)

#data=pd.read_csv(THIS_FOLDER+ "\Start_iz_IJS_normal.csv", delimiter=";",dtype=str)
    df=pd.DataFrame(data[1:],columns =data[0])
    df.rename(columns = {"D [ÎĽSv/h]":r"D [μSv/h]"}, inplace = True)

    """idx=df.groupby(['N [Decimal degrees]','E [Decimal degrees]'])[r'D [μSv/h]'].transform(max) == df[r'D [μSv/h]']
    if os.path.exists(THIS_FOLDER + THIS_FOLDER+'\Podatki.csv'):
    os.remove(THIS_FOLDER+'\Podatki.csv')
    df[idx].to_csv(THIS_FOLDER+'\Podatki.csv',sep=';')"""
    #Small data
    inx=df.sort_values('D [μSv/h]').groupby(['N [Decimal degrees]','E [Decimal degrees]']).tail(1)
    print(inx)
    if os.path.exists(THIS_FOLDER +"\Data\Created\XS.csv"):
        os.remove(THIS_FOLDER+"\Data\Created\XS.csv")
    outfile = open(THIS_FOLDER+"\Data\Created\XS.csv", 'wb')
    inx.to_csv(THIS_FOLDER+"\Data\Created\XS.csv",sep=';')
    
    #Medium data
    df['N [Decimal degrees]']=df['N [Decimal degrees]'].astype(float).round(decimals = 2)
    df['E [Decimal degrees]']=df['E [Decimal degrees]'].astype(float).round(decimals = 2)
    inx=df.sort_values('D [μSv/h]').groupby(['N [Decimal degrees]','E [Decimal degrees]']).tail(1)
    
    if os.path.exists(THIS_FOLDER + "\Data\.csv"):
        os.remove(THIS_FOLDER+ "\Data\.csv")
    outfile = open(THIS_FOLDER+ "\Data\.csv", 'wb')
    inx.to_csv(THIS_FOLDER+ "\Data\.csv",sep=';')

    
    def round_off_rating(x, base=5):
        return base * round(x/base,3)
    df['N [Decimal degrees]']=round_off_rating(df['N [Decimal degrees]'])
    df['E [Decimal degrees]']=round_off_rating(df['E [Decimal degrees]'])
    inx=df.sort_values('D [μSv/h]').groupby(['N [Decimal degrees]','E [Decimal degrees]']).tail(1)

    if os.path.exists(THIS_FOLDER +"\Data\Created\S.csv"):
        os.remove(THIS_FOLDER+"\Data\Created\S.csv")
    outfile = open(THIS_FOLDER+"\Data\Created\S.csv", 'wb')
    inx.to_csv(THIS_FOLDER+"\Data\Created\S.csv",sep=';')

    #Big data
    df['N [Decimal degrees]']=df['N [Decimal degrees]'].astype(float).round(decimals = 1)
    df['E [Decimal degrees]']=df['E [Decimal degrees]'].astype(float).round(decimals = 1)
    inx=df.sort_values('D [μSv/h]').groupby(['N [Decimal degrees]','E [Decimal degrees]']).tail(1)
    if os.path.exists(THIS_FOLDER +"\Data\Created\XL.csv"):
        os.remove(THIS_FOLDER+"\Data\Created\XL.csv")
    outfile = open(THIS_FOLDER+"\Data\Created\XL.csv", 'wb')
    inx.to_csv(THIS_FOLDER+"\Data\Created\XL.csv",sep=';')

#
#IZDELAVA LAYERJEV
#
from osgeo import gdal
import os
import numpy as np
import matplotlib.cm as cm
import matplotlib.pyplot as plt
from mycolorpy import colorlist as mcp
cm = plt.cm.Reds

import os
import pandas as pd
#Function for removing not needed layers

    
from datetime import datetime
import time
now = datetime.now()
date = now.strftime("%d-%m-%Y_%H-%M-%S")
Datasets(date)

print("Normal layer")
from threading import Timer

"""QgsProject.instance().reloadAllLayers()
from qgis.PyQt.QtCore import QSettings
QSettings().setValue("/qgis/map_update_interval",150)
layer = QgsProject.instance().mapLayersByName("BuffedXL")[0]
print(layer)
layer.setAutoRefreshInterval(5000)
layer.setAutoRefreshEnabled(True)"""

run = True
i=0
def test():
    global i
    import time
    global run
    #rmvLyr("BuffedL")
    #rmvLyr("BuffedXL")
    #rmvLyr("BuffedXS")
    #rmvLyr("OpenStreetMap"
    #now =datetime.now()
    #date = now.strftime("%d-%m-%Y_%H-%M-%S")
    print("Deleting")
    #rmvLyr("L")
    #rmvLyr("XL")
    #rmvLyr("XS")
    print("Done Deleting")
    print("Creating dataset")
    Datasets(date)
    print("Done Creating dataset")
    print("Reseting")
    #Reseting(date)
    i+=1
    print("Done reseting")
    if i==20:
        return print("Done 5 times")
    if run:
        Timer(3, test).start()
test()