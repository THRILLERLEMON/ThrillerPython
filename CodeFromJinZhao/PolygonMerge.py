# -*- coding: cp936 -*-
# polygon merge

# user

plg_path = r'E:\�й��߽�\������ֿ�����\�ֿ�����'  # polygon�洢·��
out_fc = r'E:\python_test\MergeTest01.shp'  # ��������·��

# calculate
print 'Polygon Merge:'

import arcpy
from arcpy import env
arcpy.env.workspace = plg_path

fcList = arcpy.ListFeatureClasses()
print '����' + str(len(fcList)) + '��Polygon'
print 'Processing......'

arcpy.Merge_management (fcList, out_fc, 'Mode')

print 'Finish~'
