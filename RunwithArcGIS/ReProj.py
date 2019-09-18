# -*- coding: cp936 -*-
#栅格转投影，使用参考影像定义目标投影（WGS84）

#修改部分

ras_path=r"F:\LAI\MODIS_LAI\month"     #栅格数据存储路径
suffix='tif'    #数据后缀

sample=r'E:\1111\ET\LP_GLASS_LAI\82_15_LAI\GLASS_AVHRR_LAI_1982_CUT.tif'   #重投影及捕捉栅格参考影像
rsize='1000' #转投影重采样精度，根据目标投影单位设置

out_path=r"F:\LAI\MODIS_LAI\month_prj"    #结果存储路径

########

#计算部分
print "栅格数据批量转投影重采样"

import arcpy
import arcpy.sa
arcpy.env.workspace=ras_path
arcpy.env.snapRaster = sample

for ras_file in arcpy.ListRasters('*',suffix):
    out_name=out_path+"\\"+ras_file.encode('cp936')
    arcpy.ProjectRaster_management(ras_file.encode('cp936'),out_name,sample,'NEAREST',rsize,'#','#','#')
    print ras_file.encode('cp936')+"  OK!"
print "Finish!"
