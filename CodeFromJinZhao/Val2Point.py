# -*- coding: cp936 -*-
print"��ȡ������λ��դ����������"

#####	�޸�	#####
ptshp = r'I:\�й��߽�\china\china.shp'  # λ�õ�����

ras_pt = r'I:\GIMMS_NDVI\mvc_NDVI_wdh_MEAN'  # դ������Ŀ¼
suffix = 'img'  # դ�����ݺ�׺

#####################

import arcpy
from arcpy.sa import *
arcpy.CheckOutExtension("Spatial")
arcpy.env.workspace=ras_pt
ras=arcpy.ListRasters('*', suffix)
print "����"+str(len(ras))+"��դ������"
print "Processing......"

extrac_tif=''
for rsnm in ras:
	rs = rsnm.encode('cp936')
	extrac_tif=extrac_tif+';'+rs
	print rs
	
extrac_tif=extrac_tif[1:len(extrac_tif)]

print "Extrating..."
ExtractMultiValuesToPoints(ptshp, extrac_tif, "NONE")
	
print "Finish!"
