import os,sys
import numpy
from osgeo import ogr
from osgeo import gdal
from osgeo import osr
ogr.RegisterAll()
lpareads=ogr.Open('C:\\Users\\thril\\Desktop\\blend\\LP_area\\LP_AREA.shp')
lparea=lpareads.GetLayerByIndex(0)
print(lparea.GetFeatureCount())
gdal.Warp('C:\\Users\\thril\\Desktop\\blend\\LP_2000\\result_landuse_clip.tif','C:\\Users\\thril\\Desktop\\blend\\LP_2000\\result_landuse.tif',cutlineLayer  = lparea,srcNodata=0, dstNodata=0,cropToCutline=True,dstSRS="WGS84")
print('ok')