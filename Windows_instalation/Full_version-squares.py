from osgeo import gdal
import qgis
import os
import numpy as np
import matplotlib.cm as cm
import matplotlib.pyplot as plt
from mycolorpy import colorlist as mcp

import os
import pandas as pd

from PyQt5.QtWidgets import QInputDialog, QLineEdit, QDialog, QApplication, QDialogButtonBox, QFormLayout
#DODAJ VSEM
from PyQt5.QtGui import QColor, QFont
from qgis.utils import iface

class InputDialog_DATA(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Map of Radioactivity in Slovenia")
        self.first = QLineEdit(self)
        self.third = QLineEdit(self)
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self);

        layout = QFormLayout(self)
        layout.addRow("Datafile (full path)", self.first)
        layout.addRow("File for created PDF,png,SVG (full path)", self.third)
        layout.addWidget(buttonBox)

        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

    def getInputs(self):
        return (self.first.text(), self.third.text())


THIS_FOLDER = os.path.dirname(os.path.abspath("__file__"))
folders = InputDialog_DATA()
if folders.exec():
    FILES=np.array(folders.getInputs())
    if FILES[0]=='':
        data_folder=THIS_FOLDER+"\\Data\\"
    else:
        data_folder=FILES[0]+"\\"
    if FILES[1]=='':
        saving_folder = THIS_FOLDER+"\\Output\\"
        if not os.path.exists(saving_folder):
            os.makedirs(saving_folder)
        saving_folder=THIS_FOLDER+"\\Output\\"
    else:
        saving_folder=FILES[1]+"\\"
print("Selected paths: Datafile:"+ data_folder+ "\nFile for created PDF,png,SVG:"+saving_folder)
#
def dataSets(date,data):
    if os.path.exists(data+"\Created\Datafile "+str(date)+".csv"):
        os.remove(data+"\Created\Datafile "+str(date)+".csv")
    def Delete_existing(filename):
        if os.path.exists(data+str(filename)):
            fo = open(data+str(filename), "wb")
            fo.close()
            os.remove(data+str(filename))
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
    
from datetime import datetime
now = datetime.now()
date = str(now.strftime("%d-%m-%Y_%H-%M-%S"))

created=dataSets(date,data_folder)
#IZDELAVA LAYERJEV
#
from osgeo import gdal
import qgis
import os
import numpy as np
import matplotlib.cm as cm
import matplotlib.pyplot as plt
from mycolorpy import colorlist as mcp
cm = plt.cm.Reds
from processing.core.Processing import processing

import os
import pandas as pd

column_index=3

urlWithParams = 'type=xyz&url=https://a.tile.openstreetmap.org/%7Bz%7D/%7Bx%7D/%7By%7D.png&zmax=19&zmin=0&crs=EPSG3857'
rlayer = QgsRasterLayer(urlWithParams, 'OpenStreetMap', 'wms')  
if rlayer.isValid():
    QgsProject.instance().addMapLayer(rlayer)
else:
    print('invalid layer')
def rmvLyr(lyrname):
    qinst = QgsProject.instance()
    qinst.removeMapLayer(qinst.mapLayersByName(lyrname)[0].id())

column_index=3

#PRINTING STREET MAP
    

#QgsLayerDefinition.loadLayerDefinition(THIS_FOLDER+'Layer 500.qlr',QgsProject.instance(), QgsProject.instance().QgsLayerTreeGroup())
#layer_list = QgsLayerDefinition().loadLayerDefinitionLayers(THIS_FOLDER+'/Layers/Layer 500 opacity.qlr')
#QgsProject.instance().addMapLayers(layer_list)

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
    layer.setName("Doza radioaktivnosti")
    current_node = iface.layerTreeView().currentNode()
    QgsLayerDefinition().exportLayerDefinition(THIS_FOLDER+"/Created_layers/Points "+layer.name()+".qlr", [current_node])    
    print(f"Graduated color scheme applied")
#
#FUNCTION FOR COLORING SQUARES
#
def apply_graduated_symbology(layer,date):
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
    current_node = iface.layerTreeView().currentNode()
    QgsLayerDefinition().exportLayerDefinition(layers_save+"Squares "+layer.name()+" "+date+".qlr", [current_node])
    layer.setName("Radioactivity Dose")
    #layer.setBlendMode(QPainter.CompositionMode_Normal)
    #layer.setFeatureBlendMode(QPainter.CompositionMode_Normal)
#
#FUNCTION FOR CREATING SQUARES
#
def Creating_map(layer,date):
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
    print(layers_save+"output"+layer.name()+".shp")
    if layer.name()=="XS ":
        params = {
            "INPUT": layer,
            "DISTANCE": 0.0005,
            "SEGMENTS": 4,
            "END_CAP_STYLE": 2,
            "OUTPUT": layers_save+"output"+layer.name()+" "+date+".shp"}
    if layer.name()=="S ":
        params = {
            "INPUT": layer,
            "DISTANCE": 0.005,
            "SEGMENTS": 4,
            "END_CAP_STYLE": 2,
            "OUTPUT": layers_save+"output"+layer.name()+" "+date+".shp"}
    if layer.name()=="L ":
        params = {
            "INPUT": layer,
            "DISTANCE": 0.005,
            "SEGMENTS": 4,
            "END_CAP_STYLE": 2,
            "OUTPUT": layers_save+"output"+layer.name()+" "+date+".shp"}
    if layer.name()=="XL ":
        params = {
            "INPUT": layer,
            "DISTANCE": 0.05,
            "SEGMENTS": 4,
            "END_CAP_STYLE": 2,
            "OUTPUT": layers_save+"output"+layer.name()+" "+date+".shp"}
    out1=processing.run("native:buffer", params)
    grid = QgsVectorLayer(out1['OUTPUT'], "Buffed"+layer.name(), 'ogr')
    QgsProject().instance().addMapLayer(grid)
    grid.setScaleBasedVisibility(True)
    if "Buffed"+layer.name()=="BuffedXS ":
        grid.setMinimumScale(25000.0)
        grid.setMaximumScale(20.0)
    #if "Buffed"+layer.name()=="BuffedS":
        #grid.setMinimumScale(25000.0)
        #grid.setMaximumScale(1000.0)
    if "Buffed"+layer.name()=="BuffedL ":
        grid.setMinimumScale(200000.0)
        grid.setMaximumScale(25000.0)
    if "Buffed"+layer.name()=="BuffedXL ":
        grid.setMinimumScale(11000000.0)
        grid.setMaximumScale(200000.0)
    #QgsGeometryAnalyzer().buffer(layer, THIS_FOLDER+"output.shp", 0.05, False, False, -1)
    rmvLyr(layer.name())
    apply_graduated_symbology(grid,date)
#
#FUNCTION FOR CREATING LAYER
#
def Creating_layer(file,date):
    uri="file:///"+created+file+date+".csv"+"?type=regexp&delimiter=;&maxFields=10000&detectTypes=yes&decimalPoint=,&xField=E%20[Decimal%20degrees]&yField=N%20[Decimal%20degrees]&crs=EPSG:4326&spatialIndex=no&subsetIndex=no&watchFile=no"
    layer = QgsVectorLayer(uri, file, 'delimitedtext')
    layer.setScaleBasedVisibility(True)
    if file[0:2]=="XS":
        layer.setMinimumScale(25000.0)
        layer.setMaximumScale(20.0)
    #if layer.name()=="S":
        #layer.setMinimumScale(25000.0)
        #layer.setMaximumScale(10000.0)
    if file[0:1]=="L":
        layer.setMinimumScale(200000.0)
        layer.setMaximumScale(25000.0)
    if file[0:2]=="XL":
        layer.setMinimumScale(11000000.0)
        layer.setMaximumScale(200000.0)
    layer= QgsProject.instance().addMapLayer(layer)
    Creating_map(layer,date)

layers_save = created+"Layers\\" 
if not os.path.exists(layers_save):
    os.makedirs(layers_save)        
Creating_layer("XS ",date)
#Creating_layer("S.csv")
Creating_layer("L ",date)
Creating_layer("XL ",date)


from qgis.PyQt import QtGui

#layers = QgsProject.instance().mapLayersByName('MrežaXL')
layers = QgsProject.instance().mapLayersByName('Radioactivity Dose')
layer = layers[0]

project = QgsProject.instance()
manager = project.layoutManager()
layoutName = 'Zemljevid Slovenije'
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
legend.attemptMove(QgsLayoutPoint(225, 150, QgsUnitTypes.LayoutMillimeters))

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
layoutItemPicture.setPicturePath(THIS_FOLDER+"\Layers\logo.jpg")

dim_image_original = [1186, 360]
new_dim = [i * 0.70 for i in dim_image_original]
layoutItemPicture.attemptMove(QgsLayoutPoint(10, 180, QgsUnitTypes.LayoutMillimeters))
layoutItemPicture.attemptResize(QgsLayoutSize(*new_dim, QgsUnitTypes.LayoutPixels))
layout.addLayoutItem(layoutItemPicture)

layout = manager.layoutByName("Zemljevid Slovenije")
exporter = QgsLayoutExporter(layout)
exporter.exportToPdf(saving_folder+"Slovenia"+date+".pdf", QgsLayoutExporter.PdfExportSettings())
exporter.exportToImage(saving_folder+"Slovenia"+date+".png", QgsLayoutExporter.ImageExportSettings())