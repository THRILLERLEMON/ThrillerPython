# -*- coding: cp936 -*-
#批量重采样

# 修改部分

raspath = r"G:\MODIS数据\NPP多沙粗沙\NPP_yr"    # 原始数据位置
ras_suffix = 'tif'    # 栅格数据后缀
ras_vd = [0, 10000]    # 栅格数据有效范围
ras_sf = 1 #栅格数据 scale factor

res_size = r'I:\VI_LPfat_GPP\VI_GPPsce02\LP_out\ETa\ETa1982.tif'   # 重采样精度，数值单位由原始数据投影单位决定，如WGS-84单位为十进制度
res_type = 'NEAREST'
'''
    要使用的重采样算法。默认设置为 NEAREST。

    NEAREST —最邻近分配法
    BILINEAR —双线性插值法
    CUBIC —三次卷积插值法
    MAJORITY —多数重采样法
'''

out_suffix = 'tif'    # 重采样结果输出后缀
out_temp = r"G:\MODIS数据\NPP多沙粗沙\NPP_yr\NPP_LP_VI"  # 结果数据存储目录


#计算部分
print "栅格数据批量重采样"

import arcpy
from arcpy.sa import *
arcpy.CheckOutExtension("Spatial")
arcpy.env.workspace=raspath
arcpy.env.mask = res_size
arcpy.env.snapRaster = res_size
arcpy.env.extent = res_size

ras_fs = arcpy.ListRasters('*', ras_suffix)
print "共有" + '%d'%len(ras_fs) + "个NDVI数据"
#
print "Processing......"
for rs in ras_fs:
    arcpy.gp.RasterCalculator_sa("SetNull(('"+rs+"' < "+str(ras_vd[0])+") | ('"+rs+"' > "+str(ras_vd[1])+"),'"+rs+"'*"+str(ras_sf)+")", out_temp+"\\"+rs)   #setnull

    resall_nm = out_temp + "\\" + rs[0:len(rs) - len(ras_suffix) - 1] + "_res." + out_suffix
    arcpy.Resample_management(out_temp + "\\" + rs, resall_nm, res_size, res_type)  # resample

    arcpy.Delete_management(out_temp + "\\" + rs, "")

    print rs

print "Finish!"
