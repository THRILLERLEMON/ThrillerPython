# -*- coding: cp936 -*-

#scrip
#ʹ��shp���������ü�դ�����ݲ�ͳ�ƾ�ֵ
print"ʹ��shp���������ü�դ�����ݲ�ͳ�ƽ����ֵ"

###########�޸Ĳ���###########

ras_file = r"D:\Franz\ETinversGPP\ETinvsGPP\VI_LfPLuc_GPPinvrs_his\82to12_crop_PdemVZ\GPPrl2cp\yave"   #���ü���ԭʼդ�����ݴ洢�ļ���·��
suffix = 'tif'  #���ü���ԭʼդ�����ݺ�׺
bvalue=-99   #���ü���ԭʼդ�����ݱ���ֵ

shp_file = r"D:\Franz2\45��С����߽缰ˮ��վ��\45��С����ֱ�Ӳü�"   #�ü�����shpģ�����ݴ洢�ļ���·��

ras_file_cut = r"C:\CutTmp"   #�ü���դ�����ݽ���洢�ļ���·��
txtname=r"D:\Franz\ETinversGPP\ETinvsGPP\VI_LfPLuc_GPPinvrs_his\82to12_crop_PdemVZ\GPPrl2cp\yave_sts"     #���ͳ���ı�·��

#############################

#���㲿��
import arcpy
arcpy.env.workspace=shp_file
shps=arcpy.ListFeatureClasses()
arcpy.env.workspace=ras_file
ras=arcpy.ListRasters('*',suffix)
print "����"+str(len(shps))+"��shp����"
#
print "Processing......"

for rs in ras:
	rstmp=rs.encode('cp936')
	print "����"+str(len(ras))+"��raster���ݣ����ڴ����"+str(ras.index(rs)+1)+"����"+rstmp
	result=[]
	for sh in shps:
		shtmp=sh.encode('cp936')
		shpfile=shp_file+"\\"+shtmp
		outname=ras_file_cut+"\\"+rstmp[0:len(rstmp)-4]+shtmp[0:len(shtmp)-4]+".tif"
		#arcpy.Clip_management(rstmp,"#",outname,shpfile,"#","ClippingGeometry")
		arcpy.Clip_management(rstmp,"#",outname,shpfile,str(bvalue),"ClippingGeometry") #������Чֵ
		try:
			stats=arcpy.GetRasterProperties_management(outname,"MEAN")
			result.append(shtmp+'   '+str(stats)+"\n")
		except:
			result.append(shtmp+'   '+"NaN"+"\n")
		arcpy.Delete_management(outname,"")
		print shtmp+"   OK!"
	file(txtname+"\\"+rstmp[0:len(rstmp)-4]+".txt",'w').writelines(result)

print "Finish!"
