# -*- coding: cp936 -*-
#������ASCII����תΪդ�񲢶���ͶӰ
print "������ASCII����תΪդ�񲢶���ͶӰ"

#�޸Ĳ���
asc_path=r"E:\VI_LPfat_GPP\VI_Cap01\LP_out\Ta\ASC"  #ASCII�ı����ݴ洢�ļ���
suffix='*.asc'    #���ݺ�׺
proj_file=r'E:\LP_landcover\IGBP\VIreal.prj'  #*.prjͶӰ�ļ�
ras_path=r"E:\VI_LPfat_GPP\VI_Cap01\LP_out\Ta\GEOTIFF"   #ASCIIתդ�����洢�ļ���


#���㲿��
import arcpy
import arcpy.sa
arcpy.env.workspace=asc_path
ascfs=arcpy.ListFiles(suffix)
print "����"+str(len(ascfs))+"��ASCII����"
print "Processing......"

for as_f in ascfs:
	as_file=str(as_f)
	rasname=ras_path+"\\"+as_file[0:len(as_file)-3]+"tif"
	arcpy.ASCIIToRaster_conversion(asc_path+'\\'+as_file,rasname,"FLOAT") #ASCII to raster
	arcpy.DefineProjection_management(rasname,proj_file)   #define Projection
	print as_file

print "Finsh!"
