# -*- coding: cp936 -*-
#դ��ת��ʽ���

#�޸Ĳ���

ras_path=r"C:\��������\�ן�\data\org"     #դ�����ݴ洢·��
in_suffix='dat'    #ԭʼ���ݺ�׺
unvalid='#'    #��Ҫ��ֵΪNoData��ֵ�����û�У�����д'#'

out_path=r"C:\��������\�ן�\data\org2"    #����洢·��
out_suffix='tif'    #������ݺ�׺
########

#���㲿��
print "դ����������ת��ʽ���"
print "����դ���׺��"+in_suffix
print "���դ���׺��"+out_suffix
print "Processing......"

import arcpy
arcpy.env.workspace=ras_path

for ras_file in arcpy.ListRasters('*',in_suffix):
    rasorig=ras_file.encode('cp936')
    out_name=out_path+"\\"+rasorig[0:len(rasorig)-len(in_suffix)]+out_suffix
    arcpy.CopyRaster_management(rasorig,out_name,"","",unvalid,"NONE","NONE","")
    print rasorig[0:len(rasorig)-3]+out_suffix+"  OK!"
print "Finish!"
