# -*- coding: cp936 -*-
# mask裁剪
print "使用mask裁剪"
# 修改部分
ras_path=r"H:\VI_LP_simu_infat\Budyko校正\ETa_ave"	#栅格数据目录
suffix="tif"	#栅格数据后缀

mask_pt=r"H:\VI_LP_simu_infat\Budyko校正\smbaisn_tif"	#栅格mask数据目录
mask_suffix='tif'  # mask数据后缀

out_path=r"H:\VI_LP_simu_infat\Budyko校正\smbs02"       #提取结果文件夹

#计算部分
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


print "共有"+'%d'%len(ras)+"个栅格数据"

for rs in ras:
        rstnm=rs.encode('cp936')
        print "共有"+str(len(ras))+"个raster数据，正在处理第"+str(ras.index(rs)+1)+"个："+rstnm
        for msk in msksras:
                msknm=msk.encode('cp936')
                mskfile=mask_pt+"\\"+msknm
                outname=out_path+"\\"+rstnm[0:len(rstnm)-4]+msknm[0:len(msknm)-4]+".tif"

                ras_cut=ExtractByMask(rstnm,mskfile)
                ras_cut.save(outname)
                # arcpy.Delete_management(outname,"")
                print msknm+" OK!"

print "Finish!"
