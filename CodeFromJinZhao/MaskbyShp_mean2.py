# -*- coding: cp936 -*-

#scrip
#ʹ��shp���������ü�դ�����ݲ�ͳ�ƾ�ֵ
print"ʹ��shp���������ü�դ�����ݲ�ͳ�ƽ����ֵ"

###########�޸Ĳ���###########

ras_file = r"D:\VI_LPfat_GPP\VI_Cap01\LP_out\ETa2PRP\ALL"   #���ü���ԭʼդ�����ݴ洢�ļ���·��
suffix = 'tif'  #���ü���ԭʼդ�����ݺ�׺
bvalue= -99   #���ü���ԭʼդ�����ݱ���ֵ

shp_file = r"D:\�й��߽�\45��С����ֱ�Ӳü�"   #�ü�����shpģ�����ݴ洢�ļ���·��

ras_file_cut = r"C:\tmp"   #�ü���դ�����ݽ���洢�ļ���·��
txtname=r"D:\VI_LPfat_GPP\VI_Cap01\LP_out\ETa2PRP\smlbs"     #���ͳ���ı�·��

#############################


#���㲿��
import arcpy
arcpy.env.workspace=shp_file
shps=arcpy.ListFeatureClasses()
arcpy.env.workspace=ras_file
ras=arcpy.ListRasters('*',suffix)

print "����"+str(len(ras))+"��դ������"
#
print "Processing......"
for sh in shps:
    shtmp=sh.encode('cp936')
    shpfile=shp_file+"\\"+shtmp
    print "����"+str(len(shps))+"��shp���ݣ����ڴ����"+str(shps.index(sh)+1)+"����"+shtmp
    result=[]
    for rs in ras:
        rstmp=rs.encode('cp936')
        outname=ras_file_cut+"\\"+rstmp[0:len(rstmp)-4]+shtmp[0:len(shtmp)-len(suffix)]+"tif"
        #arcpy.Clip_management(rstmp,"#",outname,shpfile,"#","ClippingGeometry")
        arcpy.Clip_management(rstmp,"#",outname,shpfile,str(bvalue),"ClippingGeometry") #������Чֵ
        stats=arcpy.GetRasterProperties_management(outname,"MEAN")
        result.append(rstmp+'   '+str(stats)+"\n")
        #arcpy.Delete_management(outname,"")
        print rstmp+"   OK!"

    file(txtname+"\\"+shtmp[0:len(shtmp)-4]+".txt",'w').writelines(result)

print "Finish!"
