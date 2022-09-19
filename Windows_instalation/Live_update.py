#
#IZDELAVA DATOTEK ZA DELO
# 
import numpy as np 
import os
import pandas as pd
THIS_FOLDER = os.path.dirname(os.path.abspath("__file__"))
import shutil

#THIS_FOLDER=THIS_FOLDER+"\Obdelava\\"
def Datasets(date):
    saving = THIS_FOLDER+"\Data\Created\Saved_files\\"
    if not os.path.exists(saving):
        os.makedirs(saving)
    for i in ["Datafile "+date+".csv", "XS "+date+".csv","S "+date+".csv","L "+date+".csv","XL "+date+".csv"]:
        if os.path.exists(THIS_FOLDER + "\Data\Created\\"+i):
            now_1 = datetime.now()
            date_1 = now_1.strftime("%d-%m-%Y_%H-%M-%S")
            shutil.copyfile(THIS_FOLDER + "\Data\Created\\"+i, saving+i[:-23]+date_1+".csv")
            with open(THIS_FOLDER+"\Data\Created\\"+i,'r+') as file:
                file.truncate(0)
    if os.path.exists(THIS_FOLDER + "\Data\Created\Datafile.csv"):
        os.remove(THIS_FOLDER + "\Data\Created\Datafile.csv")
    def Delete_existing(filename):
        if os.path.exists(THIS_FOLDER + "\\"+str(filename)):
            fo = open(THIS_FOLDER + "\\"+str(filename), "wb")
            fo.close()
            os.remove(THIS_FOLDER + "\\"+str(filename))
    #dir_list=os.listdir(THIS_FOLDER+"\Created_layers")
    """for i in dir_list:
        #print(os.path.splitext(i)[0][:6])
        if  os.path.splitext(i)[0][:6]=="output":
            os.remove(THIS_FOLDER+"\Created_layers"+"\\"+i)"""
            #print("Done with:" +str(i))"""
            
    for i in ["Datafile.csv", "XS.csv","S.csv","L.csv","XL.csv","MrežaXL.csv"]:
        Delete_existing("\Data\\"+i)
        #print("Done deleting previus.")
    dir_list = os.listdir(THIS_FOLDER)

    with open(THIS_FOLDER + "\Data\Created\Datafile "+date+".csv","a") as file :
        file.write("\"N;Date;Time;N [Decimal degrees];E [Decimal degrees];GPS uncertainty [m];h [m];Location provider;D [ÎĽSv/h];Standard deviation;Standard error of the mean value;CF;Number of measured points\".\n")
    #print("Creating new datafile")
    def Editing(filename):
        with open(THIS_FOLDER + "\\Data\\"+ filename, 'r') as file :
            filedata = file.read()
    # Replace the target string
        filedata = filedata.replace('\".\"', ';')
    # Write the file out again
        with open(THIS_FOLDER + "\Data\Created\Datafile "+date+".csv","a") as file :
            file.writelines(filedata[191:])
    file.close()

    dir_list = os.listdir(THIS_FOLDER+"\Data")

    for i in dir_list:
        if i.endswith(".csv") and i!=THIS_FOLDER+"\Data\Datafile.csv":
            #print("Start with:"+str(i))
            a=Editing(str(i))
            #print("Done with:" +str(i))
      
    data = np.loadtxt(THIS_FOLDER + "\Data\Created\Datafile "+date+".csv",delimiter=";", dtype=str)

#data=pd.read_csv(THIS_FOLDER+ "\Start_iz_IJS_normal.csv", delimiter=";",dtype=str)
    df=pd.DataFrame(data[1:],columns =data[0])
    df.rename(columns = {"D [ÎĽSv/h]":r"D [μSv/h]"}, inplace = True)

    """idx=df.groupby(['N [Decimal degrees]','E [Decimal degrees]'])[r'D [μSv/h]'].transform(max) == df[r'D [μSv/h]']
    if os.path.exists(THIS_FOLDER + THIS_FOLDER+'\Podatki.csv'):
    os.remove(THIS_FOLDER+'\Podatki.csv')
    df[idx].to_csv(THIS_FOLDER+'\Podatki.csv',sep=';')"""
    #Small data
    inx=df.sort_values('D [μSv/h]').groupby(['N [Decimal degrees]','E [Decimal degrees]']).tail(1)
    #if os.path.exists(THIS_FOLDER +"\Data\Created\XS "+date+".csv"):
        #os.remove(THIS_FOLDER+"\Data\Created\XS "+date+".csv")
    outfile = open(THIS_FOLDER+"\Data\Created\XS "+date+".csv", 'wb')
    inx.to_csv(THIS_FOLDER+"\Data\Created\XS "+date+".csv",sep=';')
    outfile.close()
    
    #Medium data
    df['N [Decimal degrees]']=df['N [Decimal degrees]'].astype(float).round(decimals = 2)
    df['E [Decimal degrees]']=df['E [Decimal degrees]'].astype(float).round(decimals = 2)
    inx=df.sort_values('D [μSv/h]').groupby(['N [Decimal degrees]','E [Decimal degrees]']).tail(1)
    
    #if os.path.exists(THIS_FOLDER +"\Data\Created\L "+date+".csv"):
        #os.remove(THIS_FOLDER+"\Data\Created\L "+date+".csv")
    outfile = open(THIS_FOLDER+"\Data\Created\L "+date+".csv", 'wb')
    inx.to_csv(THIS_FOLDER+"\Data\Created\L "+date+".csv",sep=';')
    outfile.close()
    
    def round_off_rating(x, base=5):
        return base * round(x/base,3)
    df['N [Decimal degrees]']=round_off_rating(df['N [Decimal degrees]'])
    df['E [Decimal degrees]']=round_off_rating(df['E [Decimal degrees]'])
    inx=df.sort_values('D [μSv/h]').groupby(['N [Decimal degrees]','E [Decimal degrees]']).tail(1)

    if os.path.exists(THIS_FOLDER +"\Data\Created\S "+date+".csv"):
        os.remove(THIS_FOLDER+"\Data\Created\S "+date+".csv")
    outfile = open(THIS_FOLDER+"\Data\Created\S "+date+".csv", 'wb')
    inx.to_csv(THIS_FOLDER+"\Data\Created\S "+date+".csv",sep=';')
    outfile.close()
    #Big data
    df['N [Decimal degrees]']=df['N [Decimal degrees]'].astype(float).round(decimals = 1)
    df['E [Decimal degrees]']=df['E [Decimal degrees]'].astype(float).round(decimals = 1)
    inx=df.sort_values('D [μSv/h]').groupby(['N [Decimal degrees]','E [Decimal degrees]']).tail(1)
    #if os.path.exists(THIS_FOLDER +"\Data\Created\XL "+date+".csv"):
        #os.remove(THIS_FOLDER+"\Data\Created\XL "+date+".csv")
    outfile = open(THIS_FOLDER+"\Data\Created\XL "+date+".csv", 'wb')
    inx.to_csv(THIS_FOLDER+"\Data\Created\XL "+date+".csv",sep=';')
    outfile.close()
#
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

import os
import pandas as pd
#Function for removing not needed layers

def rmvLyr(lyrname):
    qinst = QgsProject.instance()
    qinst.removeMapLayer(qinst.mapLayersByName(lyrname)[0].id())

column_index=3
def Reseting(date):
    def apply_graduated_symbology_points(layer,border,color1,date):
        target_field = 'D [μSv/h]'
        def Group(index, min, max,layer):
            symbol = QgsSymbol.defaultSymbol(layer.geometryType())
            get_styles = QgsStyle.defaultStyle()
            symbol.setColor(QColor(str(color1[index])))
            if layer.name()=="XL":
                symbol.setSize(0.1)
                symbol.setSizeUnit(1)
            if layer.name()=="L":
                symbol.setSize(0.01)
                symbol.setSizeUnit(1)
            if layer.name()=="XS":
                symbol.setSize(0.001)
                symbol.setSizeUnit(1)
            myRange = QgsRendererRange(min, max, symbol,str(index)+", "+str(min)+"-"+str(max)+" μSv/h")
            return myRange
        
        myRangeList = []
        for i in range(0,column_index):
            myRange=Group(i,border[i], border[i+1],layer)
            myRangeList.append(myRange) 

        myRenderer = QgsGraduatedSymbolRenderer(target_field, myRangeList)  
        myRenderer.setMode(QgsGraduatedSymbolRenderer.Custom)
        #myRenderer.setSymbolSizes(5,5)
        if layer.name()=="XS":
            layer.loadNamedStyle(THIS_FOLDER+"\Layers\S.qml")
        if layer.name()=="L":
            layer.loadNamedStyle(THIS_FOLDER+"\Layers\L.qml")
        if layer.name()=="XL":
            layer.loadNamedStyle(THIS_FOLDER+"\Layers\XL.qml")
        ramp = QgsCptCityColorRamp("grass/gyr","",False,True)
        myRenderer.updateColorRamp(ramp)
        #layer.setRenderer(myRenderer)
        #current_node = iface.layerTreeView().currentNode()
        #QgsLayerDefinition().exportLayerDefinition(THIS_FOLDER+"/Created_layers/Points "+layer.name()+" "+date+".qlr", [current_node])    
    #
    #FUNCTION FOR COLORING SQUARES
    #
    def apply_graduated_symbology(layer,date):
        target_field = 'D [μSv/h]'
        myRenderer  = QgsGraduatedSymbolRenderer()
        myRenderer.setClassAttribute(target_field)
        color1=mcp.gen_color(cmap="autumn",n=column_index)
        border=[0,0.5,100,1000]
        def Group(index, min, max,layer):
            symbol = QgsSymbol.defaultSymbol(layer.geometryType())
            symbol.setColor(QColor(str(color1[index])))
            myRange = QgsRendererRange(min, max, symbol, 'Group'+str(index)+", "+str(min)+"-"+str(max))
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
        #current_node = iface.layerTreeView().currentNode()
        #QgsLayerDefinition().exportLayerDefinition(THIS_FOLDER+"/Created_layers/Squares "+layer.name()+" "+date+".qlr", [current_node])
    #layer.setBlendMode(QPainter.CompositionMode_Normal)
    #layer.setFeatureBlendMode(QPainter.CompositionMode_Normal)
    #
    #FUNCTION FOR CREATING SQUARES
    #
    def Creating_map(layer,date):
        #Getting the data max in min for labels
        target_field = 'D [μSv/h]'
    #Creating colored groups
        column_index=5
        border=[0,0.5,100,1000]
        color1=mcp.gen_color(cmap="autumn",n=column_index)
        apply_graduated_symbology_points(layer,border,color1,date)
        """if layer.name()=="XS":
            params = {
                "INPUT": layer,
                "DISTANCE": 0.0005,
                "SEGMENTS": 4,
                "END_CAP_STYLE": 2,
                "OUTPUT": THIS_FOLDER+"\Created_layers\output"+layer.name()+" "+date+".shp"}
        if layer.name()=="S":
            params = {
                "INPUT": layer,
                "DISTANCE": 0.005,
                "SEGMENTS": 4,
                "END_CAP_STYLE": 2,
                "OUTPUT": THIS_FOLDER+"\Created_layers\output"+layer.name()+" "+date+".shp"}
        if layer.name()=="L":
            params = {
                "INPUT": layer,
                "DISTANCE": 0.005,
                "SEGMENTS": 4,
                "END_CAP_STYLE": 2,
                "OUTPUT": THIS_FOLDER+"\Created_layers\output"+layer.name()+" "+date+".shp"}
        if layer.name()=="XL":
            params = {
                "INPUT": layer,
                "DISTANCE": 0.05,
                "SEGMENTS": 4,
                "END_CAP_STYLE": 2,
                "OUTPUT":  THIS_FOLDER+"\Created_layers\output"+layer.name()+" "+date+".shp"}
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
        if "Buffed"+layer.name()=="BuffedL":
            grid.setMinimumScale(200000.0)
            grid.setMaximumScale(25000.0)
        if "Buffed"+layer.name()=="BuffedXL":
            grid.setMinimumScale(11000000.0)
            grid.setMaximumScale(200000.0)
        grid.setAutoRefreshEnabled(True)
        # Set seconds (5 seconds)
        grid.setAutoRefreshInterval(2000)
        grid.setAutoRefreshEnabled(True)"""
        #QgsGeometryAnalyzer().buffer(layer, THIS_FOLDER+"output.shp", 0.05, False, False, -1)
        #rmvLyr(layer.name())
        #apply_graduated_symbology(grid,date)
    #
    #FUNCTION FOR CREATING LAYER
    #
    def Creating_layer(name,file,date):
        uri="file:///"+THIS_FOLDER+"/Data/Created/"+file+"?type=regexp&delimiter=;&maxFields=10000&detectTypes=yes&decimalPoint=,&xField=E%20[Decimal%20degrees]&yField=N%20[Decimal%20degrees]&crs=EPSG:4326&spatialIndex=no&subsetIndex=no&watchFile=no"
        layer = QgsVectorLayer(uri, name, 'delimitedtext')
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
        layer.setAutoRefreshEnabled(True)
        # Set seconds (5 seconds)
        layer.setAutoRefreshInterval(2000)
        layer.setAutoRefreshEnabled(True)
        Creating_map(layer,date)
    Creating_layer("XS","XS "+date+".csv",date)
    #Creating_layer("S.csv")
    Creating_layer("L","L "+date+".csv",date)
    Creating_layer("XL","XL "+date+".csv",date)
    
from datetime import datetime
import time
now = datetime.now()
date = now.strftime("%d-%m-%Y_%H-%M-%S")
Datasets(date)

urlWithParams = 'type=xyz&url=https://a.tile.openstreetmap.org/%7Bz%7D/%7Bx%7D/%7By%7D.png&zmax=19&zmin=0&crs=EPSG3857'
rlayer = QgsRasterLayer(urlWithParams, 'OpenStreetMap', 'wms')  
if rlayer.isValid():
    QgsProject.instance().addMapLayer(rlayer)
else:
    print('invalid layer')
Reseting(date)
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
    """layers = QgsProject.instance().mapLayersByName('XL')
    layer = layers[0]
    Creating_map(layer,date)
    layers = QgsProject.instance().mapLayersByName('L')
    layer = layers[0]
    Creating_map(layer,date)
    layers = QgsProject.instance().mapLayersByName('XS')
    layer = layers[0]
    Creating_map(layer,date)"""
    #rmvLyr("XL")
    print("Done Creating dataset")
    print("Reseting")
    #Reseting(date)
    i+=1
    print(i)
    print("Done reseting")
    now_2 = datetime.now()
    date_2 = now_2.strftime("%d-%m-%Y_%H-%M-%S")
    from qgis.PyQt import QtGui
    #layers = QgsProject.instance().mapLayersByName('MrežaXL')
    layers = QgsProject.instance().mapLayersByName('XL')
    layer = layers[0]
    project = QgsProject.instance()
    manager = project.layoutManager()
    layoutName = 'Zemljevid Slovenije'+date
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
    #legend.setTitle("Prikaz radioaktivnosti,/nDoza [μSv/h]")
    layerTree = QgsLayerTree()
    layerTree.addLayer(layer)
    legend.model().setRootGroup(layerTree)
    layout.addLayoutItem(legend)
    legend.attemptMove(QgsLayoutPoint(225, 160, QgsUnitTypes.LayoutMillimeters))

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
    layoutItemPicture.setPicturePath(THIS_FOLDER+"/Layers/Logo.jpg")

    dim_image_original = [1186, 360]
    new_dim = [i * 0.70 for i in dim_image_original]
    layoutItemPicture.attemptMove(QgsLayoutPoint(10, 180, QgsUnitTypes.LayoutMillimeters))
    layoutItemPicture.attemptResize(QgsLayoutSize(*new_dim, QgsUnitTypes.LayoutPixels))
    layout.addLayoutItem(layoutItemPicture)
    layout = manager.layoutByName("Zemljevid Slovenije"+date)
    exporter = QgsLayoutExporter(layout)
    #exporter.exportToPdf(THIS_FOLDER+"\\Output\\"+"Slovenia "+date+".pdf", QgsLayoutExporter.PdfExportSettings())
    exporter.exportToImage(THIS_FOLDER+"\\Output\\"+"Slovenia "+date_2+".png", QgsLayoutExporter.ImageExportSettings())
    if i==5:
        return print("Done 5 times")
        run=False
    if run==True:
        Timer(10, test).start()
test()
