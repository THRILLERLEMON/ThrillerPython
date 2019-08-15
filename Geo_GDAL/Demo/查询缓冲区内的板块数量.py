from osgeo import ogr
# 河流矢量数据
shp1 = ogr.Open('F:/data/shuju/s_l1.shp')
# 斑块矢量数据(面状的)
shp2 = ogr.Open('F:/data/shuju/province-p2009.shp')
# 需要注意的是，无论图层在ArcGIS里的投影是什么，在这里投影都会和第一个导入的图层一样
layer1 = shp1.GetLayer()
layer2 = shp2.GetLayer()
memory_driver = ogr.GetDriverByName('memory')
memory_ds = memory_driver.CreateDataSource('temp')
# 创建缓冲区
buff_lyr = memory_ds.CreateLayer('buffer')
buff_feat = ogr.Feature(buff_lyr.GetLayerDefn())
# 建立1KM的缓冲区
for feat in layer1:
    buff_geom = feat.geometry().Buffer(1000)
    tmp = buff_feat.SetGeometry(buff_geom)
    tmp = buff_lyr.CreateFeature(buff_feat)

result_lyr = memory_ds.CreateLayer('result')
# 将河流缓冲区与斑块矢量进行重叠
buff_lyr.Intersection(layer2, result_lyr)
# 统计1KM内斑块的个数
print('缓冲区范围内斑块个数: {}个'.format(result_lyr.GetFeatureCount()))
