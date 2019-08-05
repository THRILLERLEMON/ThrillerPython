import os,sys
import numpy
from osgeo import ogr
from osgeo import gdal
from osgeo import osr

def creatbufferlyr(lyr,buff_dis,name):
    memory_driver = ogr.GetDriverByName('ESRI Shapefile')
    outpath='C:\\Users\\thril\\Desktop\\blend\\LP_2000\\temp\\'+name
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
roadds=ogr.Open('C:\\Users\\thril\\Desktop\\blend\\LP_2000\\road.shp')
road=roadds.GetLayerByIndex(0)
if road is None:
    print('cannot open road')
    sys.exit(1)
railds=ogr.Open('C:\\Users\\thril\\Desktop\\blend\\LP_2000\\rail.shp')
rail=railds.GetLayerByIndex(0)
if rail is None:
    print('cannot open rail')
    sys.exit(1)
print('already input shp')
roadbuffer=creatbufferlyr(road,50,'roadbuffer')
railbuffer=creatbufferlyr(rail,50,'railbuffer')
print('already buffer')






