# -*- coding: cp936 -*-
#mask�ü�
print "ʹ��mask�ü�"
#�޸Ĳ���
ras_path=r"E:\VI_LPfat_GPP\VI_Cap01\LP_out\ETa\ALL\82to12"	#դ�������ļ���
suffix="tif"	#դ�����ݺ�׺

mask=r"E:\SWATdata\HRU\LPmsk\VI_LP_msk.tif"	#mask����

out_path=r"E:\SWATdata\HRU\VI_Crp01_ETa"       #��ȡ����ļ���

#���㲿��
print "Processing......"

import arcpy
from arcpy.sa import *
arcpy.CheckOutExtension("Spatial")
arcpy.env.workspace=ras_path
arcpy.env.snapRaster = mask
# arcpy.env.extent = mask

rasters=arcpy.ListRasters('*',suffix)
print "����"+'%d'%len(rasters)+"��դ������"

for rs in rasters:
        ras=rs.encode('cp936')
        outname=out_path+"\\"+ras[0:len(ras)-4]+".tif"
        ras_cut=ExtractByMask(ras,mask)
        ras_cut.save(outname)
        print ras
print "OK!"
