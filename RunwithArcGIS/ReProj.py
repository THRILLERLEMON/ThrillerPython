# -*- coding: cp936 -*-
#դ��תͶӰ��ʹ�òο�Ӱ����Ŀ��ͶӰ��WGS84��

#�޸Ĳ���

ras_path=r"F:\LAI\MODIS_LAI\month"     #դ�����ݴ洢·��
suffix='tif'    #���ݺ�׺

sample=r'E:\1111\ET\LP_GLASS_LAI\82_15_LAI\GLASS_AVHRR_LAI_1982_CUT.tif'   #��ͶӰ����׽դ��ο�Ӱ��
rsize='1000' #תͶӰ�ز������ȣ�����Ŀ��ͶӰ��λ����

out_path=r"F:\LAI\MODIS_LAI\month_prj"    #����洢·��

########

#���㲿��
print "դ����������תͶӰ�ز���"

import arcpy
import arcpy.sa
arcpy.env.workspace=ras_path
arcpy.env.snapRaster = sample

for ras_file in arcpy.ListRasters('*',suffix):
    out_name=out_path+"\\"+ras_file.encode('cp936')
    arcpy.ProjectRaster_management(ras_file.encode('cp936'),out_name,sample,'NEAREST',rsize,'#','#','#')
    print ras_file.encode('cp936')+"  OK!"
print "Finish!"
