# -*- coding: cp936 -*-
#MODIS hdf����ƴ�Ӳ������MODIS�ļ�����ʱ����ϢӦΪYYYYDDD����ȡĳһָ�����Σ�ƴ���ص����ּ����ֵ
#���裺
#1��python�����ļ��У���ȡ��������Ψһֵ�������б�
#2�������ļ�������ʼλ����ȡͬһ��������hdf���ݵ�ָ���������ݴ洢����ʱ��·����
#3��ƴ�Ӹո���ȡ�����ݣ������µ����ݣ�ɾ��֮ǰ��ȡ�ķֿ�����

##�޸Ĳ���#
ras_path=r'I:\MODIS_NDVI_HDF\LP_NDVI2013' #���ݴ洢�ļ���
tps=9  #�ļ�����������ʼλ�ã���0��ʼ
band=0  #��ȡ�Ĳ���������0��ʼ
efrg = [-2000,10000]  # ��Ч��ֵ��Χ
sf = 0.0001  # scale factor
valid='32_BIT_FLOAT'   #��ֵ��Χ���ο�ע��
'''
    1_BIT ��1 λ�޷���������ֵ����Ϊ 0 �� 1�� 
    2_BIT ��2 λ�޷���������֧�ֵ�ֵΪ 0 �� 3�� 
    4_BIT ��4 λ�޷���������֧�ֵ�ֵΪ 0 �� 15�� 
    8_BIT_UNSIGNED ��8 λ�޷����������͡�֧�ֵ�ֵΪ 0 �� 255�� 
    8_BIT_SIGNED ��8 λ�з����������͡�֧�ֵ�ֵΪ -128 �� 127�� 
    16_BIT_UNSIGNED ��16 λ�޷����������͡�ȡֵ��ΧΪ 0 �� 65,535�� 
    16_BIT_SIGNED ��16 λ�з����������͡�ȡֵ��ΧΪ -32,768 �� 32,767�� 
    32_BIT_UNSIGNED ��32 λ�޷����������͡�ȡֵ��ΧΪ 0 �� 4,294,967,295�� 
    32_BIT_SIGNED ��32 λ�з����������͡�ȡֵ��ΧΪ -2,147,483,648 �� 2,147,483,647��
    32_BIT_FLOAT ��֧��С���� 32 λ�������͡�
    64_BIT ��֧��С���� 64 λ�������͡�
'''
#samp = r'I:\MODIS_NDVI_HDF\prgras\MOD13A3.A2000_cut_cut.tif'  # תͶӰ�ο�����

tmp_path=r'I:\MODIS_NDVI_HDF\tmp' #��ʱ���ݴ洢�ļ���
out_path=r'I:\MODIS_NDVI_HDF\mosaic' #ƴ�ӽ������ļ���
#########

#���㲿��
print 'MODIS hdf����ƴ�Ӳ����'

import os
afs=os.listdir(ras_path)
dates=[]    #yyyyddd
hdfs=[] #hdf files
for fn in afs:
    if fn.endswith('.hdf'):
        hdfs.append(fn)
        dates.append(fn[tps:tps+7])    #
date=sorted(set(dates))
print '����'+str(len(date))+'������'

import arcpy
import warnings
warnings.filterwarnings("ignore")
from arcpy.sa import *
arcpy.CheckOutExtension("Spatial")
arcpy.env.workspace=ras_path
#arcpy.env.snapRaster = samp

for yd in date:
    extrac_tif_name=[]
    extrac_tif=''
    for hdf_f in hdfs:
        if hdf_f.startswith(hdf_f[0:tps]+yd):
            orgras=tmp_path+'\\'+hdf_f[0:len(hdf_f)-3]+"tif"
            arcpy.ExtractSubDataset_management(hdf_f,orgras,str(band))
            stnras = tmp_path+'\\'+hdf_f[0:len(hdf_f)-4]+"_stn.tif"
            arcpy.gp.RasterCalculator_sa("SetNull(('"+orgras+"' < "+str(efrg[0])+") | ('"+orgras+"' > "+str(efrg[1])+"),'"+orgras+"'*"+str(sf)+")", stnras)  # setnull
            arcpy.Delete_management(orgras)

            extrac_tif=extrac_tif+';'+stnras
            extrac_tif_name.append(stnras)
    extrac_tif=extrac_tif[1:len(extrac_tif)]
    rasmosiac=hdfs[0][0:tps]+yd+".tif"
    arcpy.MosaicToNewRaster_management(extrac_tif,out_path,rasmosiac,"#",valid,"#","1","LAST","FIRST")
    for exfn in extrac_tif_name:
        arcpy.Delete_management(exfn)

    # rasprj = out_path+'\\'+rasmosiac
    # arcpy.ProjectRaster_management(rasmosiac,rasprj,samp,'NEAREST',samp,'#','#','#')
    # arcpy.Delete_management(rasmosiac)
    print rasmosiac
	
print '���'
