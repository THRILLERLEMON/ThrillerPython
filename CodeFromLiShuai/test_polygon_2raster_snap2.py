# -*-coding:utf-8-*-


import os
import arcpy


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


def get_tif_landUse_path(path, file_path_name, Suffix_name):
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
                if os.path.isfile(new_file) and new_file.endswith('%s.tif' % Suffix_name):
                    filelist.append(new_file)
                else:
                    continue
        else:
            continue
    return filelist


def get_Snap_path(shppath, snapfile_path_name, snap_Suffix_name=''):
    """
    get shp file list and reference snap raster list.
    :param path: the path string, contains shapefile and snap raster.
    :param shpfile_path_name: shapefile direction name.
    :param snapfile_path_name: snap raster data direction name.
    :param shp_Suffix_name: shapefile name before .shp.
    :param snap_Suffix_name: snap raster data name before .tif.
    :return: shapefile list and snap raster file list.
    """
    snapfilelist = []
    c_files = os.listdir(shppath)
    for file in c_files:
        newfile = os.path.join(shppath, file)
        if os.path.isdir(newfile):

            snap_new_path = os.path.join(newfile, snapfile_path_name)
            snap_Suffix_name = snap_new_path.split(os.path.sep)[-2]
            snap_files_new = os.path.join(snap_new_path, "%s.tif" % snap_Suffix_name)
            if os.path.exists(snap_files_new):
                snapfilelist.append(snap_files_new)
            else:
                snap_files_new_list = dirlist(snap_new_path, [], 'tif')
                snapfilelist.append(snap_files_new_list[0])
        else:
            continue
    return snapfilelist


def shp2raster(input_shp, field, snapraster, outpath):
    print("Start " + input_shp)
    arcpy.env.snapRaster = snapraster
    arcpy.env.cellSize = snapraster
    arcpy.env.extent = snapraster
    arcpy.env.outputCoordinateSystem = snapraster

    # Execute FeatureToRaster
    arcpy.FeatureToRaster_conversion(input_shp, field, outpath)
    print(outpath + " had been rasterized!")
    return


def mask_main(shp_path, snapraster_path, outpath, outSuffix_name):
    county_names = [u'未央区', u'新城区', u'碑林区', u'莲湖区', u'灞桥区', u'雁塔区', u'阎良区', u'临潼区', u'长安区', u'高陵区', u'鄠邑区', u'蓝田县',
                    u'周至县', u'金台区', u'渭滨区', u'凤翔县', u'岐山县', u'扶风县', u'眉县', u'秦都区', u'杨凌区', u'渭城区', u'兴平市', u'三原县',
                    u'泾阳县', u'乾县', u'礼泉县', u'永寿县', u'武功县', u'临渭区', u'华阴市', u'华州区', u'潼关县', u'大荔县', u'合阳县', u'澄城县',
                    u'蒲城县', u'白水县', u'富平县', u'洛南县']
    field = 'CSDM'
    # field = 'TDLYDM'
    shpFiles = dirlist(shp_path, [], 'shp')
    snaprasterFiles = get_Snap_path(snapraster_path, u'土壤侵蚀')
    outpath_list = [i1 for i1 in [os.path.join(outpath, i) for i in os.listdir(outpath)] if os.path.isdir(i1)]

    for i_county in county_names:
        print(i_county)
        outpath_tmp = [i for i in outpath_list if i_county in i][0]
        shpFile = [i for i in shpFiles if i_county in i][0]
        snaprasterFile = [i for i in snaprasterFiles if i_county in i][0]

        outpath_new = os.path.join(outpath_tmp, outSuffix_name)
        check_path_exit_or_not(outpath_new)
        oupath_file = os.path.join(outpath_new, i_county + "_" + outSuffix_name + '.tif')
        # if os.path.exists(oupath_file):
        # os.remove(oupath_file)
        # shp2raster(shpFile, field, snaprasterFile, oupath_file)
        if not os.path.exists(oupath_file):
            shp2raster(shpFile, field, snaprasterFile, oupath_file)
        else:
            print("%s is already exists!" % oupath_file)
    return


def main(shp_path, snapraster_path, outpath, outSuffix_name):
    mask_main(shp_path, snapraster_path, outpath, outSuffix_name)
    return


if __name__ == '__main__':
    shp_path = u'G:\\LiShuai\\2019\\最终版土地利用\\更新后水保数据'
    snapraster_path = u"G:\\LiShuai\\2018年成果数据"
    outpath = u'G:\\LiShuai\\2019\\start'
    # outSuffix_name = 'land_use_last'
    outSuffix_name = 'measures_last'

    main(shp_path, snapraster_path, outpath, outSuffix_name)
