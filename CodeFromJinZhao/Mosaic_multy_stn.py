# -*- coding: cp936 -*-
#MODIS hdf数据拼接并输出，MODIS文件名中时间信息应为YYYYDDD，提取某一指定波段，拼接重叠部分计算均值
#步骤：
#1、python遍历文件夹，提取日期数据唯一值，生成列表
#2、根据文件日期起始位置提取同一日期所有hdf数据的指定波段数据存储到临时的路径中
#3、拼接刚刚提取的数据，生成新的数据，删除之前提取的分块数据

##修改部分#
ras_path=r'I:\MODIS_NDVI_HDF\LP_NDVI2013' #数据存储文件夹
tps=9  #文件名中日期起始位置，从0开始
band=0  #提取的波段数，从0开始
efrg = [-2000,10000]  # 有效数值范围
sf = 0.0001  # scale factor
valid='32_BIT_FLOAT'   #数值范围，参考注释
'''
    1_BIT —1 位无符号整数。值可以为 0 或 1。 
    2_BIT —2 位无符号整数。支持的值为 0 到 3。 
    4_BIT —4 位无符号整数。支持的值为 0 到 15。 
    8_BIT_UNSIGNED —8 位无符号数据类型。支持的值为 0 到 255。 
    8_BIT_SIGNED —8 位有符号数据类型。支持的值为 -128 到 127。 
    16_BIT_UNSIGNED —16 位无符号数据类型。取值范围为 0 到 65,535。 
    16_BIT_SIGNED —16 位有符号数据类型。取值范围为 -32,768 到 32,767。 
    32_BIT_UNSIGNED —32 位无符号数据类型。取值范围为 0 到 4,294,967,295。 
    32_BIT_SIGNED —32 位有符号数据类型。取值范围为 -2,147,483,648 到 2,147,483,647。
    32_BIT_FLOAT —支持小数的 32 位数据类型。
    64_BIT —支持小数的 64 位数据类型。
'''
#samp = r'I:\MODIS_NDVI_HDF\prgras\MOD13A3.A2000_cut_cut.tif'  # 转投影参考数据

tmp_path=r'I:\MODIS_NDVI_HDF\tmp' #临时数据存储文件夹
out_path=r'I:\MODIS_NDVI_HDF\mosaic' #拼接结果输出文件夹
#########

#计算部分
print 'MODIS hdf数据拼接并输出'

import os
afs=os.listdir(ras_path)
dates=[]    #yyyyddd
hdfs=[] #hdf files
for fn in afs:
    if fn.endswith('.hdf'):
        hdfs.append(fn)
        dates.append(fn[tps:tps+7])    #
date=sorted(set(dates))
print '共有'+str(len(date))+'个日期'

import arcpy
import warnings
warnings.filterwarnings("ignore")
from arcpy.sa import *
arcpy.CheckOutExtension("Spatial")
arcpy.env.workspace=ras_path
#arcpy.env.snapRaster = samp

for yd in date:
    extrac_tif_name=[]
    extrac_tif=''
    for hdf_f in hdfs:
        if hdf_f.startswith(hdf_f[0:tps]+yd):
            orgras=tmp_path+'\\'+hdf_f[0:len(hdf_f)-3]+"tif"
            arcpy.ExtractSubDataset_management(hdf_f,orgras,str(band))
            stnras = tmp_path+'\\'+hdf_f[0:len(hdf_f)-4]+"_stn.tif"
            arcpy.gp.RasterCalculator_sa("SetNull(('"+orgras+"' < "+str(efrg[0])+") | ('"+orgras+"' > "+str(efrg[1])+"),'"+orgras+"'*"+str(sf)+")", stnras)  # setnull
            arcpy.Delete_management(orgras)

            extrac_tif=extrac_tif+';'+stnras
            extrac_tif_name.append(stnras)
    extrac_tif=extrac_tif[1:len(extrac_tif)]
    rasmosiac=hdfs[0][0:tps]+yd+".tif"
    arcpy.MosaicToNewRaster_management(extrac_tif,out_path,rasmosiac,"#",valid,"#","1","LAST","FIRST")
    for exfn in extrac_tif_name:
        arcpy.Delete_management(exfn)

    # rasprj = out_path+'\\'+rasmosiac
    # arcpy.ProjectRaster_management(rasmosiac,rasprj,samp,'NEAREST',samp,'#','#','#')
    # arcpy.Delete_management(rasmosiac)
    print rasmosiac
	
print '完成'
