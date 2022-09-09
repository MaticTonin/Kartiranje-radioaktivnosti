from PyQt5.QtGui import *
import numpy as np
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import pandas as pd
import sys
import numpy as np
import os
import matplotlib.cm as cm
import matplotlib.pyplot as plt
from mycolorpy import colorlist as mcp

#DODAJ VSEM
from PyQt5.QtWidgets import QInputDialog, QLineEdit, QDialog, QApplication, QDialogButtonBox, QFormLayout
from processing.core.Processing import processing
from PyQt5.QtGui import QColor, QFont,QPainter
from qgis.utils import iface

cm = plt.cm.Reds
def rmvLyr(lyrname):
    qinst = QgsProject.instance()
    qinst.removeMapLayer(qinst.mapLayersByName(lyrname)[0].id())
#
#INPUT ABOUT DATAFILES
#
class InputDialog_DATA(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Map of Radioactivity in Slovenia")
        self.first = QLineEdit(self)
        self.second = QLineEdit(self)
        self.third = QLineEdit(self)
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self);

        layout = QFormLayout(self)
        layout.addRow("Datafile (full path)", self.first)
        layout.addRow("File for created layers (full path)", self.second)
        layout.addRow("File for created PDF,png,SVG (full path)", self.third)
        layout.addWidget(buttonBox)

        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

    def getInputs(self):
        return (self.first.text(), self.second.text(), self.third.text())


THIS_FOLDER = os.path.dirname(os.path.abspath("__file__"))
folders = InputDialog_DATA()
if folders.exec():
    FILES=np.array(folders.getInputs())
    if FILES[0]=='':
        data_folder=THIS_FOLDER+"\\Data\\"
    else:
        data_folder=FILES[0]+"\\"
    if FILES[1]=='':
        layers_save = THIS_FOLDER+"\\Created_Layers\\" 
        if not os.path.exists(layers_save):
            os.makedirs(layers_save)
        print(THIS_FOLDER+"\\Created_Layers\\")
        created_layers=THIS_FOLDER+"\\Created_layers\\"
    else:
        created_layers=FILES[1]+"\\"
    if FILES[2]=='':
        saving_folder=THIS_FOLDER+"\\"
    else:
        saving_folder=FILES[2]+"\\"
print("Selected paths: Datafile:"+ data_folder+ "\nCreated layers:" +created_layers+ "\nFile for created PDF,png,SVG:"+saving_folder)
#
#Setting dataset
#
def dataSets(date,data,layers):
#
    if os.path.exists(data+"\Created\Datafile "+str(date)+".csv"):
        os.remove(data+"\Created\Datafile "+str(date)+".csv")
    def Delete_existing(filename):
        if os.path.exists(data+str(filename)):
            fo = open(data+str(filename), "wb")
            fo.close()
            os.remove(data+str(filename))
    dir_list=os.listdir(layers)
    for i in dir_list:
        #print(os.path.splitext(i)[0][:6])
        if  os.path.splitext(i)[0][:6]=="output":
            os.remove(layers+i)
            #print("Done with:" +str(i))"""
    created = data+"Created\\" 
    if not os.path.exists(created):
        os.makedirs(created)        
    for i in ["Datafile.csv", "XS.csv","S.csv","L.csv","XL.csv","MrežaXL.csv"]:
        Delete_existing(i)
        #print("Done deleting previus.")
    dir_list = os.listdir(data)

    with open(created+"Datafile "+date+".csv","a") as file :
        file.write("\"N;Date;Time;N [Decimal degrees];E [Decimal degrees];GPS uncertainty [m];h [m];Location provider;D [ÎĽSv/h];Standard deviation;Standard error of the mean value;CF;Number of measured points\".\n")
    #print("Creating new datafile")
    def Editing(filename):
        with open(data+ filename, 'r') as file :
            filedata = file.read()
    # Replace the target string
        filedata = filedata.replace('\".\"', ';')
    # Write the file out again
        with open(created+"Datafile "+date+".csv","a") as file :
            file.writelines(filedata[191:])
    file.close()

    dir_list = os.listdir(data)
    for i in dir_list:
        if i.endswith(".csv") and i[0:8]!="Datafile" and i[0:3]!="XL " and i[0:3]!="XS " and i[0:2]!="L " and i[0:2]!="S ":
            #print("Start with:"+str(i))
            a=Editing(str(i))
            #print("Done with:" +str(i))
      
    info = np.loadtxt(created+"Datafile "+date+".csv",delimiter=";", dtype=str)
#data=pd.read_csv(THIS_FOLDER+ "\Start_iz_IJS_normal.csv", delimiter=";",dtype=str)
    df=pd.DataFrame(info[1:],columns =info[0])
    df.rename(columns = {"D [ÎĽSv/h]":r"D [μSv/h]"}, inplace = True)

    """idx=df.groupby(['N [Decimal degrees]','E [Decimal degrees]'])[r'D [μSv/h]'].transform(max) == df[r'D [μSv/h]']
    if os.path.exists(THIS_FOLDER + THIS_FOLDER+'\Podatki.csv'):
    os.remove(THIS_FOLDER+'\Podatki.csv')
    df[idx].to_csv(THIS_FOLDER+'\Podatki.csv',sep=';')"""
    #Small data
    inx=df.sort_values('D [μSv/h]').groupby(['N [Decimal degrees]','E [Decimal degrees]']).tail(1)
    if os.path.exists(created+"XS "+date+".csv"):
        os.remove(created+"XS "+date+".csv")
    outfile = open(created+"XS "+date+".csv", 'wb')
    inx.to_csv(created+"XS "+date+".csv",sep=';')
    outfile.close()
    
    #Medium data
    df['N [Decimal degrees]']=df['N [Decimal degrees]'].astype(float).round(decimals = 2)
    df['E [Decimal degrees]']=df['E [Decimal degrees]'].astype(float).round(decimals = 2)
    inx=df.sort_values('D [μSv/h]').groupby(['N [Decimal degrees]','E [Decimal degrees]']).tail(1)
    
    if os.path.exists(created+"\L "+date+".csv"):
        os.remove(created+"\L "+date+".csv")
    outfile = open(created+"\L "+date+".csv", 'wb')
    inx.to_csv(created+"\L "+date+".csv",sep=';')
    outfile.close()
    
    def round_off_rating(x, base=5):
        return base * round(x/base,3)
    df['N [Decimal degrees]']=round_off_rating(df['N [Decimal degrees]'])
    df['E [Decimal degrees]']=round_off_rating(df['E [Decimal degrees]'])
    inx=df.sort_values('D [μSv/h]').groupby(['N [Decimal degrees]','E [Decimal degrees]']).tail(1)

    if os.path.exists(created+"\S "+date+".csv"):
        os.remove(created+"\S "+date+".csv")
    outfile = open(created+"\S "+date+".csv", 'wb')
    inx.to_csv(created+"\S "+date+".csv",sep=';')
    outfile.close()
    #Big data
    df['N [Decimal degrees]']=df['N [Decimal degrees]'].astype(float).round(decimals = 1)
    df['E [Decimal degrees]']=df['E [Decimal degrees]'].astype(float).round(decimals = 1)
    inx=df.sort_values('D [μSv/h]').groupby(['N [Decimal degrees]','E [Decimal degrees]']).tail(1)
    if os.path.exists(created+"\XL "+date+".csv"):
        os.remove(created+"\XL "+date+".csv")
    outfile = open(created+"\XL "+date+".csv", 'wb')
    inx.to_csv(created+"\XL "+date+".csv",sep=';')
    outfile.close()
    return created
    
def Zones_window():
    qid = QDialog()
    items = ("None", "Just zones", "Zones with 100m population", "Zones with 500m population")        
    item, ok = QInputDialog.getItem(qid, "Outside layers:", "Add outside layers from Layers map:", items, 0, False)
    if item=="Just zones":
        THIS_FOLDER = os.path.dirname(os.path.abspath("__file__"))
        layer_list = QgsLayerDefinition().loadLayerDefinitionLayers(THIS_FOLDER+"\Layers\Cone z oznakami.qlr")
        QgsProject.instance().addMapLayers(layer_list)
    if item=="Zones with 100m population":
        THIS_FOLDER = os.path.dirname(os.path.abspath("__file__"))
        layer_list = QgsLayerDefinition().loadLayerDefinitionLayers(THIS_FOLDER+"\Layers\Zone with 100.qlr")
        QgsProject.instance().addMapLayers(layer_list)
    if item=="Zones with 500m population":
        print("Selected Zones with 500m population")
        THIS_FOLDER = os.path.dirname(os.path.abspath("__file__"))
        print(THIS_FOLDER)
        layer_list = QgsLayerDefinition().loadLayerDefinitionLayers(THIS_FOLDER+"\Layers\Zone with 500.qlr")
        QgsProject.instance().addMapLayers(layer_list)



#Window for choosing which one  
qid = QDialog()
items = ("Circles", "Squares", "Polygons", "None")        
item, ok = QInputDialog.getItem(qid, "Showing data on map", "Show data as:", items, 0, False)
#
#Layers functions
#
def krogci(data,layers,date):
    column_index=3
    urlWithParams = 'type=xyz&url=https://a.tile.openstreetmap.org/%7Bz%7D/%7Bx%7D/%7By%7D.png&zmax=19&zmin=0&crs=EPSG3857'
    rlayer = QgsRasterLayer(urlWithParams, 'OpenStreetMap', 'wms')  
    if rlayer.isValid():
        QgsProject.instance().addMapLayer(rlayer)
    else:
        print('invalid layer')
    
    def apply_graduated_symbology(layer):
        target_field = 'D [μSv/h]'
        myRenderer  = QgsGraduatedSymbolRenderer()
        myRenderer.setClassAttribute(target_field)
        color1=mcp.gen_color(cmap="autumn",n=column_index)
        border=[0,0.5,100,1000]
        def Group(index, min, max,layer):
            symbol = QgsSymbol.defaultSymbol(layer.geometryType())
            symbol.setColor(QColor(str(color1[index])))
            myRange = QgsRendererRange(min, max, symbol,str(min)+"-"+str(max)+" μSv/h")
            return myRange
        
        myRangeList = []
        for i in range(0,column_index):
            myRange=Group(i,border[i], border[i+1],layer)
            myRangeList.append(myRange) 

        myRenderer = QgsGraduatedSymbolRenderer(target_field, myRangeList)  
        myRenderer.setMode(QgsGraduatedSymbolRenderer.Custom)
        ramp = QgsCptCityColorRamp("grass/gyr","",False,True)
        myRenderer.updateColorRamp(ramp)
        layer.setRenderer(myRenderer)
        layer.setOpacity(0.75)
        layer.setName("Radioactivity dose")
        current_node = iface.layerTreeView().currentNode()
        QgsLayerDefinition().exportLayerDefinition(layers+"Points "+layer.name()+".qlr", [current_node])    

    def Creating_layer(file):
        uri="file:///"+data+file+"?type=regexp&delimiter=;&maxFields=10000&detectTypes=yes&decimalPoint=,&xField=E%20[Decimal%20degrees]&yField=N%20[Decimal%20degrees]&crs=EPSG:4326&spatialIndex=no&subsetIndex=no&watchFile=no"
        layer = QgsVectorLayer(uri, file, 'delimitedtext')
        layer.setScaleBasedVisibility(True)
        if file[0:2]=="XS":
            layer.setMinimumScale(50000.0)
            layer.setMaximumScale(20.0)
        if file[0:1]=="S":
            layer.setMinimumScale(200000.0)
            layer.setMaximumScale(50000.0)
        if file[0:1]=="L":
            layer.setMinimumScale(400000.0)
            layer.setMaximumScale(200000.0)
        if file[0:2]=="XL":
            layer.setMinimumScale(11000000.0)
            layer.setMaximumScale(400000.0)
        layer= QgsProject.instance().addMapLayer(layer)
        apply_graduated_symbology(layer)
    Creating_layer("XS "+date+".csv")
    Creating_layer("S "+date+".csv")
    Creating_layer("L "+date+".csv")
    Creating_layer("XL "+date+".csv")

def grid(data,layers,date):
    column_index=3

    urlWithParams = 'type=xyz&url=https://a.tile.openstreetmap.org/%7Bz%7D/%7Bx%7D/%7By%7D.png&zmax=19&zmin=0&crs=EPSG3857'
    rlayer = QgsRasterLayer(urlWithParams, 'OpenStreetMap', 'wms')  
    if rlayer.isValid():
        QgsProject.instance().addMapLayer(rlayer)
    else:
        print('invalid layer')

    layer_list = QgsLayerDefinition().loadLayerDefinitionLayers(THIS_FOLDER+'/Layers/Regije.qlr')
    QgsProject.instance().addMapLayers(layer_list)
    def creating_grid(name):
        crs = QgsProject().instance().crs().toWkt() # it is EPSG:3857 
        out1 = processing.run('native:creategrid', params_grid)
        grid = QgsVectorLayer(out1['OUTPUT'], 'Mreža XL', 'ogr')
        QgsProject().instance().addMapLayer(grid)

    def Creating_layer(file,data,layers,date):
        uri="file:///"+data+file+"?type=regexp&delimiter=;&maxFields=10000&detectTypes=yes&decimalPoint=,&xField=E%20[Decimal%20degrees]&yField=N%20[Decimal%20degrees]&crs=EPSG:4326&spatialIndex=no&subsetIndex=no&watchFile=no"
        layer = QgsVectorLayer(uri, file, 'delimitedtext')
        params_grid={}
        layer= QgsProject.instance().addMapLayer(layer)
        crs = QgsProject().instance().crs().toWkt() # it is EPSG:3857
        if file[0:2]=="XS":
            params_grid= {'TYPE':3,
                'EXTENT':'Regije',
                'HSPACING':0.001,
                'VSPACING':0.001,
                'HOVERLAY':0,
                'VOVERLAY':0,
                'CRS':crs,
                'OUTPUT':'memoryXS'}
        if file[0:1]=="S":
            params_grid= {'TYPE':3,
                'EXTENT':'Regije',
                'HSPACING':0.001,
                'VSPACING':0.001,
                'HOVERLAY':0,
                'VOVERLAY':0,
                'CRS':crs,
                'OUTPUT':'memoryS'}
        if file[0:1]=="L":
            params_grid= {'TYPE':3,
                'EXTENT':'Regije',
                'HSPACING':0.01,
                'VSPACING':0.01,
                'HOVERLAY':0,
                'VOVERLAY':0,
                'CRS':crs,
                'OUTPUT':'memoryL'}
        if file[0:2]=="XL":
            params_grid= {'TYPE':3,
                'EXTENT':'Regije',
                'HSPACING':0.1,
                'VSPACING':0.1,
                'HOVERLAY':0,
                'VOVERLAY':0,
                'CRS':crs,
                'OUTPUT':'memoryXL'}
        crs = QgsProject().instance().crs().toWkt()
        out1 = processing.run('native:creategrid', params_grid)
        grid = QgsVectorLayer(out1['OUTPUT'], 'Grid'+file, 'ogr')
        print("Printing grid")
        QgsProject().instance().addMapLayer(grid)
        params= {"POLYGONS": "Grid"+file,
                "POINTS": file,
                "WEIGHT": 'D [μSv/h]',
                "FIELD": 'D [μSv/h]',
                "OUTPUT": 'Mreža'+file[0:2]}
        out1=processing.run('qgis:countpointsinpolygon', params)
        grid = QgsVectorLayer(out1['OUTPUT'], "Mreža"+file[0:2], 'ogr')
        for lyr in ["Grid"+str(file),str(file)]:
            rmvLyr(lyr)
        grid.setScaleBasedVisibility(True)
        if file[0:2]=="XS":
            grid.setMinimumScale(50000.0)
            grid.setMaximumScale(20.0)
        if file[0:1]=="S":
            grid.setMinimumScale(50000.0)
            grid.setMaximumScale(1000.0)
        if file[0:1]=="L":
            grid.setMinimumScale(200000.0)
            grid.setMaximumScale(25000.0)
        if file[0:2]=="XL":
            grid.setMinimumScale(11000000.0)
            grid.setMaximumScale(200000.0)
        print("is working")
        QgsProject().instance().addMapLayer(grid)
        print("Printing map")
        apply_graduated_symbology(grid,data,layers,date)
    def apply_graduated_symbology(layer,data,layers,date):
        target_field = 'D [μSv/h]'
        myRenderer  = QgsGraduatedSymbolRenderer()
        myRenderer.setClassAttribute(target_field)
        color1=mcp.gen_color(cmap="autumn",n=column_index)
        border=[0.01,0.5,100,1000]
        def Group(index, min, max,layer):
            symbol = QgsSymbol.defaultSymbol(layer.geometryType())
            symbol.setColor(QColor(str(color1[index])))
            myRange = QgsRendererRange(min, max, symbol,str(min)+"-"+str(max)+" μSv/h")
            return myRange
        
        myRangeList = []
        for i in range(0,column_index):
            myRange=Group(i,border[i], border[i+1],layer)
            myRangeList.append(myRange) 

        myRenderer = QgsGraduatedSymbolRenderer(target_field, myRangeList)  
        myRenderer.setMode(QgsGraduatedSymbolRenderer.Custom)
        ramp = QgsCptCityColorRamp("grass/gyr","",False,True)
        myRenderer.updateColorRamp(ramp)
        layer.setRenderer(myRenderer)
        layer.setOpacity(0.75)
        layer.setName("Radioactivity dose")
        layer.setBlendMode(QPainter.CompositionMode_Darken)
        layer.setFeatureBlendMode(QPainter.CompositionMode_ColorDodge)    

    def Creating_layer_dots(file,data,layers,date):
        uri="file:///"+data+file+"?type=regexp&delimiter=;&maxFields=10000&detectTypes=yes&decimalPoint=,&xField=E%20[Decimal%20degrees]&yField=N%20[Decimal%20degrees]&crs=EPSG:4326&spatialIndex=no&subsetIndex=no&watchFile=no"
        layer = QgsVectorLayer(uri, file, 'delimitedtext')
        layer.setScaleBasedVisibility(True)
        if file[0:2]=="XS":
            layer.setMinimumScale(25000.0)
            layer.setMaximumScale(10.0)
        if file[0:1]=="L":
            layer.setMinimumScale(400000.0)
            layer.setMaximumScale(200000.0)
        if file[0:1]=="XL":
            layer.setMinimumScale(11000000.0)
            layer.setMaximumScale(400000.0)
        layer= QgsProject.instance().addMapLayer(layer)
        apply_graduated_symbology(layer,data,layers,date)
    Creating_layer("XL "+date+".csv",data,layers,date)    
    Creating_layer("L "+date+".csv",data,layers,date)
    rmvLyr("Regije")
def squares(data, layers, date):
    column_index=3

    #PRINTING STREET MAP
    urlWithParams = 'type=xyz&url=https://a.tile.openstreetmap.org/%7Bz%7D/%7Bx%7D/%7By%7D.png&zmax=19&zmin=0&crs=EPSG3857'
    rlayer = QgsRasterLayer(urlWithParams, 'OpenStreetMap', 'wms')


    if rlayer.isValid():
        QgsProject.instance().addMapLayer(rlayer)
    else:
        print('invalid layer')
    #
    #FUNCTION FOR COLORING DOTS
    #
    def apply_graduated_symbology_points(layer,border,color1):
        """Creates Symbology for each value in range of values. 
        Vir:https://data.library.virginia.edu/how-to-apply-a-graduated-color-symbology-to-a-layer-using-python-for-qgis-3/"""
        target_field = 'D [μSv/h]'
        def Group(index, min, max,layer):
            symbol = QgsSymbol.defaultSymbol(layer.geometryType())
            symbol.setColor(QColor(str(color1[index])))
            myRange = QgsRendererRange(min, max, symbol, str(min)+"-"+str(max)+" μSv/h")
            return myRange
        
        myRangeList = []
        for i in range(0,column_index):
            myRange=Group(i,border[i], border[i+1],layer)
            myRangeList.append(myRange) 

        myRenderer = QgsGraduatedSymbolRenderer(target_field, myRangeList)  
        myRenderer.setMode(QgsGraduatedSymbolRenderer.Custom)
        ramp = QgsCptCityColorRamp("wkp/precip/wiki-precip-mm","",False,True)
        myRenderer.updateColorRamp(ramp)    
        layer.setRenderer(myRenderer)
        layer.setName("Radioactivity dose")
        current_node = iface.layerTreeView().currentNode()
        QgsLayerDefinition().exportLayerDefinition(layers+"Points "+layer.name()+".qlr", [current_node])    
    #
    #FUNCTION FOR COLORING SQUARES
    #
    def apply_graduated_symbology(layer):
        target_field = 'D [ÎĽSv/h]'
        myRenderer  = QgsGraduatedSymbolRenderer()
        myRenderer.setClassAttribute(target_field)
        color1=mcp.gen_color(cmap="autumn",n=column_index)
        border=[0,0.5,100,1000]
        def Group(index, min, max,layer):
            symbol = QgsSymbol.defaultSymbol(layer.geometryType())
            symbol.setColor(QColor(str(color1[index])))
            myRange = QgsRendererRange(min, max, symbol,str(min)+"-"+str(max)+" μSv/h")
            return myRange
        
        myRangeList = []
        for i in range(0,column_index):
            myRange=Group(i,border[i], border[i+1],layer)
            myRangeList.append(myRange) 

        myRenderer = QgsGraduatedSymbolRenderer(target_field, myRangeList)  
        myRenderer.setMode(QgsGraduatedSymbolRenderer.Custom)
        ramp = QgsCptCityColorRamp("grass/gyr","",False,True)
        myRenderer.updateColorRamp(ramp)
        layer.setRenderer(myRenderer)
        layer.setOpacity(0.75)
        layer.setName("Radioactivity dose")
        current_node = iface.layerTreeView().currentNode()
        QgsLayerDefinition().exportLayerDefinition(THIS_FOLDER+"/Created_layers/Squares "+layer.name()+".qlr", [current_node])
    #layer.setBlendMode(QPainter.CompositionMode_Normal)
    #layer.setFeatureBlendMode(QPainter.CompositionMode_Normal)
    #
    #FUNCTION FOR CREATING SQUARES
    #
    def Creating_map(layer):
    #Getting the data max in min for labels
        target_field = 'D [μSv/h]'
        max=0
        min=0
        for feature in layer.getFeatures():
            number = feature['D [μSv/h]']
            if number >max:
                max=number
            if number < min:
                min=number

    #Creating colored groups
        column_index=5
        color1=mcp.gen_color(cmap="autumn",n=column_index)
        border=np.linspace(min,max,column_index+1)
        #apply_graduated_symbology_points(layer,border,color1)
        if layer.name()=="XS":
            params = {
                "INPUT": layer,
                "DISTANCE": 0.0005,
                "SEGMENTS": 4,
                "END_CAP_STYLE": 2,
                "OUTPUT": layers+"output"+layer.name()+".shp"}
        if layer.name()=="S ":
            params = {
                "INPUT": layer,
                "DISTANCE": 0.005,
                "SEGMENTS": 4,
                "END_CAP_STYLE": 2,
                "OUTPUT": layers+"output"+layer.name()+".shp"}
        if layer.name()=="L ":
            params = {
                "INPUT": layer,
                "DISTANCE": 0.005,
                "SEGMENTS": 4,
                "END_CAP_STYLE": 2,
                "OUTPUT": layers+"output"+layer.name()+".shp"}
        if layer.name()=="XL":
            params = {
                "INPUT": layer,
                "DISTANCE": 0.05,
                "SEGMENTS": 4,
                "END_CAP_STYLE": 2,
                "OUTPUT": THIS_FOLDER+"/Created_layers/output"+layer.name()+".shp"}
        out1=processing.run("native:buffer", params)
        grid = QgsVectorLayer(out1['OUTPUT'], "Buffed"+layer.name(), 'ogr')
        QgsProject().instance().addMapLayer(grid)
        grid.setScaleBasedVisibility(True)
        if "Buffed"+layer.name()=="BuffedXS":
            grid.setMinimumScale(25000.0)
            grid.setMaximumScale(20.0)
        #if "Buffed"+layer.name()=="BuffedS":
            #grid.setMinimumScale(25000.0)
            #grid.setMaximumScale(1000.0)
        if "Buffed"+layer.name()=="BuffedL ":
            grid.setMinimumScale(200000.0)
            grid.setMaximumScale(25000.0)
        if "Buffed"+layer.name()=="BuffedXL":
            grid.setMinimumScale(11000000.0)
            grid.setMaximumScale(200000.0)
        #QgsGeometryAnalyzer().buffer(layer, THIS_FOLDER+"output.shp", 0.05, False, False, -1)
        rmvLyr(layer.name())
        apply_graduated_symbology(grid)
    #
    #FUNCTION FOR CREATING LAYER
    #
    def Creating_layer(file):
        uri="file:///"+data+file+"?type=regexp&delimiter=;&maxFields=10000&detectTypes=yes&decimalPoint=,&xField=E%20[Decimal%20degrees]&yField=N%20[Decimal%20degrees]&crs=EPSG:4326&spatialIndex=no&subsetIndex=no&watchFile=no"
        layer = QgsVectorLayer(uri, file[0:2], 'delimitedtext')
        layer.setScaleBasedVisibility(True)
        if layer.name()=="XS":
            layer.setMinimumScale(25000.0)
            layer.setMaximumScale(20.0)
        #if layer.name()=="S":
            #layer.setMinimumScale(25000.0)
            #layer.setMaximumScale(10000.0)
        if layer.name()=="L":
            layer.setMinimumScale(200000.0)
            layer.setMaximumScale(25000.0)
        if layer.name()=="XL":
            layer.setMinimumScale(11000000.0)
            layer.setMaximumScale(200000.0)
        layer= QgsProject.instance().addMapLayer(layer)
        Creating_map(layer)
        
    Creating_layer("XL "+date+".csv")
    Creating_layer("XS "+date+".csv")
    Creating_layer("L "+date+".csv")
from datetime import datetime
now = datetime.now()
date = str(now.strftime("%d-%m-%Y_%H-%M-%S"))
if ok and item:
    if item=="Circles":
        #Datasets(date)
        print("Selected: Circles")
        created=dataSets(date,data_folder,created_layers)
        krogci(created,created_layers,date)
        #Window for choosing the layer of population
    if item=="Squares":
        print("Selected: Squares")
        created=dataSets(date,data_folder,created_layers)
        squares(created,created_layers,date)
        #Window for choosing the layer of population
    if item=="Polygons":
        print("Selected: Polygons")
        created=dataSets(date,data_folder,created_layers)
        grid(created,created_layers,date)
        #Window for choosing the layer of population
    if item=="None":
        print("Selected: None")
        urlWithParams = 'type=xyz&url=https://a.tile.openstreetmap.org/%7Bz%7D/%7Bx%7D/%7By%7D.png&zmax=19&zmin=0&crs=EPSG3857'
        rlayer = QgsRasterLayer(urlWithParams, 'OpenStreetMap', 'wms')  
        if rlayer.isValid():
            QgsProject.instance().addMapLayer(rlayer)
        else:
            print('invalid layer')
Zones_window()
#
#Save window
#
qid = QDialog()
items = ("None", "Slovenia map", "Krško map", "Both")        
item, ok = QInputDialog.getItem(qid, "Saving layers", "Save layer as:", items, 0, False)
save = saving_folder+"Output\\" 
if not os.path.exists(save):
    os.makedirs(save)        
if item=="Slovenia map":
    print("Selected: Slovenia map")
    from qgis.PyQt import QtGui
    #layers = QgsProject.instance().mapLayersByName('MrežaXL')
    layers = QgsProject.instance().mapLayersByName('Radioactivity dose')
    layer = layers[0]
    project = QgsProject.instance()
    manager = project.layoutManager()
    layoutName = 'Slovenia'
    layouts_list = manager.printLayouts()
    # remove any duplicate layouts
    for layout in layouts_list:
        if layout.name() == layoutName:
            manager.removeLayout(layout)
    layout = QgsPrintLayout(project)
    layout.initializeDefaults()
    layout.setName(layoutName)
    manager.addLayout(layout)

        # create map item in the layout
    map = QgsLayoutItemMap(layout)
    map.setRect(20, 200, 20, 20)

        # set the map extent
    ms = QgsMapSettings()
    ms.setLayers([layer]) # set layers to be mapped
    rect = QgsRectangle(13.271,45.375,16.723,46.685)
    rect.scale(1.0)
    ms.setExtent(rect)
    map.setExtent(rect)
    map.setBackgroundColor(QColor(255, 255, 255, 0))
    layout.addLayoutItem(map)

    map.attemptMove(QgsLayoutPoint(5, 8, QgsUnitTypes.LayoutMillimeters))
    map.attemptResize(QgsLayoutSize(285, 195, QgsUnitTypes.LayoutMillimeters))

    legend = QgsLayoutItemLegend(layout)
    #legend.setTitle("Prikaz radioaktivnosti,\nDoza [μSv/h]")
    layerTree = QgsLayerTree()
    layerTree.addLayer(layer)
    legend.model().setRootGroup(layerTree)
    layout.addLayoutItem(legend)
    legend.attemptMove(QgsLayoutPoint(225, 145, QgsUnitTypes.LayoutMillimeters))

    scalebar = QgsLayoutItemScaleBar(layout)
    scalebar.setStyle('Line Ticks Up')
    scalebar.setUnits(QgsUnitTypes.DistanceKilometers)
    scalebar.setNumberOfSegments(2)
    scalebar.setNumberOfSegmentsLeft(0)
    scalebar.setUnitsPerSegment(20)
    scalebar.setLinkedMap(map)
    scalebar.setUnitLabel('km')
    scalebar.setFont(QFont('Arial', 14))
    scalebar.update()
    layout.addLayoutItem(scalebar)
    scalebar.attemptMove(QgsLayoutPoint(225, 190, QgsUnitTypes.LayoutMillimeters))
    layoutItemPicture = QgsLayoutItemPicture(layout)
    layoutItemPicture.setResizeMode(QgsLayoutItemPicture.Zoom)
    layoutItemPicture.setMode(QgsLayoutItemPicture.FormatRaster)
    layoutItemPicture.setPicturePath("C:\IJS\Obdelava\Final\Kartiranje-radioaktivnosti\Layers\logo.jpg")

    dim_image_original = [1186, 360]
    new_dim = [i * 0.70 for i in dim_image_original]
    layoutItemPicture.attemptMove(QgsLayoutPoint(10, 180, QgsUnitTypes.LayoutMillimeters))
    layoutItemPicture.attemptResize(QgsLayoutSize(*new_dim, QgsUnitTypes.LayoutPixels))
    layout.addLayoutItem(layoutItemPicture)
    qid = QDialog()
    items = ("No", "Pdf", "png", "Both")        
    item, ok = QInputDialog.getItem(qid, "Prikaz", "Export layouts as:", items, 0, False)
    if item =="Pdf":
        print("Selected Pdf")
        layout = manager.layoutByName("Slovenia")
        exporter = QgsLayoutExporter(layout)
        exporter.exportToPdf(save+"Slovenia"+date+".pdf", QgsLayoutExporter.PdfExportSettings())
    if item =="png":
        print("Selected png")
        layout = manager.layoutByName("Slovenia")
        exporter = QgsLayoutExporter(layout)
        exporter.exportToImage(save+"Slovenia"+date+".png", QgsLayoutExporter.ImageExportSettings())
    if item =="Both":
        print("Selected Both")
        layout = manager.layoutByName("Slovenia")
        exporter = QgsLayoutExporter(layout)
        exporter.exportToPdf(saving_folder+"Slovenia"+date+".pdf", QgsLayoutExporter.PdfExportSettings())
        exporter.exportToImage(save+"Slovenia"+date+".png", QgsLayoutExporter.ImageExportSettings())
if item=="Krško map":
    print("Selected: Krško map")
    from qgis.PyQt import QtGui
    #layers = QgsProject.instance().mapLayersByName('MrežaXL')
    layers = QgsProject.instance().mapLayersByName('Radioactivity dose')
    layer = layers[0]
    project = QgsProject.instance()
    manager = project.layoutManager()
    layoutName = 'Krško'
    layouts_list = manager.printLayouts()
    # remove any duplicate layouts
    for layout in layouts_list:
        if layout.name() == layoutName:
            manager.removeLayout(layout)
    layout = QgsPrintLayout(project)
    layout.initializeDefaults()
    layout.setName(layoutName)
    manager.addLayout(layout)

        # create map item in the layout
    map = QgsLayoutItemMap(layout)
    map.setRect(20, 200, 20, 20)

        # set the map extent
    ms = QgsMapSettings()
    ms.setLayers([layer]) # set layers to be mapped
    rect = QgsRectangle(15.127,45.688,15.888,46.200)
    rect.scale(1.0)
    ms.setExtent(rect)
    map.setExtent(rect)
    map.setBackgroundColor(QColor(255, 255, 255, 0))
    layout.addLayoutItem(map)

    map.attemptMove(QgsLayoutPoint(5, 8, QgsUnitTypes.LayoutMillimeters))
    map.attemptResize(QgsLayoutSize(285, 195, QgsUnitTypes.LayoutMillimeters))

    legend = QgsLayoutItemLegend(layout)
    #legend.setTitle("Prikaz radioaktivnosti,\nDoza [μSv/h]")
    layerTree = QgsLayerTree()
    layerTree.addLayer(layer)
    legend.model().setRootGroup(layerTree)
    layout.addLayoutItem(legend)
    legend.attemptMove(QgsLayoutPoint(225, 145, QgsUnitTypes.LayoutMillimeters))

    scalebar = QgsLayoutItemScaleBar(layout)
    scalebar.setStyle('Line Ticks Up')
    scalebar.setUnits(QgsUnitTypes.DistanceKilometers)
    scalebar.setNumberOfSegments(2)
    scalebar.setNumberOfSegmentsLeft(0)
    scalebar.setUnitsPerSegment(3)
    scalebar.setLinkedMap(map)
    scalebar.setUnitLabel('km')
    scalebar.setFont(QFont('Arial', 14))
    scalebar.update()
    layout.addLayoutItem(scalebar)
    scalebar.attemptMove(QgsLayoutPoint(225, 190, QgsUnitTypes.LayoutMillimeters))
    layoutItemPicture = QgsLayoutItemPicture(layout)
    layoutItemPicture.setResizeMode(QgsLayoutItemPicture.Zoom)
    layoutItemPicture.setMode(QgsLayoutItemPicture.FormatRaster)
    layoutItemPicture.setPicturePath("C:\IJS\Obdelava\Final\Kartiranje-radioaktivnosti\Layers\logo.jpg")

    dim_image_original = [1186, 360]
    new_dim = [i * 0.70 for i in dim_image_original]
    layoutItemPicture.attemptMove(QgsLayoutPoint(10, 180, QgsUnitTypes.LayoutMillimeters))
    layoutItemPicture.attemptResize(QgsLayoutSize(*new_dim, QgsUnitTypes.LayoutPixels))
    layout.addLayoutItem(layoutItemPicture)
    qid = QDialog()
    items = ("No", "Pdf", "png", "Both")        
    item, ok = QInputDialog.getItem(qid, "Prikaz", "Export layouts as:", items, 0, False)
    if item =="Pdf":
        print("Selected Pdf")
        layout = manager.layoutByName("Krško")
        exporter = QgsLayoutExporter(layout)
        exporter.exportToPdf(save+"Krško"+date+".pdf", QgsLayoutExporter.PdfExportSettings())
    if item =="png":
        print("Selected png")
        layout = manager.layoutByName("Krško")
        exporter = QgsLayoutExporter(layout)
        exporter.exportToImage(save+"Krško"+date+".png", QgsLayoutExporter.ImageExportSettings())
    if item =="Both":
        print("Selected Both")
        layout = manager.layoutByName("Krško")
        exporter = QgsLayoutExporter(layout)
        exporter.exportToPdf(saving_folder+"Krško"+date+".pdf", QgsLayoutExporter.PdfExportSettings())
        exporter.exportToImage(save+"Krško"+date+".png", QgsLayoutExporter.ImageExportSettings())
if item=="Both":
    print("Selected: Both")
    from qgis.PyQt import QtGui
    #layers = QgsProject.instance().mapLayersByName('MrežaXL')
    layers = QgsProject.instance().mapLayersByName('Radioactivity dose')
    layer = layers[0]
    project = QgsProject.instance()
    manager = project.layoutManager()
    layoutName = 'Slovenia'
    layouts_list = manager.printLayouts()
    # remove any duplicate layouts
    for layout in layouts_list:
        if layout.name() == layoutName:
            manager.removeLayout(layout)
    layout = QgsPrintLayout(project)
    layout.initializeDefaults()
    layout.setName(layoutName)
    manager.addLayout(layout)

        # create map item in the layout
    map = QgsLayoutItemMap(layout)
    map.setRect(20, 200, 20, 20)

        # set the map extent
    ms = QgsMapSettings()
    ms.setLayers([layer]) # set layers to be mapped
    rect = QgsRectangle(13.271,45.375,16.723,46.685)
    rect.scale(1.0)
    ms.setExtent(rect)
    map.setExtent(rect)
    map.setBackgroundColor(QColor(255, 255, 255, 0))
    layout.addLayoutItem(map)

    map.attemptMove(QgsLayoutPoint(5, 8, QgsUnitTypes.LayoutMillimeters))
    map.attemptResize(QgsLayoutSize(285, 195, QgsUnitTypes.LayoutMillimeters))

    legend = QgsLayoutItemLegend(layout)
    #legend.setTitle("Prikaz radioaktivnosti,\nDoza [μSv/h]")
    layerTree = QgsLayerTree()
    layerTree.addLayer(layer)
    legend.model().setRootGroup(layerTree)
    layout.addLayoutItem(legend)
    legend.attemptMove(QgsLayoutPoint(225, 145, QgsUnitTypes.LayoutMillimeters))

    scalebar = QgsLayoutItemScaleBar(layout)
    scalebar.setStyle('Line Ticks Up')
    scalebar.setUnits(QgsUnitTypes.DistanceKilometers)
    scalebar.setNumberOfSegments(2)
    scalebar.setNumberOfSegmentsLeft(0)
    scalebar.setUnitsPerSegment(20)
    scalebar.setLinkedMap(map)
    scalebar.setUnitLabel('km')
    scalebar.setFont(QFont('Arial', 14))
    scalebar.update()
    layout.addLayoutItem(scalebar)
    scalebar.attemptMove(QgsLayoutPoint(225, 190, QgsUnitTypes.LayoutMillimeters))
    
    layoutItemPicture = QgsLayoutItemPicture(layout)
    layoutItemPicture.setResizeMode(QgsLayoutItemPicture.Zoom)
    layoutItemPicture.setMode(QgsLayoutItemPicture.FormatRaster)
    layoutItemPicture.setPicturePath("C:\IJS\Obdelava\Final\Kartiranje-radioaktivnosti\Layers\logo.jpg")

    dim_image_original = [1186, 360]
    new_dim = [i * 0.70 for i in dim_image_original]
    layoutItemPicture.attemptMove(QgsLayoutPoint(10, 180, QgsUnitTypes.LayoutMillimeters))
    layoutItemPicture.attemptResize(QgsLayoutSize(*new_dim, QgsUnitTypes.LayoutPixels))
    layout.addLayoutItem(layoutItemPicture)
        
    #KRŠKO MAP
    from qgis.PyQt import QtGui
    #layers = QgsProject.instance().mapLayersByName('MrežaXL')
    layers = QgsProject.instance().mapLayersByName('Radioactivity dose')
    layer = layers[0]
    project = QgsProject.instance()
    manager = project.layoutManager()
    layoutName = 'Krško'
    layouts_list = manager.printLayouts()
    # remove any duplicate layouts
    for layout in layouts_list:
        if layout.name() == layoutName:
            manager.removeLayout(layout)
    layout = QgsPrintLayout(project)
    layout.initializeDefaults()
    layout.setName(layoutName)
    manager.addLayout(layout)

        # create map item in the layout
    map = QgsLayoutItemMap(layout)
    map.setRect(20, 200, 20, 20)

        # set the map extent
    ms = QgsMapSettings()
    ms.setLayers([layer]) # set layers to be mapped
    rect = QgsRectangle(15.127,45.688,15.888,46.200)
    rect.scale(1.0)
    ms.setExtent(rect)
    map.setExtent(rect)
    map.setBackgroundColor(QColor(255, 255, 255, 0))
    layout.addLayoutItem(map)

    map.attemptMove(QgsLayoutPoint(5, 8, QgsUnitTypes.LayoutMillimeters))
    map.attemptResize(QgsLayoutSize(285, 195, QgsUnitTypes.LayoutMillimeters))

    legend = QgsLayoutItemLegend(layout)
    #legend.setTitle("Prikaz radioaktivnosti,\nDoza [μSv/h]")
    layerTree = QgsLayerTree()
    layerTree.addLayer(layer)
    legend.model().setRootGroup(layerTree)
    layout.addLayoutItem(legend)
    legend.attemptMove(QgsLayoutPoint(225, 145, QgsUnitTypes.LayoutMillimeters))

    scalebar = QgsLayoutItemScaleBar(layout)
    scalebar.setStyle('Line Ticks Up')
    scalebar.setUnits(QgsUnitTypes.DistanceKilometers)
    scalebar.setNumberOfSegments(2)
    scalebar.setNumberOfSegmentsLeft(0)
    scalebar.setUnitsPerSegment(3)
    scalebar.setLinkedMap(map)
    scalebar.setUnitLabel('km')
    scalebar.setFont(QFont('Arial', 14))
    scalebar.update()
    layout.addLayoutItem(scalebar)
    scalebar.attemptMove(QgsLayoutPoint(225, 190, QgsUnitTypes.LayoutMillimeters))
    
    layoutItemPicture = QgsLayoutItemPicture(layout)
    layoutItemPicture.setResizeMode(QgsLayoutItemPicture.Zoom)
    layoutItemPicture.setMode(QgsLayoutItemPicture.FormatRaster)
    layoutItemPicture.setPicturePath("C:\IJS\Obdelava\Final\Kartiranje-radioaktivnosti\Layers\logo.jpg")

    dim_image_original = [1186, 360]
    new_dim = [i * 0.70 for i in dim_image_original]
    layoutItemPicture.attemptMove(QgsLayoutPoint(10, 180, QgsUnitTypes.LayoutMillimeters))
    layoutItemPicture.attemptResize(QgsLayoutSize(*new_dim, QgsUnitTypes.LayoutPixels))
    layout.addLayoutItem(layoutItemPicture)
    qid = QDialog()
    items = ("No", "Pdf", "png", "Both")        
    item, ok = QInputDialog.getItem(qid, "Prikaz", "Export layouts as:", items, 0, False)
    if item =="Pdf":
        print("Selected Pdf")
        layout = manager.layoutByName("Krško")
        exporter = QgsLayoutExporter(layout)
        exporter.exportToPdf(save+"Krško"+date+".pdf", QgsLayoutExporter.PdfExportSettings())
        layout = manager.layoutByName("Slovenia")
        exporter = QgsLayoutExporter(layout)
        exporter.exportToPdf(save+"Slovenia"+date+".pdf", QgsLayoutExporter.PdfExportSettings())
    if item =="png":
        print("Selected png")
        layout = manager.layoutByName("Krško")
        exporter = QgsLayoutExporter(layout)
        exporter.exportToImage(save+"Krško"+date+".png", QgsLayoutExporter.ImageExportSettings())
        layout = manager.layoutByName("Slovenia")
        exporter = QgsLayoutExporter(layout)
        exporter.exportToImage(save+"Slovenia"+date+".png", QgsLayoutExporter.ImageExportSettings())
    if item =="Both":
        print("Selected Both")
        layout = manager.layoutByName("Krško")
        exporter = QgsLayoutExporter(layout)
        exporter.exportToPdf(save+"Krško"+date+".pdf", QgsLayoutExporter.PdfExportSettings())
        exporter.exportToImage(save+"Krško"+date+".png", QgsLayoutExporter.ImageExportSettings())
        layout = manager.layoutByName("Slovenia")
        exporter = QgsLayoutExporter(layout)
        exporter.exportToPdf(save+"Slovenia"+date+".pdf", QgsLayoutExporter.PdfExportSettings())
        exporter.exportToImage(save+"Slovenia"+date+".png", QgsLayoutExporter.ImageExportSettings())
    #exporter.exportToImage('/Users/ep9k/Desktop/TestLayout.png', QgsLayoutExporter.ImageExportSettings())

print("Done with program")