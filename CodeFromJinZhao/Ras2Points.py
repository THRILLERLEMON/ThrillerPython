# -*- coding: cp936 -*-

print "դ��ת��"

###########�޸Ĳ���###########

ras_file = r"D:\ISI-MIP_GPP_Pre_SWrad\GPP_GCMs_ALL\visit"   #ԭʼդ�����ݴ洢�ļ���·��
suffix = 'tif'  #ԭʼդ�����ݺ�׺
valid=[0,65500] #��Чֵ��Χ
sfactor=1 #scale factor
MaskPLG = r'D:\������ԭ�ֱ߽�\LPfat.shp'

PTdoc = r'D:\ISI-MIP_GPP_Pre_SWrad\GPP_GCMs_ALL\visit_pt'  # �����ݴ洢·��

##############################
import arcpy
import warnings
warnings.filterwarnings("ignore")
from arcpy.sa import *
arcpy.CheckOutExtension("Spatial")
arcpy.env.workspace=ras_file
arcpy.env.mask = MaskPLG

ras=arcpy.ListRasters('*',suffix)
print "����"+str(len(ras))+"��դ������"
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
	
	
	

