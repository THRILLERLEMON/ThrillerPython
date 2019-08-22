# -*- coding: cp936 -*-
#批量将ASCII数据转为栅格并定义投影
print "批量将Raster数据转为ASC"

#修改部分
ras_path = r"D:\ld_loess_liang\GeoTiff_1km"  #ASCII文本数据存储文件夹
suffix = 'tif'    #数据后缀
asc_path = r"D:\ld_loess_liang\GeoTiff_1km_asc"   #ASCII转栅格结果存储文件夹


#计算部分
import arcpy
import arcpy.sa
arcpy.env.workspace = ras_path
print "Processing......"

for rasfs in arcpy.ListRasters('*', suffix):
	rasfile = rasfs.encode('cp936')
	ascnm = asc_path + "\\" + rasfile[0:len(rasfile) - len(suffix)] + "asc"
	arcpy.RasterToASCII_conversion(rasfile, ascnm)
	
	print rasfile

print "Finsh!"
