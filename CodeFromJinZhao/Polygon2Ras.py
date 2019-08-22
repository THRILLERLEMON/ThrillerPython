# polygon covert to raster

# user

plg_path = r'H:\YYTcatchment\test\ply2ras\poly'  # polygon�洢·��
ras_refer = 'H:\YYTcatchment\CatchmentRaster\CatchmentRas\CatchmentRas05.tif'  # �ο�դ������ ָ��դ��ͶӰ������Χ���ֱ���

rasID = ''  # ����դ��ֵ���ֶ�
celassg = ''  # դ��ֵ��ʽ


out_path = r'H:\YYTcatchment\test\ply2ras\ras'  # ���·��

# calculate
print 'Polygon Merge:'

import arcpy
from arcpy import env
arcpy.env.workspace = plg_path
arcpy.env.outputCoordinatesSystem = ras_refer
arcpy.env.extent = ras_refer
arcpy.env.snapRaster = ras_refer

fcList = arcpy.ListFeatureClasses()
print '����' + str(len(fcList)) + '��Polygon'
print 'Processing......'

for plg in fcList:
	plgnm = plg.encode('cp936')
	outrasnm = out_path + '\\' + plgnm[0:len(plgnm) - 3] + 'tif'  # name.
	arcpy.PolygonToRaster_conversion(plgnm, rasID, outrasnm, '#', '#', ras_refer)
	print plgnm
	
print 'Finish~'
