# -*- coding: cp936 -*-
print"提取点数据位置栅格数据至点"

#####	修改	#####
ptshp = r'I:\中国边界\china\china.shp'  # 位置点数据

ras_pt = r'I:\GIMMS_NDVI\mvc_NDVI_wdh_MEAN'  # 栅格数据目录
suffix = 'img'  # 栅格数据后缀

#####################

import arcpy
from arcpy.sa import *
arcpy.CheckOutExtension("Spatial")
arcpy.env.workspace=ras_pt
ras=arcpy.ListRasters('*', suffix)
print "共有"+str(len(ras))+"个栅格数据"
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
