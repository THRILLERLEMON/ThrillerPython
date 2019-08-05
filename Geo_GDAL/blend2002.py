import os,sys
import numpy
from osgeo import ogr
from osgeo import gdal
from osgeo import osr

def creatbufferlyr(lyr,buff_dis,name):
    memory_driver = ogr.GetDriverByName('ESRI Shapefile')
    outpath='C:\\Users\\thril\\Desktop\\blend\\2002\\temp\\'+name
    memory_ds = memory_driver.CreateDataSource(outpath)
    buff_lyr = memory_ds.CreateLayer('buffer',lyr.GetSpatialRef())
    buff_feat = ogr.Feature(buff_lyr.GetLayerDefn())
    featureCount = lyr.GetFeatureCount()
    for i in range(featureCount):
        feat = lyr.GetNextFeature()
        featgeom=feat.geometry()
        buff_geom=featgeom.Buffer(buff_dis)
        buff_feat.SetGeometry(buff_geom)
        buff_lyr.CreateFeature(buff_feat)
        # print(feat.geometry().GetArea())
        # print(buff_feat.geometry().GetArea())
    print(buff_lyr.GetFeatureCount())
    return buff_lyr

ogr.RegisterAll()
lpareads=ogr.Open('C:\\Users\\thril\\Desktop\\blend\\LP_area\\LP_AREA.shp')
lparea=lpareads.GetLayerByIndex(0)
if lparea is None:
    print('cannot open lparea')
    sys.exit(1)
roadds=ogr.Open('C:\\Users\\thril\\Desktop\\blend\\2002\\2002road.shp')
road=roadds.GetLayerByIndex(0)
if road is None:
    print('cannot open road')
    sys.exit(1)
railds=ogr.Open('C:\\Users\\thril\\Desktop\\blend\\2002\\2002rail.shp')
rail=railds.GetLayerByIndex(0)
if rail is None:
    print('cannot open rail')
    sys.exit(1)
print('already input shp')

road_driver = ogr.GetDriverByName('ESRI Shapefile')
road_ds = road_driver.CreateDataSource('C:\\Users\\thril\\Desktop\\blend\\2002\\temp\\roadbuffer')
roadbuff_lyr = road_ds.CreateLayer('buffer',road.GetSpatialRef())
roadbuff_feat = ogr.Feature(roadbuff_lyr.GetLayerDefn())
roadfeatureCount = road.GetFeatureCount()
for i in range(roadfeatureCount):
    feat = road.GetNextFeature()
    featgeom=feat.geometry()
    buff_geom=featgeom.Buffer(50)
    roadbuff_feat.SetGeometry(buff_geom)
    roadbuff_lyr.CreateFeature(roadbuff_feat)

rail_driver = ogr.GetDriverByName('ESRI Shapefile')
rail_ds = rail_driver.CreateDataSource('C:\\Users\\thril\\Desktop\\blend\\2002\\temp\\railbuffer')
railbuff_lyr = rail_ds.CreateLayer('buffer',rail.GetSpatialRef())
railbuff_feat = ogr.Feature(railbuff_lyr.GetLayerDefn())
railfeatureCount = rail.GetFeatureCount()
for i in range(railfeatureCount):
    feat = rail.GetNextFeature()
    featgeom=feat.geometry()
    buff_geom=featgeom.Buffer(50)
    railbuff_feat.SetGeometry(buff_geom)
    railbuff_lyr.CreateFeature(railbuff_feat)

print('already buffer')

memorydriver = ogr.GetDriverByName('ESRI Shapefile')
memoryds = memorydriver.CreateDataSource('C:\\Users\\thril\\Desktop\\blend\\2002\\temp\\union')
union_lyr = memoryds.CreateLayer('union',road.GetSpatialRef())
roadbuff_lyr.Union(railbuff_lyr,union_lyr)
print('already union')

tf=gdal.Open(r'C:\Users\thril\Desktop\blend\classified2002-01-01.tif')
if tf is None:
    print ('cannot open tif')
    sys.exit(1)
tfPro=tf.GetProjection()
tfTra=tf.GetGeoTransform()
print(tfTra)
tfband=tf.GetRasterBand(1)
tfXSize=tfband.XSize
tfYSize=tfband.YSize
print(tfXSize)
print(tfYSize)
cols=tf.RasterXSize
rows=tf.RasterYSize
imgdriver = gdal.GetDriverByName('GTiff')
new_raster = imgdriver.Create(r'C:\Users\thril\Desktop\blend\2002\new_raster.tif', tfXSize, tfYSize, 1, gdal.GDT_Byte)
new_raster.SetGeoTransform(tfTra)
new_raster.SetProjection(tfPro)
new_band = new_raster.GetRasterBand(1)
new_band.SetNoDataValue(-9999)
new_band.FlushCache()
gdal.RasterizeLayer(new_raster, [1], union_lyr, burn_values=[222])
newData=new_band.ReadAsArray(0,0,cols,rows)
tfData=tfband.ReadAsArray(0,0,cols,rows)
newNoData=new_band.GetNoDataValue()
tfNoData=tfband.GetNoDataValue()
tfData[newData==222]=502
resultPath = r'C:\Users\thril\Desktop\blend\2002\result_landuse.tif'
resultds = imgdriver.Create(resultPath, cols, rows, 1, tfband.DataType)
resultds.SetGeoTransform(tfTra)
resultds.SetProjection(tfPro)
resultds.GetRasterBand(1).WriteArray(tfData)    
resultds = None
print('ok!')

