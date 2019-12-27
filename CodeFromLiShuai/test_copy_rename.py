# -*-coding=utf-8-*-

import os
import shutil
import sys


# import numpy as np
# from osgeo import gdal, ogr
# import pandas as pd

# reload(sys)
# sys.setdefaultencoding('utf-8')


def check_path_exit_or_not(path):
    """
    This subfunction judge path exists or not
    :param path: path
    :return: none
    """
    if not os.path.exists(path):
        os.makedirs(path)
    return


def readRaster_Geo_Prj(rasterPath, bandN):
    """
    This subfunction read raster data
    :param rasterPath: raster data absolute path
    :param bandN: band number
    :return: raster data, geoTransform, projection
    """
    # rasterPath = unicode(rasterPath, 'utf-8')
    # rasterPath = u'%s'%rasterPath
    ds = gdal.Open(rasterPath)
    data = ds.GetRasterBand(bandN).ReadAsArray()
    # data[data == data[0, 0]] = np.nan
    geoT = ds.GetGeoTransform()
    prj = ds.GetProjection()
    del ds
    return data, geoT, prj


def writeRaster(data, outpath_file, cols, rows, bands_num, geoTtansform, projection):
    """
    This subfunction write raster data out to the outpath_file
    :param data: raster data.
    :param outpath_file: output file name endwith .tif or .img.
    :param cols: the cols of data.
    :param rows: the rows of data.
    :param bands_num: outpput data bands number, must be equal to z value of data.
    :param geoTtansform: geographic coordinate system
    :param projection: projection coordinate system
    :return: none
    """

    # get band data type
    if bands_num == 1:
        data_tmp = data
    else:
        data_tmp = data[0, :, :]
    if 'int8' in data_tmp.dtype.name:
        datatype = gdal.GDT_Byte
    elif 'int16' in data_tmp.dtype.name:
        datatype = gdal.GDT_UInt16
    else:
        datatype = gdal.GDT_Float32

    # get data driver type
    basename = os.path.basename(outpath_file).split(".")[1]
    if basename == "tif":
        driver_name = "GTiff"
    else:
        raise ValueError(
            "The parameter outpath_file must be end of \".tif\" or \".img\"!")

    # save tiff to the outpath_file
    outdrv = gdal.GetDriverByName(driver_name)
    outdat = outdrv.Create(outpath_file, cols, rows, bands_num, datatype, ["COMPRESS=DEFLATE"])

    assert outdat is not None
    outdat.SetGeoTransform(geoTtansform)
    outdat.SetProjection(projection)
    if bands_num > 1:
        for i in range(bands_num):
            outdat.GetRasterBand(i + 1).WriteArray(data[i, :, :])
    else:
        outdat.GetRasterBand(1).WriteArray(data)
    outdat = None

    print("Data has already be write to %s" % outpath_file)
    return


def main(from_dir, target_dir, copy_dir):
    county_directions = [i1 for i1 in [os.path.join(from_dir, i) for i in os.listdir(from_dir)] if os.path.isdir(i1)]

    for i_from_direction in county_directions:
        child_directions = [i11 for i11 in [os.path.join(i_from_direction, i12) for i12 in os.listdir(i_from_direction)]
                            if os.path.isdir(i11)]
        rm_list = [i13 for i13 in child_directions if os.path.basename(i13) in copy_dir]

        county_name = os.path.basename(i_from_direction)
        new_target_dir_1 = os.path.join(target_dir, county_name)
        for i_rm in rm_list:
            # if "_" in os.path.basename(i_rm):
            #     new_name = os.path.basename(i_rm).split("_")[0]
            # else:
            #     new_name = os.path.basename(i_rm)
            new_name = "soil_e_level"
            # new_target_dir = os.path.join(new_target_dir_1, new_name)
            new_target_dir = os.path.join(target_dir, new_name)
            # new_target_dir = target_dir
            check_path_exit_or_not(new_target_dir)

            for root, dirs, files in os.walk(i_rm, topdown=False):
                for name in files:
                    new_name1 = name.split(".")[0]
                    prefix = ".".join(name.split(".")[1:])
                    if county_name in name:
                        # new_filename = "_".join(notif_name.split("_")[1:])

                        new_file_name = os.path.join(new_target_dir, "%s_%s.%s" % (new_name, county_name, prefix))
                        # new_file_name = os.path.join(new_target_dir, "%s.%s" % (new_name1,prefix))
                    else:
                        # new_file_name = os.path.join(new_target_dir, "%s_%s.tif" % (name.split(".")[0], county_name))
                        new_file_name = os.path.join(new_target_dir, "%s_%s.%s" % (new_name, county_name, prefix))
                        # new_file_name = os.path.join(new_target_dir, "%s.%s" % (new_name1, prefix))
                    # if not os.path.exists(new_file_name):
                    shutil.copyfile(os.path.join(root, name), new_file_name)
                    # print("%s copy completed!" % name)
                    # else:
                    #     print("%s is already exists!" % name)

            print("%s copy completed!" % i_from_direction)
    return


if __name__ == '__main__':
    # file_dir = "/Volumes/dipper/LiShuai/2019/result"
    file_dir = u"G:/LiShuai/2019/d_version/change_L1p4S1p25"
    # file_dir = "/Volumes/dipper/LiShuai/2018年成果数据"
    # file_dir = "/Volumes/dipper/LiShuai/2019动态监测"
    # target_dir = "/Volumes/Backup Plus/2019成果整理/各区县因子及土壤侵蚀"
    # target_dir = "/Volumes/Backup Plus/2019水土流失动态监测/2018年结果"
    # target_dir = "/Volumes/Backup Plus/2019成果整理/各区县因子及土壤侵蚀"
    target_dir = u"H:\\SOIL_E"

    # copy_dir = ['soil_e_level_update']
    copy_dir = ['soil_e_level_update_change_L1p4S1p25']
    # copy_dir = ['B']
    main(file_dir, target_dir, copy_dir)
