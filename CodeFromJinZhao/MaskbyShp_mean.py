# -*- coding: cp936 -*-
#ʹ��shp���������ü�դ�����ݲ�ͳ�ƾ�ֵ
print"ʹ��shp���������ü�դ�����ݲ�ͳ�ƽ����ֵ"
#�޸Ĳ���
ras_file = r"D:\CRU4.02\GeoTiff_LP\rh\Year"    #դ������λ��
suffix = 'tif'    #դ�����ݺ�׺
bvalue= -9999	#դ�����ݱ���ֵ
clpgeo = 'ClippingGeometry'

shp_file = r"G:\������ԭ�ֱ߽�\LPfat.shp"  #�ü�ģ��shp����
ras_file_cut = r"D:\tmp"  #դ�����ݲü�����洢λ��
txtname=r"D:\CRU4.02\GeoTiff_LP\cru4.02_rh_yr_LP.txt"     #���ͳ���ı�·��������
#���㲿��
import arcpy
import os
if not os.path.exists(ras_file_cut):
    os.mkdir(ras_file_cut)

arcpy.env.workspace=ras_file
ras=arcpy.ListRasters('*',suffix)
print "����"+'%d'%len(ras)+"��դ������"
#
print "Processing......"
result=[]
for rs in ras:
    outname=ras_file_cut+"\\"+str(rs[0:len(rs)-4])+".tif"    #####
    #arcpy.Clip_management(rs,"#",outname,shp_file,str(bvalue),"ClippingGeometry")   #ClippingGeometry   NONE
    arcpy.Clip_management(rs,"#",outname,shp_file,str(bvalue),clpgeo)
    stats = arcpy.GetRasterProperties_management(outname,"MEAN")
    result.append(str(stats)+"\n")
    #arcpy.Delete_management(outname,"")
    print str(rs)+"   OK!"

file(txtname,'w').writelines(result)
print "Finish!"
