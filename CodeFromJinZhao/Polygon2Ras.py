# polygon covert to raster

# user

plg_path = r'H:\YYTcatchment\test\ply2ras\poly'  # polygon存储路径
ras_refer = 'H:\YYTcatchment\CatchmentRaster\CatchmentRas\CatchmentRas05.tif'  # 参考栅格数据 指定栅格投影、处理范围及分辨率

rasID = ''  # 生成栅格值的字段
celassg = ''  # 栅格赋值方式


out_path = r'H:\YYTcatchment\test\ply2ras\ras'  # 输出路径

# calculate
print 'Polygon Merge:'

import arcpy
from arcpy import env
arcpy.env.workspace = plg_path
arcpy.env.outputCoordinatesSystem = ras_refer
arcpy.env.extent = ras_refer
arcpy.env.snapRaster = ras_refer

fcList = arcpy.ListFeatureClasses()
print '共有' + str(len(fcList)) + '个Polygon'
print 'Processing......'

for plg in fcList:
	plgnm = plg.encode('cp936')
	outrasnm = out_path + '\\' + plgnm[0:len(plgnm) - 3] + 'tif'  # name.
	arcpy.PolygonToRaster_conversion(plgnm, rasID, outrasnm, '#', '#', ras_refer)
	print plgnm
	
print 'Finish~'
