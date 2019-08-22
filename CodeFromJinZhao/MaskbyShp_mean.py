# -*- coding: cp936 -*-
#使用shp数据批量裁剪栅格数据并统计均值
print"使用shp数据批量裁剪栅格数据并统计结果均值"
#修改部分
ras_file = r"D:\CRU4.02\GeoTiff_LP\rh\Year"    #栅格数据位置
suffix = 'tif'    #栅格数据后缀
bvalue= -9999	#栅格数据背景值
clpgeo = 'ClippingGeometry'

shp_file = r"G:\黄土高原胖边界\LPfat.shp"  #裁剪模板shp数据
ras_file_cut = r"D:\tmp"  #栅格数据裁剪结果存储位置
txtname=r"D:\CRU4.02\GeoTiff_LP\cru4.02_rh_yr_LP.txt"     #输出统计文本路径及名称
#计算部分
import arcpy
import os
if not os.path.exists(ras_file_cut):
    os.mkdir(ras_file_cut)

arcpy.env.workspace=ras_file
ras=arcpy.ListRasters('*',suffix)
print "共有"+'%d'%len(ras)+"个栅格数据"
#
print "Processing......"
result=[]
for rs in ras:
    outname=ras_file_cut+"\\"+str(rs[0:len(rs)-4])+".tif"    #####
    #arcpy.Clip_management(rs,"#",outname,shp_file,str(bvalue),"ClippingGeometry")   #ClippingGeometry   NONE
    arcpy.Clip_management(rs,"#",outname,shp_file,str(bvalue),clpgeo)
    stats = arcpy.GetRasterProperties_management(outname,"MEAN")
    result.append(str(stats)+"\n")
    #arcpy.Delete_management(outname,"")
    print str(rs)+"   OK!"

file(txtname,'w').writelines(result)
print "Finish!"
