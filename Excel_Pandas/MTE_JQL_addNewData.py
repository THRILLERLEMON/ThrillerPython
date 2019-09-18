# MTE work;add new train data to xlsx
# Windows 10 1903
# 2019.9.19
# JiQiulei thrillerlemon@outlook.com

import pandas as pd


def addVarData(tarTable, varTablePath, sheetStr):
    varsheet = pd.read_excel(varTablePath, sheet_name=sheetStr)
    for c, thisSite in enumerate(tarTable.loc[:, '站点']):
        if pd.isnull(thisSite):
            break
        thisRow = tarTable.loc[c]

        findresult = varsheet[(varsheet["year"] == thisRow['年']) & (
            varsheet["month"] == thisRow['月'])].copy()

        getValue = findresult[thisSite]
        tarTable.loc[c, sheetStr] = getValue.values
    print("over a var")
    return tarTable


oldtable = pd.read_excel(
    'E:\\OFFICE\\MTE_NEE_DATA\\GRA_Train_NEE_5.xlsx', sheet_name="All", encoding='gbk')
addDataXlsPath = 'E:\\OFFICE\\MTE_NEE_DATA\\addNewData.xlsx'

oldtable = addVarData(oldtable, addDataXlsPath, "GSOC")
oldtable=addVarData(oldtable,addDataXlsPath,"curvature")
oldtable=addVarData(oldtable,addDataXlsPath,"elevation")
oldtable=addVarData(oldtable,addDataXlsPath,"slope")
oldtable=addVarData(oldtable,addDataXlsPath,"tpi")
oldtable=addVarData(oldtable,addDataXlsPath,"twi")
oldtable=addVarData(oldtable,addDataXlsPath,"vbf")
oldtable=addVarData(oldtable,addDataXlsPath,"Manure_Application")
oldtable=addVarData(oldtable,addDataXlsPath,"NHx_N_Deposition")
oldtable=addVarData(oldtable,addDataXlsPath,"Nfertilizer_Application")
oldtable=addVarData(oldtable,addDataXlsPath,"NOy_N_Deposition")

print(oldtable)
oldtable.to_excel(
    'E:\OFFICE\MTE_NEE_DATA/outexcel.xlsx', encoding='gbk')
print('Already Finish Work! Good! THRILLER柠檬！')
