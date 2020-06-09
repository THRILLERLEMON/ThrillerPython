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

csvPath = 'D:\\OneDrive\\SharedFile\\GEE_V2\\CompareWithLCs\\CompareFIG\\'

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


fontL = {'family': 'Times New Roman',
         'size': 12}

fig = plt.figure(figsize=(14, 7), dpi=400)
rect1 = [0, 0.58, 0.9, 0.5]  # [左, 下, 宽, 高] 规定的矩形区域 （全部是0~1之间的数，表示比例）
rect2 = [0, 0, 0.2, 0.5]
rect3 = [0.26, 0, 0.1, 0.5]
rect4 = [0.42, 0, 0.1, 0.5]
rect5 = [0.58, 0, 0.1, 0.5]
rect6 = [0.74, 0, 0.05, 0.5]
rect7 = [0.85, 0, 0.05, 0.5]

# Modis2001-2016
ax1 = plt.axes(rect1)
drawData = excelData.loc['0':'17']
for kind in np.arange(1, 8, 1):
    ax1.plot(list(np.arange(1, 19, 1)), drawData.iloc[:, kind].apply(lambda x: x / 10000000000), color=colors[kind - 1],
             linewidth=1, linestyle='-', marker='o', ms=7, label=names[kind - 1])
    ax1.set_xticks(list(np.arange(1, 19, 1)))
    ax1.set_xticklabels(np.arange(2001, 2019, 1), fontsize=14, fontfamily='Times New Roman')
    ax1.set_yticks(list(np.arange(-25, 25, 5)))
    ax1.set_yticklabels(list(ax1.get_yticks()), fontsize=14, fontfamily='Times New Roman')
    ax1.set_xlabel('Year', fontdict={'family': 'Times New Roman', 'size': 14})
    ax1.set_ylabel(r'$\Delta$' + ' Area($\mathregular{10^4km^2}$)', fontdict={'family': 'Times New Roman', 'size': 14})
    # ax1.legend(prop=fontL,frameon=False)
# LJY1985\1995\2000\2005
ax2 = plt.axes(rect2)
drawData = excelData.loc['18':'21']
for kind in np.arange(1, 8, 1):
    ax2.plot(list(np.arange(1, 5, 1)), drawData.iloc[:, kind].apply(lambda x: x / 10000000000), color=colors[kind - 1],
             linewidth=1, linestyle='-', marker='x', ms=7, label=names[kind - 1])
    ax2.set_xticks(np.arange(1, 5, 1))
    ax2.set_xlim(0.4, 4.6)
    ax2.set_xticklabels(['1985', '1995', '2000', '2005'], fontsize=14, fontfamily='Times New Roman')
    ax2.set_yticks(list(np.arange(-25, 25, 5)))
    ax2.set_yticklabels(list(ax1.get_yticks()), fontsize=14, fontfamily='Times New Roman')
    ax2.set_xlabel('Year', fontdict={'family': 'Times New Roman', 'size': 14})
    ax2.set_ylabel(r'$\Delta$' + ' Area($\mathregular{10^4km^2}$)', fontdict={'family': 'Times New Roman', 'size': 14})
# FROMGLC 2010 2015  2017
ax3 = plt.axes(rect3)
drawData = excelData.loc['23':'24']
for kind in np.arange(1, 8, 1):
    ax3.plot(list(np.arange(1, 3, 1)), drawData.iloc[:, kind].apply(lambda x: x / 10000000000), color=colors[kind - 1],
             linewidth=1, linestyle='-', marker='H', ms=7, label=names[kind - 1])
    ax3.set_xticks(np.arange(1, 3, 1))
    ax3.set_xlim(0.4, 2.6)
    ax3.set_xticklabels(['2015', '2017'], fontsize=14, fontfamily='Times New Roman')
    ax3.set_yticks(list(np.arange(-25, 25, 5)))
    ax3.set_yticklabels(list(ax1.get_yticks()), fontsize=14, fontfamily='Times New Roman')
    ax3.set_xlabel('Year', fontdict={'family': 'Times New Roman', 'size': 14})
    ax3.set_ylabel(r'$\Delta$' + ' Area($\mathregular{10^4km^2}$)', fontdict={'family': 'Times New Roman', 'size': 14})
# GlobalLandCover30 2000   2010
ax4 = plt.axes(rect4)
drawData = excelData.loc['25':'26']
for kind in np.arange(1, 8, 1):
    ax4.plot(list(np.arange(1, 3, 1)), drawData.iloc[:, kind].apply(lambda x: x / 10000000000), color=colors[kind - 1],
             linewidth=1, linestyle='-', marker='v', ms=7, label=names[kind - 1])
    ax4.set_xticks(np.arange(1, 3, 1))
    ax4.set_xlim(0.4, 2.6)
    ax4.set_xticklabels(['2000', '2010'], fontsize=14, fontfamily='Times New Roman')
    ax4.set_yticks(list(np.arange(-25, 25, 5)))
    ax4.set_yticklabels(list(ax1.get_yticks()), fontsize=14, fontfamily='Times New Roman')
    ax4.set_xlabel('Year', fontdict={'family': 'Times New Roman', 'size': 14})
    ax4.set_ylabel(r'$\Delta$' + ' Area($\mathregular{10^4km^2}$)', fontdict={'family': 'Times New Roman', 'size': 14})
# GlobCover 2005 2009
ax5 = plt.axes(rect5)
drawData = excelData.loc['27':'28']
for kind in np.arange(1, 8, 1):
    ax5.plot(list(np.arange(1, 3, 1)), drawData.iloc[:, kind].apply(lambda x: x / 10000000000), color=colors[kind - 1],
             linewidth=1, linestyle='-', marker='s', ms=7, label=names[kind - 1])
    ax5.set_xticks(np.arange(1, 3, 1))
    ax5.set_xlim(0.4, 2.6)
    ax5.set_xticklabels(['2005', '2009'], fontsize=14, fontfamily='Times New Roman')
    ax5.set_yticks(list(np.arange(-25, 25, 5)))
    ax5.set_yticklabels(list(ax1.get_yticks()), fontsize=14, fontfamily='Times New Roman')
    ax5.set_xlabel('Year', fontdict={'family': 'Times New Roman', 'size': 14})
    ax5.set_ylabel(r'$\Delta$' + ' Area($\mathregular{10^4km^2}$)', fontdict={'family': 'Times New Roman', 'size': 14})
# GLC 1992
ax6 = plt.axes(rect6)
drawData = list(excelData.loc[29])
for kind in np.arange(1, 8, 1):
    ax6.scatter(1, drawData[kind] / 10000000000, color=colors[kind - 1], marker='+', s=75, alpha=0.99,
                label=names[kind - 1])
    ax6.set_xticks([1])
    ax6.set_xticklabels(['1992'], fontsize=14, fontfamily='Times New Roman')
    ax6.set_yticks(list(np.arange(-25, 25, 5)))
    ax6.set_yticklabels(list(ax1.get_yticks()), fontsize=14, fontfamily='Times New Roman')
    ax6.set_xlabel('Year', fontdict={'family': 'Times New Roman', 'size': 14})
    ax6.set_ylabel(r'$\Delta$' + ' Area($\mathregular{10^4km^2}$)', fontdict={'family': 'Times New Roman', 'size': 14})
# COPERNICUS_100 2015
ax7 = plt.axes(rect7)
drawData = list(excelData.loc[30])
for kind in np.arange(1, 8, 1):
    ax7.scatter(1, drawData[kind] / 10000000000, color=colors[kind - 1], marker='*', s=75, alpha=0.99,
                label=names[kind - 1])
    ax7.set_xticks([1])
    ax7.set_xticklabels(['2015'], fontsize=14, fontfamily='Times New Roman')
    ax7.set_yticks(list(np.arange(-25, 25, 5)))
    ax7.set_yticklabels(list(ax1.get_yticks()), fontsize=14, fontfamily='Times New Roman')
    ax7.set_xlabel('Year', fontdict={'family': 'Times New Roman', 'size': 14})
    ax7.set_ylabel(r'$\Delta$' + ' Area($\mathregular{10^4km^2}$)', fontdict={'family': 'Times New Roman', 'size': 14})

plt.savefig('D:\\OneDrive\\SharedFile\\GEE_V2\\CompareWithLCs\\figggg.png', bbox_inches='tight')
# plt.show()
