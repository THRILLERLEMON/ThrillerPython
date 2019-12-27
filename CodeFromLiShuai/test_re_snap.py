# -*-coding=utf-8-*-


import os

import arcpy
from arcpy.sa import *


def check_path_exit_or_not(path):
    """
    This subfunction judge path exists or not
    :param path: path
    :return: none
    """
    if not os.path.exists(path):
        os.makedirs(path)
    return


def dirlist(path, filelist, datformat):
    """
    This subfunction traverse the file of a specific format under a given folder, and save the file name to return.
    :param path: file path.
    :param filelist: fiel name list.
    :param datformat: data format, such as tif,hdf,asc etc.
    :return: fiel name list.
    """
    C_files = os.listdir(path)
    for file in C_files:
        newfile = os.path.join(path, file)
        if os.path.isdir(newfile):
            dirlist(file, filelist, datformat)
        else:
            if file.endswith(".%s" % datformat):
                filelist.append(newfile)
    return filelist


def get_landUse_path(path, file_path_name, Suffix_name):
    """
    get file list in path/file_path_name and end with *Suffix_name.tif
    :param path:
    :param file_path_name: file path name.
    :param Suffix_name: string before .tif.
    :return: file list
    """
    filelist = []
    C_files = os.listdir(path)
    for file in C_files:
        newfile = os.path.join(path, file)
        if os.path.isdir(newfile):
            new_path = os.path.join(newfile, file_path_name)
            c_files_new = os.listdir(new_path)
            for new_file in c_files_new:
                new_file_path = os.path.join(new_path, new_file)
                if os.path.isfile(new_file_path) and new_file_path.endswith('%s.tif' % Suffix_name):
                    filelist.append(new_file_path)
                else:
                    continue
        else:
            continue
    return filelist


def get_chield_path(path, file_path_name):
    """
    get file list in path/file_path_name and end with *Suffix_name.tif
    :param path:
    :param file_path_name: file path name.
    :return: file list
    """
    filelist = []
    C_files = os.listdir(path)
    for file in C_files:
        newfile = os.path.join(path, file)
        if os.path.isdir(newfile):
            new_path = os.path.join(newfile, file_path_name)
            c_files_new = os.listdir(new_path)
            for new_file in c_files_new:
                new_file_path = os.path.join(new_path, new_file)
                if new_file_path.endswith('.tif'):
                    filelist.append(new_file_path)
                else:
                    continue
        else:
            continue
    return filelist


# check this name with different suffix in the path
def check_suffix(path, name):
    filelist = []
    files = os.listdir(path)
    for filename in files:
        # split name and suffix
        portion = os.path.splitext(filename)
        if portion[0] == name:
            filelist.append(os.path.join(path, filename))
    return filelist


# remove files
def removeFile(path):
    if path.endswith('tif'):
        try:
            os.remove(path)
        except Exception as e:
            print("Move %s file error!" % path + '\n' +
                  "Error Message: " + str(e.args))
    else:
        try:
            path_dir, file_name = os.path.split(path)
            old_file_list = check_suffix(path_dir, file_name.split(".")[0])
            for i in old_file_list:
                os.remove(i)
        except Exception as e:
            print("Move %s file error!" % path + '\n' +
                  "Error Message: " + str(e.args))
    return


def removeFile1(path):
    rm_list = ['.tif', '.tfw', '.tif.aux.xml']
    path_dir, file_name = os.path.split(path)
    for i in rm_list:
        new_path = os.path.join(path_dir, "%s%s" % (file_name.split(".")[0], i))
        if os.path.exists(new_path):
            os.remove(new_path)
            print("%s is removed!" % new_path)
        else:
            continue

    return


def mask(input_Raster, Mask_shp_raster, snapraster, outpath):
    print("Input raster " + input_Raster)
    print("Mask raster " + Mask_shp_raster)
    print("Snap raster " + snapraster)
    arcpy.env.snapRaster = snapraster
    arcpy.env.cellSize = snapraster
    arcpy.env.extent = snapraster
    arcpy.env.outputCoordinateSystem = snapraster
    # Check out the ArcGIS Spatial Analyst extension license
    arcpy.CheckOutExtension("Spatial")

    # Execute ExtractByMask
    outExtractByMask = ExtractByMask(input_Raster, Mask_shp_raster)

    # Save the output
    outExtractByMask.save(outpath)
    print(outpath + " had been Masked!")
    return


def mask_main(rasterPath, maskPath, chield_dir):
    # rasterFiles = dirlist(rasterPath, [], 'tif')
    county_names = [u'未央区', u'新城区', u'碑林区', u'莲湖区', u'灞桥区', u'雁塔区', u'阎良区', u'临潼区', u'长安区', u'高陵区', u'鄠邑区', u'蓝田县',
                    u'周至县', u'金台区', u'渭滨区', u'凤翔县', u'岐山县', u'扶风县', u'眉县', u'秦都区', u'杨凌区', u'渭城区', u'兴平市', u'三原县',
                    u'泾阳县', u'乾县', u'礼泉县', u'永寿县', u'武功县', u'临渭区', u'华阴市', u'华州区', u'潼关县', u'大荔县', u'合阳县', u'澄城县',
                    u'蒲城县', u'白水县', u'富平县', u'洛南县']
    maskFiles = get_landUse_path(maskPath, u'land_use_2018', u'')
    rasterFiles = get_chield_path(rasterPath, chield_dir)
    print(len(maskFiles))
    for county_name in county_names:
        maskFile = [ii for ii in maskFiles if county_name in ii][0]
        rasterFile = [ii for ii in rasterFiles if county_name in ii][0]
        raster_dir, raster_basename = os.path.split(rasterFile)
        raster_dir_new = os.path.join(os.path.split(raster_dir)[0], 'land_use_last_clip_by18lucc')
        outpath_new = os.path.join(raster_dir_new, raster_basename)
        # if os.path.exists(outpath_new):
        # removeFile1(outpath_new)
        check_path_exit_or_not(raster_dir_new)
        if not os.path.exists(outpath_new):
            mask(rasterFile, maskFile, maskFile, outpath_new)
        else:
            print("%s is exits" % county_name)
    return


def main(rasterPath, maskPath, chield_dir):
    mask_main(rasterPath, maskPath, chield_dir)
    return


if __name__ == '__main__':
    # raster_path = u'/Volumes/dipper/LiShuai/2019/start'
    raster_path = u'G:\\LiShuai\\2019\\start'
    mask_shp_raster_path = u'G:\\LiShuai\\2019\\start'

    chield_dir = "land_use_last_clip"
    main(raster_path, mask_shp_raster_path, chield_dir)
