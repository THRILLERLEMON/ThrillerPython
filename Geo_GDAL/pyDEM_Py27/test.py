import numpy as np
import sys
from osgeo import ogr
from osgeo import gdal
from osgeo import osr
from pydem.dem_processing import DEMProcessor
sys.setrecursionlimit(1000000)

# Ori
tiffile = r'C:\Users\thril\Desktop\ETOPO1DEM_Bedrock_gridRegis\ETOPO1_Bed_g_geotiff.tif'
Oritif = gdal.Open(tiffile)
if Oritif is None:
    print('cannot open tif')
    sys.exit(1)
OritifPro = Oritif.GetProjection()
OritifTra = Oritif.GetGeoTransform()
tifband = Oritif.GetRasterBand(1)
tifData = tifband.ReadAsArray(0, 0, Oritif.RasterXSize, Oritif.RasterYSize)
print('over in data')

# pyDEM
dem_proc = DEMProcessor(tiffile)
dem_proc.fill_flats = False
print('begin cal TWI')
twi = dem_proc.calc_twi()
cols = np.size(twi, 0)
rows = np.size(twi, 1)
print('over pyDEM process')

# out
imgdriver = gdal.GetDriverByName('GTiff')
resultPath = 'C:\\Users\\thril\\Desktop\\ETOPO1DEM_Bedrock_gridRegis\\ETOPO1_TWI.tif'
resultds = imgdriver.Create(resultPath, cols, rows, 1, twi.DataType)
resultds.SetGeoTransform(OritifTra)
resultds.SetProjection(OritifPro)
resultds.GetRasterBand(1).WriteArray(twi)
resultds = None
print('ok!')
