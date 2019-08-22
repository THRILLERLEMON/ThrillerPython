# -*- coding: cp936 -*-
# 修改部分
txt_path = r'E:\YYTcatchment\lonlattxt'  # txt数据存储路径
x_coords = "x"  # txt数据中经度字段名
y_coords = "y"  # txt数据中纬度字段名

prjfl = r"D:\Program Files (x86)\ArcGIS\Desktop10.0\Coordinate Systems\Geographic Coordinate Systems\World\WGS 1984.prj"  # 坐标系


point_path = r'E:\YYTcatchment\CatchmentSHP\Point'  # 点数据输出路径
line_path = r'E:\YYTcatchment\CatchmentSHP\Line'  # 线数据输出路径
polygon_path = r'E:\YYTcatchment\CatchmentSHP\Polygon'  # 面数据输出路径

# 计算部分
print 'XY to point,polyline and polygon'

import os
afs = os.listdir(txt_path)
tsts = []  # txt files
for fn in afs:
	if fn.endswith('.txt'):
		tsts.append(fn)

print "共有" + '%d'%len(tsts) + "个TXT数据"

import arcpy
from arcpy import env
env.workspace = txt_path

for ftst in tsts:
	ftst = ftst.encode('cp936')
	print ftst,
	
	# point
	in_Table = txt_path.encode('cp936') + '\\' + ftst
	out_Layer = "point_layer"
	outPoint = point_path.encode('cp936') + '\\Point_' + ftst[0:len(ftst) - 3] + 'shp'
	
	arcpy.MakeXYEventLayer_management(in_Table, x_coords, y_coords, out_Layer, prjfl, '#')
	arcpy.FeatureToPoint_management (out_Layer, outPoint)
	arcpy.Delete_management(out_Layer)
	print 'Point',
	
	# line
	outLine = line_path.encode('cp936') + '\\Line_' + ftst[0:len(ftst) - 3] + 'shp'
	arcpy.PointsToLine_management(outPoint, outLine, '#', '#', 'CLOSE')
	print 'Line',
	
	# polygon
	outPolygon = polygon_path.encode('cp936') + '\\Polygon_' + ftst[0:len(ftst) - 3] + 'shp'
	arcpy.FeatureToPolygon_management(outLine, outPolygon, '#', 'ATTRIBUTES', "#")
	
	# arcpy.AddField_management(outPolygon, area_coords, 'LONG')
	# cursor = arcpy.UpdateCursor(outPolygon)
	# for row in cursor:
		# row.setValue(area_coords, int(ftst[0:len(ftst) - 4]))
		# cursor.updateRow(row)
	
	print 'Polygon'

print 'Finish!'
