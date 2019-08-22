# -*- coding: cp936 -*-
#mask裁剪
print "使用mask裁剪"
#修改部分
ras_path=r"E:\VI_LPfat_GPP\VI_Cap01\LP_out\ETa\ALL\82to12"	#栅格数据文件夹
suffix="tif"	#栅格数据后缀

mask=r"E:\SWATdata\HRU\LPmsk\VI_LP_msk.tif"	#mask数据

out_path=r"E:\SWATdata\HRU\VI_Crp01_ETa"       #提取结果文件夹

#计算部分
print "Processing......"

import arcpy
from arcpy.sa import *
arcpy.CheckOutExtension("Spatial")
arcpy.env.workspace=ras_path
arcpy.env.snapRaster = mask
# arcpy.env.extent = mask

rasters=arcpy.ListRasters('*',suffix)
print "共有"+'%d'%len(rasters)+"个栅格数据"

for rs in rasters:
        ras=rs.encode('cp936')
        outname=out_path+"\\"+ras[0:len(ras)-4]+".tif"
        ras_cut=ExtractByMask(ras,mask)
        ras_cut.save(outname)
        print ras
print "OK!"
