# -*- coding: utf-8 -*-
# @Time    : 2020/4/24 21:07
# @Author  : THRILLER柠檬
# @Email   : thrillerlemon@outlook.com
# @File    : CompareWithLCs_Agricultural_land_SubPlot.py
# @Software: PyCharm

import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.linear_model import LinearRegression
import statsmodels.api as sm
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

allCountryTrueData = pd.read_excel(
    'D:\\GIS_DATA\\GEE_DATA_landcover_V2\\CompareWithLCs\\CompareWithLCs_Agricultural_land\\耕地面积_单位-平方米.xlsx',
    sheet_name="pingfangmi")

fig = plt.figure(figsize=(10, 10), dpi=300)

rect1 = [0, 0.1, 0.4, 0.4]  # [左, 下, 宽, 高] 规定的矩形区域 （全部是0~1之间的数，表示比例）
rect2 = [0.46, 0.1, 0.4, 0.4]

font = {'family': 'Times New Roman',
        'weight': 'normal',
        'size': 15}

labels = ['GLASS-GLC', 'MCD12Q1-V6', 'GlobeLand30', 'GlobCover', 'FROM-GLC', 'GLCC']
colors = ['#02559B', '#F8C011', '#F4764D', '#5FC9C9', '#525870', '#88CD00']
years = ['1990-2014', '2001-2014', '2000, 2010', '2005, 2009', '2010', '1992']
samples = [4523, 2531, 491, 488, 207, 184]
R2_ThisData = [0.29, 0.35, 0.37, 0.33, 0.32, 0.19]
R2_OtherData = [0.02, 0.12, 0.72, 0.07, 0.51, 0.02]
RMSE_ThisData = [3.21, 3.00, 3.01, 3.05, 3.38, 3.80]
RMSE_OtherData = [4.74, 4.72, 5.63, 8.92, 9.22, 7.03]

ax1 = plt.axes(rect1)
X = [[0], [0.8]]
ax1.plot(X, X, color='#E61C17', linewidth=2, linestyle='-', alpha=0.98)
for i in np.arange(len(labels)):
    ax1.scatter(R2_OtherData[i], R2_ThisData[i], marker='o', color=colors[i], s=65, alpha=0.95, edgecolors='k',
                linewidths=0)
plt.text(R2_OtherData[0] + 0.02, R2_ThisData[0] - 0.015, s=str(labels[0]), color=colors[0],
         fontproperties='Times New Roman', size=14)
plt.text(R2_OtherData[1] - 0.06, R2_ThisData[1] + 0.017, s=str(labels[1]), color=colors[1],
         fontproperties='Times New Roman', size=14)
plt.text(R2_OtherData[2] - 0.17, R2_ThisData[2] + 0.02, s=str(labels[2]), color=colors[2],
         fontproperties='Times New Roman', size=14)
plt.text(R2_OtherData[3] + 0.02, R2_ThisData[3] - 0.018, s=str(labels[3]), color=colors[3],
         fontproperties='Times New Roman', size=14)
plt.text(R2_OtherData[4] + 0.02, R2_ThisData[4] - 0.015, s=str(labels[4]), color=colors[4],
         fontproperties='Times New Roman', size=14)
plt.text(R2_OtherData[5] + 0.02, R2_ThisData[5] - 0.015, s=str(labels[5]), color=colors[5],
         fontproperties='Times New Roman', size=14)

plt.text(0.02, 0.75, s=str(labels[0]) + ' (N = ' + str(samples[0]) + ')', color=colors[0],
         fontproperties='Times New Roman', size=13)
plt.text(0.02, 0.71, s=str(labels[1]) + ' (N = ' + str(samples[1]) + ')', color=colors[1],
         fontproperties='Times New Roman', size=13)
plt.text(0.02, 0.67, s=str(labels[2]) + ' (N = ' + str(samples[2]) + ')', color=colors[2],
         fontproperties='Times New Roman', size=13)
plt.text(0.02, 0.63, s=str(labels[3]) + ' (N = ' + str(samples[3]) + ')', color=colors[3],
         fontproperties='Times New Roman', size=13)
plt.text(0.02, 0.59, s=str(labels[4]) + ' (N = ' + str(samples[4]) + ')', color=colors[4],
         fontproperties='Times New Roman', size=13)
plt.text(0.02, 0.55, s=str(labels[5]) + ' (N = ' + str(samples[5]) + ')', color=colors[5],
         fontproperties='Times New Roman', size=13)

plt.xlim((0, 0.8))
plt.ylim((0, 0.8))
ax1.spines['bottom'].set_linewidth(1.5)
ax1.spines['left'].set_linewidth(1.5)
ax1.spines['top'].set_linewidth(1.5)
ax1.spines['right'].set_linewidth(1.5)
plt.yticks(fontproperties='Times New Roman', size=14)
plt.xticks(fontproperties='Times New Roman', size=14)

plt.xlabel('$\mathregular{R^2}$ (other datasets)', font)
plt.ylabel('$\mathregular{R^2}$ (this study)', font)

ax2 = plt.axes(rect2)
X = [[2], [10]]
ax2.plot(X, X, color='#E61C17', linewidth=2, linestyle='-', alpha=0.98)
for i in np.arange(len(labels)):
    ax2.scatter(RMSE_OtherData[i], RMSE_ThisData[i], marker='o', color=colors[i], s=65, alpha=0.95, edgecolors='k',
                linewidths=0)
plt.text(RMSE_OtherData[0] - 0.97, RMSE_ThisData[0] + 0.16, s=str(labels[0]), color=colors[0],
         fontproperties='Times New Roman', size=14)
plt.text(RMSE_OtherData[1] - 0.98, RMSE_ThisData[1] - 0.39, s=str(labels[1]), color=colors[1],
         fontproperties='Times New Roman', size=14)
plt.text(RMSE_OtherData[2] + 0.15, RMSE_ThisData[2] - 0.09, s=str(labels[2]), color=colors[2],
         fontproperties='Times New Roman', size=14)
plt.text(RMSE_OtherData[3] - 0.92, RMSE_ThisData[3] - 0.41, s=str(labels[3]), color=colors[3],
         fontproperties='Times New Roman', size=14)
plt.text(RMSE_OtherData[4] - 1.37, RMSE_ThisData[4] + 0.16, s=str(labels[4]), color=colors[4],
         fontproperties='Times New Roman', size=14)
plt.text(RMSE_OtherData[5] - 0.54, RMSE_ThisData[5] + 0.15, s=str(labels[5]), color=colors[5],
         fontproperties='Times New Roman', size=14)
plt.xlim((2, 10))
plt.ylim((2, 10))

plt.text(2.2, 9.5, s=str(labels[0]) + ' (' + str(years[0]) + ')', color=colors[0], fontproperties='Times New Roman',
         size=13)
plt.text(2.2, 9.1, s=str(labels[1]) + ' (' + str(years[1]) + ')', color=colors[1], fontproperties='Times New Roman',
         size=13)
plt.text(2.2, 8.7, s=str(labels[2]) + ' (' + str(years[2]) + ')', color=colors[2], fontproperties='Times New Roman',
         size=13)
plt.text(2.2, 8.3, s=str(labels[3]) + ' (' + str(years[3]) + ')', color=colors[3], fontproperties='Times New Roman',
         size=13)
plt.text(2.2, 7.9, s=str(labels[4]) + ' (' + str(years[4]) + ')', color=colors[4], fontproperties='Times New Roman',
         size=13)
plt.text(2.2, 7.5, s=str(labels[5]) + ' (' + str(years[5]) + ')', color=colors[5], fontproperties='Times New Roman',
         size=13)

ax2.spines['bottom'].set_linewidth(1.5)
ax2.spines['left'].set_linewidth(1.5)
ax2.spines['top'].set_linewidth(1.5)
ax2.spines['right'].set_linewidth(1.5)
plt.yticks(fontproperties='Times New Roman', size=14)
plt.xticks(fontproperties='Times New Roman', size=14)
plt.xlabel('RMSE (other datasets)', font)
plt.ylabel('RMSE (this study)', font)

plt.savefig(
    'D:\\GIS_DATA\\GEE_DATA_landcover_V2\\CompareWithLCs\\CompareWithLCs_Agricultural_land\\ShowAgrSatResult.png',
    dpi=300, bbox_inches='tight')
