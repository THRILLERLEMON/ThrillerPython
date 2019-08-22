# -*- coding: cp936 -*-

print "栅格转点"

###########修改部分###########

ras_file = r"D:\ISI-MIP_GPP_Pre_SWrad\GPP_GCMs_ALL\visit"   #原始栅格数据存储文件夹路径
suffix = 'tif'  #原始栅格数据后缀
valid=[0,65500] #有效值范围
sfactor=1 #scale factor
MaskPLG = r'D:\黄土高原胖边界\LPfat.shp'

PTdoc = r'D:\ISI-MIP_GPP_Pre_SWrad\GPP_GCMs_ALL\visit_pt'  # 点数据存储路径

##############################
import arcpy
import warnings
warnings.filterwarnings("ignore")
from arcpy.sa import *
arcpy.CheckOutExtension("Spatial")
arcpy.env.workspace=ras_file
arcpy.env.mask = MaskPLG

ras=arcpy.ListRasters('*',suffix)
print "共有"+str(len(ras))+"个栅格数据"
print "Processing......"

for rs in ras:
	rstmp=rs.encode('cp936')
	rs_cut=PTdoc+"\\"+rstmp[0:len(rstmp)-len(suffix)-1]+'_cut.tif'
	outpt=PTdoc+"\\"+rstmp[0:len(rstmp)-len(suffix)-1]+'.shp'
	arcpy.gp.RasterCalculator_sa("SetNull(('"+rstmp+"'<"+str(valid[0])+")|('"+rstmp+"'>"+str(valid[1])+"),'"+rstmp+"'*"+str(sfactor)+")",rs_cut)
	arcpy.RasterToPoint_conversion(rs_cut, outpt, 'VALUE')
	arcpy.Delete_management(rs_cut,"")
	print rstmp+"   OK!"

print "Finish!"
	
	
	

