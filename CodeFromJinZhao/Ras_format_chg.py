# -*- coding: cp936 -*-
#栅格转格式另存

#修改部分

ras_path=r"C:\其他任务\白燏\data\org"     #栅格数据存储路径
in_suffix='dat'    #原始数据后缀
unvalid='#'    #需要赋值为NoData的值，如果没有，则填写'#'

out_path=r"C:\其他任务\白燏\data\org2"    #结果存储路径
out_suffix='tif'    #结果数据后缀
########

#计算部分
print "栅格数据批量转格式另存"
print "输入栅格后缀："+in_suffix
print "输出栅格后缀："+out_suffix
print "Processing......"

import arcpy
arcpy.env.workspace=ras_path

for ras_file in arcpy.ListRasters('*',in_suffix):
    rasorig=ras_file.encode('cp936')
    out_name=out_path+"\\"+rasorig[0:len(rasorig)-len(in_suffix)]+out_suffix
    arcpy.CopyRaster_management(rasorig,out_name,"","",unvalid,"NONE","NONE","")
    print rasorig[0:len(rasorig)-3]+out_suffix+"  OK!"
print "Finish!"
