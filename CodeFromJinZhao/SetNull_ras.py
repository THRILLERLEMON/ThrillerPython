# -*- coding: cp936 -*-
#setnull
print '去除单个无效值'

#修改部分
###########
filepath=r"C:\tmp"    #原始数据位置
suffix='tif'    #数据后缀
bvalue= -9999 #要去除的背景值

file_cutnull=r"C:\tmp\cut"  #去除无效值结果文件夹
###########

#计算部分
import arcpy
import warnings
warnings.filterwarnings("ignore")
from arcpy.sa import *
arcpy.CheckOutExtension("Spatial")
arcpy.env.workspace=filepath
rasters=arcpy.ListRasters('*',suffix)

print "共有"+'%d'%len(rasters)+"个栅格数据"

print "Processing......"
for rs in rasters:
    rsst=rs.encode('cp936')
    rs_cut=file_cutnull+"\\"+rsst[0:len(rsst) - len(suffix) - 1]+'_cut.tif'
    arcpy.gp.RasterCalculator_sa("SetNull('"+rsst+"'=="+str(bvalue)+",'"+rsst+"')",rs_cut)
    print rsst

print "Finish!"
