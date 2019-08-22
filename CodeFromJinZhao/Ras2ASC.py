# -*- coding: cp936 -*-
#������ASCII����תΪդ�񲢶���ͶӰ
print "������Raster����תΪASC"

#�޸Ĳ���
ras_path = r"D:\ld_loess_liang\GeoTiff_1km"  #ASCII�ı����ݴ洢�ļ���
suffix = 'tif'    #���ݺ�׺
asc_path = r"D:\ld_loess_liang\GeoTiff_1km_asc"   #ASCIIתդ�����洢�ļ���


#���㲿��
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
