# -*- coding: cp936 -*-

print"栅格数据统计"

###########修改部分###########

ras_file = r"D:\Franz\ETinversGPP\ET_PRP_gaps\PRP_GIDS\MnEle65Neg30stSmth2_crct_VerticalZonal_82to12Yr"   #原始栅格数据存储文件夹路径
suffix = 'tif'  #原始栅格数据后缀
valid=[0,65500] #有效值范围
sfactor=1 #scale factor
tmpdoc = r'D:\Franz\ETinversGPP\ET_PRP_gaps\PRP_GIDS\tmp'  # 临时数据存储空目录

sample=r''   #重投影、捕捉栅格、处理范围参考影像
stats_fun='MEAN'	#统计方法，参考如下：

'''
MINIMUM —返回输入栅格中的所有像元的最小值。 
MAXIMUM —返回输入栅格中的所有像元的最大值。 
MEAN —返回输入栅格中的所有像元的平均值。 
STD —返回输入栅格中的所有像元的标准差。 
UNIQUEVALUECOUNT —返回输入栅格中的唯一值的数目。 
TOP —返回范围的顶部值或 YMax 值。 
LEFT —返回范围的左侧值或 XMin 值。 
RIGHT —返回范围的右侧值或 XMax 值。 
BOTTOM —返回范围的底部值或 YMin 值。 
CELLSIZEX —返回 x 方向上的像元大小。 
CELLSIZEY —返回 y 方向上的像元大小。 
VALUETYPE —返回输入栅格中像元值的类型'''

txtname=r"D:\Franz\ETinversGPP\ET_PRP_gaps\PRP_GIDS\tmp\Pcrct_his_mean.txt"     #输出统计文本

#############################


#计算部分
import arcpy
import warnings
warnings.filterwarnings("ignore")
from arcpy.sa import *
arcpy.CheckOutExtension("Spatial")
arcpy.env.workspace=ras_file
arcpy.env.extent = sample
arcpy.env.mask = sample

ras=arcpy.ListRasters('*',suffix)
print "共有"+str(len(ras))+"个栅格数据"
print "Processing......"
result=[]
for rs in ras:
	rstmp=rs.encode('cp936')
	rs_cut=tmpdoc+"\\"+rstmp[0:len(rstmp) - len(suffix) - 1]+'_cut.tif'
	#arcpy.gp.RasterCalculator_sa("SetNull('"+rstmp+"'=="+str(bvalue)+",'"+rstmp+"')",rs_cut)
	arcpy.gp.RasterCalculator_sa("SetNull(('"+rstmp+"'<"+str(valid[0])+")|('"+rstmp+"'>"+str(valid[1])+"),'"+rstmp+"'*"+str(sfactor)+")",rs_cut)
	stats=arcpy.GetRasterProperties_management(rs_cut,stats_fun)
	arcpy.Delete_management(rs_cut,"")
	result.append(rstmp+'   '+str(stats)+"\n")
	print rstmp+"   OK!"

file(txtname,'w').writelines(result)
print "Finish!"
