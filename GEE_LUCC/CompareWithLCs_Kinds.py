# -*- coding: utf-8 -*-
# @Time    : 2020/4/17 21:07
# @Author  : THRILLER柠檬
# @Email   : thrillerlemon@outlook.com
# @File    : CompareWithLCs_Kinds.py
# @Software: PyCharm

import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, r2_score
import os
import sys

# 输出print内容
class Logger(object):
    def __init__(self, filename="Default.log"):
        self.terminal = sys.stdout
        self.log = open(filename, "a")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        pass


printpath = os.path.abspath(os.path.dirname(__file__))
type = sys.getfilesystemencoding()
sys.stdout = Logger('OutLog.txt')
print(printpath)

excelData = pd.read_excel(
    'D:\OneDrive\SharedFile\GEE_V2\CompareWithLCs\CompareFIG\ALLLLLLLLLLLL.xlsx', sheet_name="Sheet1")

csvPath='D:\\OneDrive\\SharedFile\\GEE_V2\\CompareWithLCs\\CompareFIG\\'

fig, ax = plt.subplots(figsize=(17, 7), dpi=300)

colors = ['#1b7201', '#50ff00', '#f2f100', '#a0c882', '#ad0101', '#0058f0', '#000000']
names = ['Forests', 'Shrubs', 'Grasslands', 'Agricultural lands', 'Built-up and Urban', 'Water', 'Barren lands']


# plt.scatter(1, 1,color='black', marker='o',s=50, label='MCD12Q1-V6')
# plt.scatter(2, 2,color='black', marker='x',s=50, label='ChinaLC1000')
# plt.scatter(3, 3,color='black', marker='H',s=50, label='FROM-GLC')
# plt.scatter(4, 4,color='black', marker='v',s=50, label='GlobeLand30')
# plt.scatter(5, 5,color='black', marker='s',s=50, label='GlobCover')
# plt.scatter(6, 6,color='black', marker='+',s=50, label='GLCC')
# plt.scatter(7, 7,color='black', marker='*',s=50, label='CGLS-LC100')
# ax.legend()
# plt.legend(bbox_to_anchor=(1.05, 0), loc=3, borderaxespad=0,prop={'family' : 'Times New Roman', 'size'   : 10})
# plt.savefig('D:\\OneDrive\\SharedFile\\GEE_V2\\CompareWithLCs\\figggg.png',dpi=300,bbox_inches='tight')



#Modis2001-2016
drawData = excelData.loc['0':'17']
for kind in np.arange(1, 8, 1):
    # plt.plot(list(np.arange(1,19,1)),drawData.iloc[:, kind],color=colors[kind-1],linewidth=9,linestyle='-',label=names[kind-1])
    plt.plot(list(np.arange(1, 19, 1)), drawData.iloc[:, kind].apply(lambda x: x / 10000000000), color=colors[kind - 1],
             linewidth=1, linestyle='-', marker='o', ms=5, label=names[kind - 1])
#LJY1985\1995\2000\2005
drawData = excelData.loc['18':'21']
for kind in np.arange(1,8,1):
    plt.plot(list(np.arange(19, 23, 1)), drawData.iloc[:, kind].apply(lambda x: x / 10000000000),
             color=colors[kind - 1], linewidth=1, linestyle='-', marker='x', ms=5, label=names[kind - 1])
#FROMGLC 2010 2015  2017
drawData = excelData.loc['22':'24']
for kind in np.arange(1,8,1):
    plt.plot(list(np.arange(23, 26, 1)), drawData.iloc[:, kind].apply(lambda x: x / 10000000000),
             color=colors[kind - 1], linewidth=1, linestyle='-', marker='H', ms=5, label=names[kind - 1])
#GlobalLandCover30 2000   2010
drawData = excelData.loc['25':'26']
for kind in np.arange(1,8,1):
    plt.plot(list(np.arange(26, 28, 1)), drawData.iloc[:, kind].apply(lambda x: x / 10000000000),
             color=colors[kind - 1], linewidth=1, linestyle='-', marker='v', ms=5, label=names[kind - 1])
#GlobCover 2005 2009
drawData = excelData.loc['27':'28']
for kind in np.arange(1,8,1):
    plt.plot(list(np.arange(28, 30, 1)), drawData.iloc[:, kind].apply(lambda x: x / 10000000000),
             color=colors[kind - 1], linewidth=1, linestyle='-', marker='s', ms=5, label=names[kind - 1])
#GLC 1992
drawData = list(excelData.loc[29])
for kind in np.arange(1, 8, 1):
    plt.scatter(30, drawData[kind] / 10000000000, color=colors[kind - 1], marker='+', s=50, alpha=0.99,
                label=names[kind - 1])
    # plt.plot(30,drawData[kind],color=colors[kind-1],linewidth=1,linestyle='--',label=names[kind-1])
#COPERNICUS_100 2015
drawData = list(excelData.loc[30])
for kind in np.arange(1, 8, 1):
    plt.scatter(31, drawData[kind] / 10000000000, color=colors[kind - 1], marker='*', s=50, alpha=0.99,
                label=names[kind - 1])
    # plt.plot(31,drawData[kind],color=colors[kind-1],linewidth=1,linestyle='--',label=names[kind-1])




plt.ylim((-30, 30))
years = ['2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014',
         '2015', '2016', '2017', '2018',
         '1985', '1995', '2000', '2005',
         '2010', '2015', '2017', '2000', '2010', '2005', '2009', '1992', '2015']
plt.xticks(list(np.arange(1, 32, 1)), years, fontsize=12, fontfamily='Times New Roman')

plt.yticks(fontproperties = 'Times New Roman', size = 12)


ax.set_xlabel('DataSet and Year', fontdict={'family' : 'Times New Roman', 'size'   : 15})
ax.set_ylabel(r'$\Delta$'+' Area($\mathregular{10^4km^2}$)',fontdict={'family' : 'Times New Roman', 'size'   : 15})
# ax.set_title('Agricultural land Area Compare',fontdict={'family' : 'Times New Roman', 'size'   : 20})

plt.savefig('D:\\OneDrive\\SharedFile\\GEE_V2\\CompareWithLCs\\figggg.png',dpi=300,bbox_inches='tight')
# plt.show()

