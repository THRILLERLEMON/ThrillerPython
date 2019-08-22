# -*- coding: cp936 -*-
# polygon merge

# user

plg_path = r'E:\中国边界\王飞宇分块流域\分块流域'  # polygon存储路径
out_fc = r'E:\python_test\MergeTest01.shp'  # 输出结果及路径

# calculate
print 'Polygon Merge:'

import arcpy
from arcpy import env
arcpy.env.workspace = plg_path

fcList = arcpy.ListFeatureClasses()
print '共有' + str(len(fcList)) + '个Polygon'
print 'Processing......'

arcpy.Merge_management (fcList, out_fc, 'Mode')

print 'Finish~'
