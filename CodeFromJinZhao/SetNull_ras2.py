# -*- coding: cp936 -*-
#setnull
print 'ȥ����Чֵ'

#�޸Ĳ���
###########
filepath=r"E:\SWATdata\HRU\Stats_ras\VI01l1"    #ԭʼ����λ��
file_cutnull=r"E:\SWATdata\HRU\Stats_ras\VI01l1_cut"  #ȥ����Чֵ����ļ���
suffix='tif'    #���ݺ�׺
valid=[0,100] #��Чֵ��Χ
sfactor=0.08333333 #scale factor
adofst = 0


###########

#���㲿��
import arcpy
import warnings
warnings.filterwarnings("ignore")
from arcpy.sa import *
arcpy.CheckOutExtension("Spatial")
arcpy.env.workspace=filepath
rasters=arcpy.ListRasters('*',suffix)
print "����"+'%d'%len(rasters)+"��դ������"

print "Processing......"
for rs in rasters:
    rsst=rs.encode('cp936')
    rs_cut=file_cutnull+"\\"+rsst
    arcpy.gp.RasterCalculator_sa("SetNull(('"+rsst+"'<"+str(valid[0])+")|('"+rsst+"'>"+str(valid[1])+"),'"+rsst+"'*"+str(sfactor)+'+'+str(adofst)+")",rs_cut)
    print rsst

print "Finish!"
