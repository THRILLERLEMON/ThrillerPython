# -*- coding: cp936 -*-
# �޸Ĳ���
txt_path = r'E:\YYTcatchment\lonlattxt'  # txt���ݴ洢·��
x_coords = "x"  # txt�����о����ֶ���
y_coords = "y"  # txt������γ���ֶ���

prjfl = r"D:\Program Files (x86)\ArcGIS\Desktop10.0\Coordinate Systems\Geographic Coordinate Systems\World\WGS 1984.prj"  # ����ϵ


point_path = r'E:\YYTcatchment\CatchmentSHP\Point'  # ���������·��
line_path = r'E:\YYTcatchment\CatchmentSHP\Line'  # ���������·��
polygon_path = r'E:\YYTcatchment\CatchmentSHP\Polygon'  # ���������·��

# ���㲿��
print 'XY to point,polyline and polygon'

import os
afs = os.listdir(txt_path)
tsts = []  # txt files
for fn in afs:
	if fn.endswith('.txt'):
		tsts.append(fn)

print "����" + '%d'%len(tsts) + "��TXT����"

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
