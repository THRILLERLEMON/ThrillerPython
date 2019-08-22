# -*- coding: cp936 -*-

print"դ������ͳ��"

###########�޸Ĳ���###########

ras_file = r"D:\Franz\ETinversGPP\ET_PRP_gaps\PRP_GIDS\MnEle65Neg30stSmth2_crct_VerticalZonal_82to12Yr"   #ԭʼդ�����ݴ洢�ļ���·��
suffix = 'tif'  #ԭʼդ�����ݺ�׺
valid=[0,65500] #��Чֵ��Χ
sfactor=1 #scale factor
tmpdoc = r'D:\Franz\ETinversGPP\ET_PRP_gaps\PRP_GIDS\tmp'  # ��ʱ���ݴ洢��Ŀ¼

sample=r''   #��ͶӰ����׽դ�񡢴���Χ�ο�Ӱ��
stats_fun='MEAN'	#ͳ�Ʒ������ο����£�

'''
MINIMUM ����������դ���е�������Ԫ����Сֵ�� 
MAXIMUM ����������դ���е�������Ԫ�����ֵ�� 
MEAN ����������դ���е�������Ԫ��ƽ��ֵ�� 
STD ����������դ���е�������Ԫ�ı�׼� 
UNIQUEVALUECOUNT ����������դ���е�Ψһֵ����Ŀ�� 
TOP �����ط�Χ�Ķ���ֵ�� YMax ֵ�� 
LEFT �����ط�Χ�����ֵ�� XMin ֵ�� 
RIGHT �����ط�Χ���Ҳ�ֵ�� XMax ֵ�� 
BOTTOM �����ط�Χ�ĵײ�ֵ�� YMin ֵ�� 
CELLSIZEX ������ x �����ϵ���Ԫ��С�� 
CELLSIZEY ������ y �����ϵ���Ԫ��С�� 
VALUETYPE ����������դ������Ԫֵ������'''

txtname=r"D:\Franz\ETinversGPP\ET_PRP_gaps\PRP_GIDS\tmp\Pcrct_his_mean.txt"     #���ͳ���ı�

#############################


#���㲿��
import arcpy
import warnings
warnings.filterwarnings("ignore")
from arcpy.sa import *
arcpy.CheckOutExtension("Spatial")
arcpy.env.workspace=ras_file
arcpy.env.extent = sample
arcpy.env.mask = sample

ras=arcpy.ListRasters('*',suffix)
print "����"+str(len(ras))+"��դ������"
print "Processing......"
result=[]
for rs in ras:
	rstmp=rs.encode('cp936')
	rs_cut=tmpdoc+"\\"+rstmp[0:len(rstmp) - len(suffix) - 1]+'_cut.tif'
	#arcpy.gp.RasterCalculator_sa("SetNull('"+rstmp+"'=="+str(bvalue)+",'"+rstmp+"')",rs_cut)
	arcpy.gp.RasterCalculator_sa("SetNull(('"+rstmp+"'<"+str(valid[0])+")|('"+rstmp+"'>"+str(valid[1])+"),'"+rstmp+"'*"+str(sfactor)+")",rs_cut)
	stats=arcpy.GetRasterProperties_management(rs_cut,stats_fun)
	arcpy.Delete_management(rs_cut,"")
	result.append(rstmp+'   '+str(stats)+"\n")
	print rstmp+"   OK!"

file(txtname,'w').writelines(result)
print "Finish!"
