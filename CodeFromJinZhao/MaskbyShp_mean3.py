# -*- coding: cp936 -*-

#scrip
#使用shp数据批量裁剪栅格数据并统计均值
print"使用shp数据批量裁剪栅格数据并统计结果均值"

###########修改部分###########

ras_file = r"D:\Franz\ETinversGPP\ETinvsGPP\VI_LfPLuc_GPPinvrs_his\82to12_crop_PdemVZ\GPPrl2cp\yave"   #待裁剪的原始栅格数据存储文件夹路径
suffix = 'tif'  #待裁剪的原始栅格数据后缀
bvalue=-99   #待裁剪的原始栅格数据背景值

shp_file = r"D:\Franz2\45个小流域边界及水文站点\45个小流域直接裁剪"   #裁剪所需shp模板数据存储文件夹路径

ras_file_cut = r"C:\CutTmp"   #裁剪后栅格数据结果存储文件夹路径
txtname=r"D:\Franz\ETinversGPP\ETinvsGPP\VI_LfPLuc_GPPinvrs_his\82to12_crop_PdemVZ\GPPrl2cp\yave_sts"     #输出统计文本路径

#############################

#计算部分
import arcpy
arcpy.env.workspace=shp_file
shps=arcpy.ListFeatureClasses()
arcpy.env.workspace=ras_file
ras=arcpy.ListRasters('*',suffix)
print "共有"+str(len(shps))+"个shp数据"
#
print "Processing......"

for rs in ras:
	rstmp=rs.encode('cp936')
	print "共有"+str(len(ras))+"个raster数据，正在处理第"+str(ras.index(rs)+1)+"个："+rstmp
	result=[]
	for sh in shps:
		shtmp=sh.encode('cp936')
		shpfile=shp_file+"\\"+shtmp
		outname=ras_file_cut+"\\"+rstmp[0:len(rstmp)-4]+shtmp[0:len(shtmp)-4]+".tif"
		#arcpy.Clip_management(rstmp,"#",outname,shpfile,"#","ClippingGeometry")
		arcpy.Clip_management(rstmp,"#",outname,shpfile,str(bvalue),"ClippingGeometry") #忽略无效值
		try:
			stats=arcpy.GetRasterProperties_management(outname,"MEAN")
			result.append(shtmp+'   '+str(stats)+"\n")
		except:
			result.append(shtmp+'   '+"NaN"+"\n")
		arcpy.Delete_management(outname,"")
		print shtmp+"   OK!"
	file(txtname+"\\"+rstmp[0:len(rstmp)-4]+".txt",'w').writelines(result)

print "Finish!"
