# -*- coding: cp936 -*-
#setnull
print 'ȥ��������Чֵ'

#�޸Ĳ���
###########
filepath=r"C:\tmp"    #ԭʼ����λ��
suffix='tif'    #���ݺ�׺
bvalue= -9999 #Ҫȥ���ı���ֵ

file_cutnull=r"C:\tmp\cut"  #ȥ����Чֵ����ļ���
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
    rs_cut=file_cutnull+"\\"+rsst[0:len(rsst) - len(suffix) - 1]+'_cut.tif'
    arcpy.gp.RasterCalculator_sa("SetNull('"+rsst+"'=="+str(bvalue)+",'"+rsst+"')",rs_cut)
    print rsst

print "Finish!"
