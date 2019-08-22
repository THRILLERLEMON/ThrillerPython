# -*- coding: cp936 -*-
#批量将ASCII数据转为栅格并定义投影
print "批量将ASCII数据转为栅格并定义投影"

#修改部分
asc_path=r"E:\VI_LPfat_GPP\VI_Cap01\LP_out\Ta\ASC"  #ASCII文本数据存储文件夹
suffix='*.asc'    #数据后缀
proj_file=r'E:\LP_landcover\IGBP\VIreal.prj'  #*.prj投影文件
ras_path=r"E:\VI_LPfat_GPP\VI_Cap01\LP_out\Ta\GEOTIFF"   #ASCII转栅格结果存储文件夹


#计算部分
import arcpy
import arcpy.sa
arcpy.env.workspace=asc_path
ascfs=arcpy.ListFiles(suffix)
print "共有"+str(len(ascfs))+"个ASCII数据"
print "Processing......"

for as_f in ascfs:
	as_file=str(as_f)
	rasname=ras_path+"\\"+as_file[0:len(as_file)-3]+"tif"
	arcpy.ASCIIToRaster_conversion(asc_path+'\\'+as_file,rasname,"FLOAT") #ASCII to raster
	arcpy.DefineProjection_management(rasname,proj_file)   #define Projection
	print as_file

print "Finsh!"
