# -*- coding: cp936 -*-
# mask�ü�
print "ʹ��mask�ü�"
# �޸Ĳ���
ras_path=r"H:\VI_LP_simu_infat\BudykoУ��\ETa_ave"	#դ������Ŀ¼
suffix="tif"	#դ�����ݺ�׺

mask_pt=r"H:\VI_LP_simu_infat\BudykoУ��\smbaisn_tif"	#դ��mask����Ŀ¼
mask_suffix='tif'  # mask���ݺ�׺

out_path=r"H:\VI_LP_simu_infat\BudykoУ��\smbs02"       #��ȡ����ļ���

#���㲿��
print "Processing......"

import arcpy
from arcpy.sa import *
arcpy.CheckOutExtension("Spatial")

arcpy.env.workspace=mask_pt
msksras=arcpy.ListRasters('*',mask_suffix)

arcpy.env.workspace=ras_path
ras=arcpy.ListRasters('*',suffix)

arcpy.env.snapRaster = ras[0].encode('cp936')
arcpy.env.extent = ras[0].encode('cp936')


print "����"+'%d'%len(ras)+"��դ������"

for rs in ras:
        rstnm=rs.encode('cp936')
        print "����"+str(len(ras))+"��raster���ݣ����ڴ����"+str(ras.index(rs)+1)+"����"+rstnm
        for msk in msksras:
                msknm=msk.encode('cp936')
                mskfile=mask_pt+"\\"+msknm
                outname=out_path+"\\"+rstnm[0:len(rstnm)-4]+msknm[0:len(msknm)-4]+".tif"

                ras_cut=ExtractByMask(rstnm,mskfile)
                ras_cut.save(outname)
                # arcpy.Delete_management(outname,"")
                print msknm+" OK!"

print "Finish!"
