# -*- coding: cp936 -*-
#栅格转投影，使用参考影像定义目标投影（WGS84）

#修改部分

ras_path=r"E:\GLASS_LAI_AVHRR_1982to2015\GeoTiff\YR_8dy_spr_org"     #栅格数据存储路径
suffix='tif'    #数据后缀

sample=r'C:\tmp\ETa_82to12_mean_cut.tif'   #重投影、捕捉栅格、处理范围参考影像
rsize=r'C:\tmp\ETa_82to12_mean_cut.tif' #转投影重采样精度，根据目标投影单位设置

## H:\VI_LP_simu_infat\miclcover2000\original_class\miclcover2000reprj_LPrecls.tif

bvalue = -99
outsfx = 'tif'
out_path=r"E:\GLASS_LAI_AVHRR_1982to2015\GeoTiff\YR_8dy_VI1km"    #结果存储路径

########

#计算部分

import arcpy,os,warnings
warnings.filterwarnings("ignore")
from arcpy.sa import *
if not(os.path.exists(out_path)):
        os.makedirs(out_path)
else:
        print 'The out_path has already exists!'

arcpy.CheckOutExtension("Spatial")

arcpy.env.workspace=ras_path
arcpy.env.snapRaster = sample
print "栅格数据批量转投影重采样"
##
# arcpy.env.extent = sample
# arcpy.env.mask = sample

for ras_file in arcpy.ListRasters('*',suffix):
        rasfl = ras_file.encode('cp936')

        rs_cut = out_path+"\\"+rasfl[0:len(rasfl)-len(outsfx)-1]+'_cut.'+outsfx
        arcpy.gp.RasterCalculator_sa("SetNull('"+rasfl+"'=="+str(bvalue)+",'"+rasfl+"')",rs_cut)
        
        out_name=out_path+"\\"+rasfl[0:len(rasfl)-len(outsfx)]+outsfx
        arcpy.ProjectRaster_management(rs_cut,out_name,sample,'NEAREST',rsize,'#','#','#')
        #arcpy.ProjectRaster_management(rs_cut,out_name,sample,'NEAREST',rsize,'Beijing_1954_To_WGS_1984_3','#','#')
        #arcpy.ProjectRaster_management(rs_cut,out_name,sample)
        
        arcpy.Delete_management(rs_cut,"")
        print ras_file.encode('cp936')+"  OK!"
print "Finish!"
