# -*- coding: UTF-8 -*-
import matplotlib.pyplot as plt
import matplotlib
import gdal
import numpy as np
import os
import sys
# from mask.py import mask

#读取HDF数据

def Read_HDF(path):
    data_hdf=gdal.Open(path)
    meta_data=data_hdf.GetSubDatasets()#获取元数据
    # print(meta_data)
    for i,j in meta_data:
       if i.endswith("250m 16 days NDVI"):#判断字符串以……结尾

           print(12455669978)
           print(i)

    return i
#拼接
def mosaic( layer_name1, layer_name2,outpath_dataname):
    data_layer1 = gdal.Open(layer_name1)
    data_layer2 = gdal.Open(layer_name2)
    data_sub1 = data_layer1.ReadAsArray().astype(np.float)
    data_sub2 = data_layer2.ReadAsArray().astype(np.float)
    data = np.concatenate((data_sub1, data_sub2), axis=1)
    data = data / 10000
    data[data > -1] = 0
    driver = gdal.GetDriverByName('GTiff')  # 创建数据类型
    # driver.register()#创建数据驱动
    # savepath = "E:\data"
    # tif_savepath = savepath + "\ok123.tif"

    data_ok = driver.Create(outpath_dataname, 9600, 4800, 1, gdal.GDT_Float64,["COMPRESS=DEFLATE"])  # 创建数据集
    #print (data)
    projection = data_layer1.GetProjection()
    data_ok.SetGeoTransform(data_layer1.GetGeoTransform())
    data_ok.SetProjection(projection)
    data_ok.GetRasterBand(1).WriteArray(data)  # 将数组写进空数据集
    print ("数据写进完成")


#获取hdf数据的名称
def choose_data(filepath,out_path):
     # data_name=[]
     # (dirpath, dirname, dirfile)=os.walk(path)
     for i in filepath:     #遍历数据列表、
         str_i=str(i)
         print("choose_data")
         if str_i.endswith("hdf"):
            str1_name=[]
            str1_name=str_i.split('.')  #数据名：MOD13Q1.A2016001.h26v05.006.2016029065706
            for n in filepath:
                str_n=str(n)
                if str_n==str_i and  os.path.exists("E:\Python\data\mosaic_data\\"+str1_name[1]+".tif"):  #排除两个数据相同的情况
                    print("数据相同"+str_i)
                    continue
                else :
                    if (str_n.endswith("hdf")):
                        str2_name=[]
                        str2_name=str_n.split('.')
                        if str1_name[0]==str2_name[0] and str1_name[1]==str2_name[1] and str1_name[3]==str2_name[3]: #判断名称
                            # print('上下拼接')# 上下拼接
                            '''''
                             hv1=str1_name[2].split('v')
                             hv2=str2_name[2].split('v')
                             if hv1[0]==hv2[0] & (int(hv1[1])==int(hv2[1])+1|int(hv1[1])==int(hv2[1])-1):
                             '''''
                            #左右拼接str1=
                            str1 = str1_name[2]
                            str2 = str2_name[2]
                            h1 = str1[1:3]
                            v1 = str1[4:6]
                            h2 = str2[1:3]
                            v2 = str2[4:6]
                            print(h2,v2)
                            if v1==v2 and (int(h1)==(int(h2)+1) ):#判断行列号是否相近
                                # data_path1=os.path.join( path,m)
                                # data_path2=os.path.join( path,n)
                                layer_name1=Read_HDF(str_i)
                                layer_name2=Read_HDF(str_n)
                                outpath_dataname=os.path.join(out_path,str1_name[1]+".tif")
                                print("左右拼")
                                mosaic( layer_name2, layer_name1,outpath_dataname)
                            if v1==v2 and (int(h1)==(int(h2)-1) ):#判断行列号是否相近
                                # data_path1=os.path.join( path,m)
                                # data_path2=os.path.join( path,n)
                                layer_name1=Read_HDF(str_i)
                                layer_name2=Read_HDF(str_n)
                                outpath_dataname=os.path.join(out_path,str1_name[1]+".tif")
                                print("右左拼")
                                mosaic( layer_name1, layer_name2,outpath_dataname)

     print("所有数据拼接完成")

     #裁剪


def main(inpath,out_path):
    filepath=[]#存储路径+数据列表
    for dirpath, dirname, dirfile in os.walk(inpath):
        for file in dirfile:
            filepath.append(os.path.join(dirpath, file))#空列表添加路径数据
            print(filepath)
    choose_data(filepath,out_path)
#
# def msak():
#     print("开始裁剪")

    # outdata_path = os.path.join("E:\Python\data\mask_data", str1_name[1] + ".tif")
    # for shp in file_path:
    #     mask_data = gdal.Warp(outdata_path, outpath_dataname, cutlineDSName=shp, srcNodata=-2,
    #                           dstNodata=-2, cropToCutline=True, dstSRS="WGS84")
    # print("裁剪完成")
def mask(inpath,outpath,shp_path):
    filepath=[]#存储路径+数据列表
    for dirpath, dirname, dirfile in os.walk(inpath):
            for file in dirfile:
                filepath.append(os.path.join(dirpath, file))#空列表添加路径数据
    print(filepath)
    for i in filepath:     #遍历数据列表、
        file_name=str(i)
        if file_name.endswith(".tif"):
            print(file_name)
            (file_path,data_name) = os.path.split(file_name)
            outdata_path=os.path.join(outpath,data_name)
            # datapath=os.path.join(inpath,file_name)
            mask_data = gdal.Warp(outdata_path, file_name, cutlineDSName=shp_path, srcNodata=-2, dstNodata=-2, cropToCutline=True, dstSRS="WGS84")
            print("裁剪完成")
        else:
            print(i+"裁剪失败，数据格式非.tif")


if __name__ == '__main__':

    in_path = "E:\Python\data\hdf_data"
    mosaic_path= "E:\Python\data\mosaic_data"
    mask_path="E:\Python\data\mask_data"
    shp_path = "E:\Python\data\\xian.shp"  # 多区域裁剪可在此处添加shp

    main(in_path,mosaic_path)

    print ("开始裁剪")
    mask(mosaic_path,mask_path,shp_path)

# '''''
# path='E:\data\ok.tif'
# data2=gdal.Open(path)
#
# band=data2.GetRasterBand(1)#获取波段
# data2_ok=band.ReadAsArray()#根据波段读取数据矩阵
# # data2_ok=np.array(data2_ok)
# print(data2_ok.shape)
#
# plt.imshow(data2_ok)
# plt.show()#显示图像
# '''''
