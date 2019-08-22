# -*- coding: cp936 -*-
#դ��תͶӰ��ʹ�òο�Ӱ����Ŀ��ͶӰ��WGS84��

#�޸Ĳ���

ras_path=r"E:\GLASS_LAI_AVHRR_1982to2015\GeoTiff\YR_8dy_spr_org"     #դ�����ݴ洢·��
suffix='tif'    #���ݺ�׺

sample=r'C:\tmp\ETa_82to12_mean_cut.tif'   #��ͶӰ����׽դ�񡢴���Χ�ο�Ӱ��
rsize=r'C:\tmp\ETa_82to12_mean_cut.tif' #תͶӰ�ز������ȣ�����Ŀ��ͶӰ��λ����

## H:\VI_LP_simu_infat\miclcover2000\original_class\miclcover2000reprj_LPrecls.tif

bvalue = -99
outsfx = 'tif'
out_path=r"E:\GLASS_LAI_AVHRR_1982to2015\GeoTiff\YR_8dy_VI1km"    #����洢·��

########

#���㲿��

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
print "դ����������תͶӰ�ز���"
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
