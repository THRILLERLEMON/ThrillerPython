# -*- coding: cp936 -*-
#setnull
print '去除无效值'

#修改部分
###########
filepath=r"E:\SWATdata\HRU\Stats_ras\VI01l1"    #原始数据位置
file_cutnull=r"E:\SWATdata\HRU\Stats_ras\VI01l1_cut"  #去除无效值结果文件夹
suffix='tif'    #数据后缀
valid=[0,100] #有效值范围
sfactor=0.08333333 #scale factor
adofst = 0


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
    rs_cut=file_cutnull+"\\"+rsst
    arcpy.gp.RasterCalculator_sa("SetNull(('"+rsst+"'<"+str(valid[0])+")|('"+rsst+"'>"+str(valid[1])+"),'"+rsst+"'*"+str(sfactor)+'+'+str(adofst)+")",rs_cut)
    print rsst

print "Finish!"
