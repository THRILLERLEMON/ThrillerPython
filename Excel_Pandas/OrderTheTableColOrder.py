# -*- coding: utf-8 -*-
import pandas as pd


def getNewpart(filename):
    newfile = pd.read_excel(filename, encoding='gbk')
    samepart = newfile.iloc[:, 0:10]
    newpart = newfile.drop(samepart, axis=1)
    return newpart


oldtable = pd.read_excel(
    'D:\\OneDrive\\SharedFile\\EXCEL 数据处理\\EXCELwork201908_linux_2ED\\AfterSX_SaX_NX_NM_HN_GS.xlsx', encoding='gbk')

firstpart = oldtable.iloc[:, 0:10]
newpart = getNewpart(
    'D:\\OneDrive\\SharedFile\\EXCEL 数据处理\\EXCELwork201908_linux_2ED\\AfterSX_SaX_NX_NM_HN_GS.xlsx')

newpartsort = newpart.sort_index(axis=1)
newtable = pd.concat([firstpart, newpartsort], axis=1)
# 删除值全部为空的列
# 返回一个bool型数组
col = newtable.count() == 0
for i in range(len(col)):
    if col[i]:
        newtable.drop(labels=col.index[i], axis=1, inplace=True)
countnumber = newtable.count()
baifenbi = countnumber / 379
newtable = newtable.append(countnumber, ignore_index=True).append(
    baifenbi, ignore_index=True)
print(newtable)

newtable.to_excel('C:/Users/thril/Desktop/OutputAll_Ordered.xlsx')
print('ok')
