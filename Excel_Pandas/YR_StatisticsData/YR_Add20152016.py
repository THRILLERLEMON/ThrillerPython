# -*- coding: utf-8 -*-
# coding: utf-8
import chardet
import xlwt
import numpy as np
import pandas as pd
import os
import sys


def FindXLSfile(parstr, path):
    filenames = os.listdir(path)
    pxlsList = list()
    for i, filename in enumerate(filenames):
        # 转码
        # filename = filename.decode('gbk')
        findresult = filename.find(parstr)
        if findresult != -1:
            pxlsList.append(filename)
        else:
            continue
    return pxlsList


def is_number(s):
    """是否是数字"""
    if s == '.':
        return True
    try:
        float(s)
        return True
    except ValueError:
        pass
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
    return False


def FindValue(parstr, pFileList, pCountryCode, pYear):
    for file in pFileList:
        # print("查找 " + str(pCountryCode) + "县" +
        #       str(pYear) + " 年" + parstr + " in " + str(file))
        fpath = path + "\\" + file
        thisSheet = pd.read_excel(fpath)
        verifyStr = thisSheet.iloc[0, 10]
        if parstr == verifyStr:
            findresult = thisSheet[
                (thisSheet["county_code"] == int(pCountryCode))
                & (thisSheet["temporal_period"] == pYear)
                ].copy()
            if findresult.empty is True:
                continue
            else:
                # print(findresult.iloc[0])
                # print(findresult.iloc[0, 10])
                if not pd.isnull(findresult.iloc[0, 10]):
                    return findresult.iloc[0, 10]
                # else:
                # print("find one it is " + str(findresult.iloc[0, 10]))
                # print ("find a empty")
        else:
            includOrNot = file.find(parstr)
            if includOrNot == -1:
                print(file + " has something wrong")


# 参量_年份
parszhang = ["国内生产总值", "第一产业生产总值", "第二产业生产总值", "第三产业生产总值", "工业生产总值", "大牲畜年末存栏", "年末生猪存栏", "羊年末存栏只数"]
path = 'E:\\OFFICE\\EXCEL 数据处理\\Add1516Data'
onetoN_Code = pd.read_excel(path + '\\OnetoN_Code.xlsx', sheet_name="Code")

# 循环每一个参数
for i, par in enumerate(parszhang):
    allCountryData = pd.read_excel(path + '\\各变量RES0522.xls', sheet_name=par)
    xlsList = FindXLSfile(par, path)
    # 循环每一个县
    for c, oneCountryCode in enumerate(allCountryData.loc[:, "County_code_N"]):
        if pd.isnull(oneCountryCode):
            break
        # 循环每一年
        for yearn in np.arange(2015, 2017, 1):
            filedname = par + "_" + str(yearn)
            # 对城区的代码进行加和处理
            if allCountryData.loc[c, "ShaanXi"] == 0 and int(oneCountryCode) in onetoN_Code.columns:
                thisCityNCode = onetoN_Code.loc[:, oneCountryCode]
                urbanValue = 0
                for nCode in thisCityNCode:
                    if pd.isnull(nCode):
                        break
                    thisCountryValue = FindValue(par, xlsList, nCode, yearn)
                    if pd.isnull(thisCountryValue):
                        thisCountryValue = 0
                    if str(thisCountryValue).isspace():
                        thisCountryValue = 0
                    if not is_number(thisCountryValue):
                        thisCountryValue = 0
                    try:
                        urbanValue = urbanValue + thisCountryValue
                    except:
                        try:
                            input_num = float(thisCountryValue)
                            urbanValue = urbanValue + input_num
                        except:
                            print('在计算' + str(oneCountryCode) + '城区的_' + par +
                                  '_时，出现问题，寻找到的' + str(nCode) + '区县' + str(yearn) + '年的值不是一个数字，忽略这个值，请检查！')
                if urbanValue == 0:
                    continue
                allCountryData.loc[c, filedname] = urbanValue
                # print(allCountryData.loc[c, newfiledname])
                print("ok find a one2N")
            else:
                # 正常的区县
                findedvalue = FindValue(par, xlsList, oneCountryCode, yearn)
                if pd.isnull(findedvalue):
                    continue
                if not is_number(findedvalue):
                    continue
                try:
                    allCountryData.loc[c, filedname] = findedvalue
                except:
                    print('在计算' + str(oneCountryCode) + '普通县' + str(yearn) + '年的_' + par +
                          '_时，出现问题，请检查！')
                # print(allCountryData[newfiledname].iloc[c])
                print("ok find a normal value")
            print('完成 ' + str(oneCountryCode) + '县的' + str(yearn) + '年' + par + '的值')
    allCountryData.to_excel(path + '//' + par + '.xls')
    print('完成 ' + par + '所有值的寻找')
print('Already Finish Work! Good! THRILLER柠檬！')
