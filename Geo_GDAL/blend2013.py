import glob
import os,sys
from osgeo import ogr
from osgeo import gdal
from osgeo import osr
import numpy
files=glob.glob(r'C:\Users\thril\Desktop\1bi25\**\lrdl.shp')
ogr.RegisterAll()
driver=ogr.GetDriverByName('ESRI Shapefile')
ds1st=driver.Open(files[0]).GetLayer('lrdl')
outds=driver.CreateDataSource(r'C:\Users\thril\Desktop\merge')
print('begin creat layer')
mergelyr=outds.CreateLayer('merged',geom_type=ogr.wkbMultiLineString)
print('in loop')
for f in files:
    ds=driver.Open(f)
    dslayer=ds.GetLayer('lrdl')
    print(dslayer.GetGeomType())
    mergelyr.Union(dslayer,mergelyr)
print('ok')