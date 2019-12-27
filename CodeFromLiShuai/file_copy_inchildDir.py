# -*-coding=utf-8-*-

import os
import shutil
import sys


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


def main(from_dir, target_dir, copy_dirname, t_dirname):
    county_names = [u'未央区', u'新城区', u'碑林区', u'莲湖区', u'灞桥区', u'雁塔区', u'阎良区', u'临潼区', u'长安区', u'高陵区', u'鄠邑区', u'蓝田县',
                    u'周至县', u'金台区', u'渭滨区', u'凤翔县', u'岐山县', u'扶风县', u'眉县', u'秦都区', u'杨凌区', u'渭城区', u'兴平市', u'三原县',
                    u'泾阳县', u'乾县', u'礼泉县', u'永寿县', u'武功县', u'临渭区', u'华阴市', u'华州区', u'潼关县', u'大荔县', u'合阳县', u'澄城县',
                    u'蒲城县', u'白水县', u'富平县', u'洛南县']

    from_directions = [i1 for i1 in [os.path.join(from_dir, i) for i in os.listdir(from_dir)] if os.path.isdir(i1)]
    target_directions = [i1 for i1 in [os.path.join(target_dir, i) for i in os.listdir(target_dir)] if
                         os.path.isdir(i1)]

    for i_county in county_names:
        from_d = [ii for ii in from_directions if i_county in ii][0]
        targ_d = [ii for ii in target_directions if i_county in ii][0]

        for i_copy in range(len(copy_dirname)):
            copy_dir_path = os.path.join(from_d, copy_dirname[i_copy])
            targ_dir_path = os.path.join(targ_d, t_dirname[i_copy])
            all_files = dirlist(copy_dir_path, [], 'tif')
            check_path_exit_or_not(targ_dir_path)
            for i_file in all_files:
                # path_dir, file_name = os.path.split(i_file)
                new_filepath = os.path.join(targ_dir_path, os.path.basename(i_file))
                # new_base_name = os.path.basename(path_dir)
                # old_file_list = check_suffix(path_dir, file_name.split(".")[0])
                # for i_old in old_file_list:
                # new_filename = "%s_%s" % (new_base_name, os.path.basename(i_old))
                # new_filepath = os.path.join(target_dir, new_filename)
                shutil.copyfile(i_file, new_filepath)
                print("%s copy completed!" % i_file)
    # for i_from_direction in from_directions:
    #     child_directions = [i11 for i11 in [os.path.join(i_from_direction, i12) for i12 in os.listdir(i_from_direction)]
    #                         if os.path.isdir(i11)]
    #
    #     for i_child in child_directions:
    #         all_files = dirlist(i_child, [], datafomate)
    #         copy_list = [i13 for i13 in all_files if os.path.basename(i13).split(".")[0] in copy_dir]
    #
    #         for i_copy in copy_list:
    #             path_dir, file_name = os.path.split(i_copy)
    #             new_base_name = os.path.basename(path_dir)
    #             old_file_list = check_suffix(path_dir, file_name.split(".")[0])
    #             for i_old in old_file_list:
    #                 new_filename = "%s_%s" % (new_base_name, os.path.basename(i_old))
    #                 new_filepath = os.path.join(target_dir, new_filename)
    #                 shutil.copyfile(i_old, new_filepath)
    #                 print("%s copy completed!" % i_old)
    #
    #         print("%s copy completed!" % i_child)
    #     print("%s copy completed!" % i_from_direction)
    return


if __name__ == '__main__':
    file_dir = u"H:\\LiShuai\\2019\\d_version\\change_L1p4S1p25"
    target_dir = u"G:\\2019成果整理\\各区县因子及土壤侵蚀"

    copy_dir = [u'L_smooth', u'S_smooth', u'soil_e_change_L1p4S1p25', u'soil_e_level_update_change_L1p4S1p25']
    targdir = [u'L', u'S', u'A', u'QD']
    main(file_dir, target_dir, copy_dir, targdir)
