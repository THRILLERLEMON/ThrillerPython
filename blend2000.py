import os,sys
import numpy
from osgeo import ogr
from osgeo import gdal
from osgeo import osr

ogr.RegisterAll()
lpareads=ogr.Open('C:\\Users\\thril\\Desktop\\blend\\LP_area\\LP_AREA.shp')
lparea=lpareads.GetLayerByIndex(0)
if lparea is None:
    print('cannot open lparea')
    sys.exit(1)
roadds=ogr.Open('C:\\Users\\thril\\Desktop\\blend\\LP_2000\\temp\\roadbuffer\\buffer.shp')
road=roadds.GetLayerByIndex(0)
if road is None:
    print('cannot open road')
    sys.exit(1)
railds=ogr.Open('C:\\Users\\thril\\Desktop\\blend\\LP_2000\\temp\\railbuffer\\buffer.shp')
rail=railds.GetLayerByIndex(0)
if rail is None:
    print('cannot open rail')
    sys.exit(1)
print('already input shp')
memorydriver = ogr.GetDriverByName('ESRI Shapefile')
memoryds = memorydriver.CreateDataSource('C:\\Users\\thril\\Desktop\\blend\\LP_2000\\temp\\layerraster')
union_lyr = memoryds.CreateLayer('union',road.GetSpatialRef())
road.Union(rail,union_lyr)

print(union_lyr.GetFeatureCount())
print('already union')
tf=gdal.Open(r'C:\Users\thril\Desktop\blend\classified2000-01-01.tif')
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
new_raster = imgdriver.Create(r'C:\Users\thril\Desktop\blend\LP_2000\new_raster.tif', tfXSize, tfYSize, 1, gdal.GDT_Byte)
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
# result=tfData
# for i in range(0,rows):
#     for j in range(0,cols):
#         if (newData[i,j]==255):
#             result[i,j] = 255
#         if (newData[i,j]==newNoData):
#             result[i,j] = tfData[i,j]
#         if (tfData[i,j]==0):
#             result[i,j] = -9999
resultPath = r'C:\Users\thril\Desktop\blend\LP_2000\result_landuse.tif'
resultds = imgdriver.Create(resultPath, cols, rows, 1, tfband.DataType)
resultds.SetGeoTransform(tfTra)
resultds.SetProjection(tfPro)
resultds.GetRasterBand(1).WriteArray(tfData)    
resultds = None
print('ok!')
