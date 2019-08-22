# -*- coding: cp936 -*-
#�����ز���

# �޸Ĳ���

raspath = r"G:\MODIS����\NPP��ɳ��ɳ\NPP_yr"    # ԭʼ����λ��
ras_suffix = 'tif'    # դ�����ݺ�׺
ras_vd = [0, 10000]    # դ��������Ч��Χ
ras_sf = 1 #դ������ scale factor

res_size = r'I:\VI_LPfat_GPP\VI_GPPsce02\LP_out\ETa\ETa1982.tif'   # �ز������ȣ���ֵ��λ��ԭʼ����ͶӰ��λ��������WGS-84��λΪʮ���ƶ�
res_type = 'NEAREST'
'''
    Ҫʹ�õ��ز����㷨��Ĭ������Ϊ NEAREST��

    NEAREST �����ڽ����䷨
    BILINEAR ��˫���Բ�ֵ��
    CUBIC �����ξ����ֵ��
    MAJORITY �������ز�����
'''

out_suffix = 'tif'    # �ز�����������׺
out_temp = r"G:\MODIS����\NPP��ɳ��ɳ\NPP_yr\NPP_LP_VI"  # ������ݴ洢Ŀ¼


#���㲿��
print "դ�����������ز���"

import arcpy
from arcpy.sa import *
arcpy.CheckOutExtension("Spatial")
arcpy.env.workspace=raspath
arcpy.env.mask = res_size
arcpy.env.snapRaster = res_size
arcpy.env.extent = res_size

ras_fs = arcpy.ListRasters('*', ras_suffix)
print "����" + '%d'%len(ras_fs) + "��NDVI����"
#
print "Processing......"
for rs in ras_fs:
    arcpy.gp.RasterCalculator_sa("SetNull(('"+rs+"' < "+str(ras_vd[0])+") | ('"+rs+"' > "+str(ras_vd[1])+"),'"+rs+"'*"+str(ras_sf)+")", out_temp+"\\"+rs)   #setnull

    resall_nm = out_temp + "\\" + rs[0:len(rs) - len(ras_suffix) - 1] + "_res." + out_suffix
    arcpy.Resample_management(out_temp + "\\" + rs, resall_nm, res_size, res_type)  # resample

    arcpy.Delete_management(out_temp + "\\" + rs, "")

    print rs

print "Finish!"
