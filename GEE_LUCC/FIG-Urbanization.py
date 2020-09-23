# -*- coding: utf-8 -*-
# @Time    : 2020/8/14 09:35
# @Author  : THRILLER柠檬
# @Email   : thrillerlemon@outlook.com
# @File    : FIG-Urbanization.py
# @Software: VSCODE

import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.linear_model import LinearRegression
import statsmodels.api as sm
from scipy.stats import pearsonr
import os
import sys

path = 'D:\\OneDrive\\SharedFile\\GEE_V2\\Urbanization\\'

parList = ['GDP(亿元)', '工业增加值(亿元)', '总人口(万人)', '城镇化率（%）']
parScaleList = [0.1, 0.1, 0.01, 1]

parYlabelListFull = ['Gross domestic product (Billion Yuan)', 'Industrial added value (Billion Yuan)',
                     'Population (Million)', 'Urbanization rate (%)']
parYlabelList = ['GDP (billion Yuan)', 'IDV (billion Yuan)',
                 'Population (million)', 'Urbanization rate (%)']

cityList = ['Zhengzhou', 'Xi an', 'Taiyuan', 'Lanzhou', 'Hohhot', 'Xining']

ColormapList = {
    'Zhengzhou': '#53BCE9',
    'Xi an': '#E02F5E',
    'Taiyuan': '#E29A4B',
    'Lanzhou': '#35B568',
    'Hohhot': '#6B49E6',
    'Xining': '#525870'
}

font = {'family': 'Times New Roman',
        'weight': 'normal',
        'size': 14}

fig = plt.figure(figsize=(12, 8), dpi=300)

for iPar in np.arange(0, len(parList)):
    ax = fig.add_subplot(2, 2, iPar + 1)
    for iCity in np.arange(0, len(cityList)):
        pData = pd.read_excel(path + 'Urbanizationsta.xls', sheet_name=cityList[iCity])
        ax.plot(list(pData['Year']), pData[parList[iPar]] * parScaleList[iPar], color=ColormapList[cityList[iCity]],
                label=cityList[iCity], linewidth=2, linestyle='-')
        plt.yticks(fontproperties='Times New Roman', size=14)
        plt.xticks(fontproperties='Times New Roman', size=14)
        ax.set_xlim(1989.5, 2017.5)
        plt.xlabel('Year', font)
        plt.ylabel(parYlabelList[iPar], font)
        if iPar == 0:
            plt.legend(loc='upper left', ncol=2, prop={'family': 'Times New Roman', 'size': 12}, frameon=False)

# ax0 = plt.axes(rect0)
# bottom = pd.Series(np.zeros(len(gpData.index)), index=gpData.index)
# for sheng in gpData.columns:
#     ax0.bar([j for j in list(gpData[sheng].index)], list(gpData[sheng]), 0.6,
#             label=str(sheng) + ' (' + shortNameMap[sheng] + ')', color=ColormapList[sheng], bottom=list(bottom))
#     bottom = bottom.add(gpData[sheng])
# plt.yticks(fontproperties='Times New Roman', size=14)
# plt.xticks(fontproperties='Times New Roman', size=14)
# ax0.set_ylim(0, 55)
# ax0.set_xlim(1985.5, 2015.5)

# plt.xlabel('Year', font)
# plt.ylabel('Grain production ($\mathregular{10^6}$ t)', font)
# plt.legend(loc='upper left', ncol=4, prop={'family': 'Times New Roman', 'size': 14}, frameon=False)

# ax1 = plt.axes(rect1)

# ax1.scatter(laData['Total'], fertilizerData['Total'], marker='o',
#             color='#1F78B4', s=70, alpha=0.8, edgecolors='k', linewidths=0)

# model = LinearRegression()
# X = laData['Total'].values.reshape(-1, 1)
# Y = fertilizerData['Total'].values.reshape(-1, 1)
# model.fit(X, Y)
# X2 = [[12], [22]]
# y2 = model.predict(X2)
# plt.plot(X2, y2, color='r', linewidth=2, linestyle='--')
# SStot = np.sum((Y - np.mean(Y)) ** 2)
# SSres = np.sum((Y - model.predict(X)) ** 2)
# compR2 = format(1 - SSres / SStot, '.2f')
# plt.yticks(fontproperties='Times New Roman', size=14)
# plt.xticks(fontproperties='Times New Roman', size=14)
# r, p = pearsonr(laData['Total'], fertilizerData['Total'])
# print(r, p, compR2)

# prInfo = '$\mathbf{\mathit{r}}$ =' + '%.3f' % r + '\n$\mathbf{\mathit{p}}$<0.001'
# ax1.text(10.5, 503, s=prInfo, fontproperties='Times New Roman', size=16)

# plt.xlim((10, 24))
# plt.ylim((200, 550))
# plt.xlabel('Leaf area of agricultural lands ($\mathregular{10^4}$ $\mathregular{km^2}$)', font)
# plt.ylabel('Chemical fertilizer usage ($\mathregular{10^4}$ t)', font)

# ax11 = plt.axes(rect11)
# plt.ylim((0, 1.2))
# for pro in provinceList:
#     r, p = pearsonr(laData[pro], fertilizerData[pro])
#     ax11.bar(shortNameMap[pro], r, color=ColormapList[pro], width=0.5)
#     if 0.01 < p < 0.05:
#         ax11.text(shortNameMap[pro], r + 0.05, s='*', rotation=90,
#                   fontproperties='Times New Roman', size=14)
#     if 0.001 < p < 0.01:
#         ax11.text(shortNameMap[pro], r + 0.05, s='**', rotation=90,
#                   fontproperties='Times New Roman', size=14)
#     if p < 0.001:
#         ax11.text(shortNameMap[pro], r + 0.05, s='***',
#                   rotation=90, fontproperties='Times New Roman', size=14)
# plt.yticks(fontproperties='Times New Roman', size=14)
# plt.xticks(fontproperties='Times New Roman', size=14)
# plt.xlabel('Province', font)
# plt.ylabel('Correlation coefficient', font)

# ax2 = plt.axes(rect2)

# ax2.scatter(laData['Total'], machineryData['Total'], marker='o',
#             color='#1F78B4', s=70, alpha=0.8, edgecolors='k', linewidths=0)
# model = LinearRegression()
# X = laData['Total'].values.reshape(-1, 1)
# Y = machineryData['Total'].values.reshape(-1, 1)
# model.fit(X, Y)
# X2 = [[12], [22]]
# y2 = model.predict(X2)
# plt.plot(X2, y2, color='r', linewidth=2, linestyle='--')
# SStot = np.sum((Y - np.mean(Y)) ** 2)
# SSres = np.sum((Y - model.predict(X)) ** 2)
# compR2 = format(1 - SSres / SStot, '.2f')

# r, p = pearsonr(laData['Total'], machineryData['Total'])
# print(r, p, compR2)

# prInfo = '$\mathbf{\mathit{r}}$ =' + '%.3f' % r + '\n$\mathbf{\mathit{p}}$<0.001'
# ax2.text(10.5, 89, s=prInfo, fontproperties='Times New Roman', size=16)

# plt.yticks(fontproperties='Times New Roman', size=14)
# plt.xticks(fontproperties='Times New Roman', size=14)
# plt.xlim((10, 24))
# plt.ylim((20, 100))
# plt.xlabel('Leaf area of agricultural lands ($\mathregular{10^4}$ $\mathregular{km^2}$)', font)
# plt.ylabel('Machinery power ($\mathregular{10^6}$ kilowatts)', font)

# ax22 = plt.axes(rect22)
# plt.ylim((0, 1.2))
# for pro in provinceList:
#     r, p = pearsonr(laData[pro], machineryData[pro])
#     ax22.bar(shortNameMap[pro], r, color=ColormapList[pro], width=0.5)
#     if 0.01 < p < 0.05:
#         ax22.text(shortNameMap[pro], r + 0.05, s='*', rotation=90,
#                   fontproperties='Times New Roman', size=14)
#     if 0.001 < p < 0.01:
#         ax22.text(shortNameMap[pro], r + 0.05, s='**', rotation=90,
#                   fontproperties='Times New Roman', size=14)
#     if p < 0.001:
#         ax22.text(shortNameMap[pro], r + 0.05, s='***',
#                   rotation=90, fontproperties='Times New Roman', size=14)
# plt.yticks(fontproperties='Times New Roman', size=14)
# plt.xticks(fontproperties='Times New Roman', size=14)
# plt.xlabel('Province', font)
# plt.ylabel('Correlation coefficient', font)

# ax3 = plt.axes(rect3)

# model = LinearRegression()
# X = laData['Total'].values.reshape(-1, 1)
# Y = filmData['Total'].values.reshape(-1, 1)
# model.fit(X, Y)
# X2 = [[12], [22]]
# y2 = model.predict(X2)
# plt.plot(X2, y2, color='r', linewidth=2, linestyle='--')
# SStot = np.sum((Y - np.mean(Y)) ** 2)
# SSres = np.sum((Y - model.predict(X)) ** 2)
# compR2 = format(1 - SSres / SStot, '.2f')
# r, p = pearsonr(laData['Total'], filmData['Total'])
# print(r, p, compR2)
# prInfo = '$\mathbf{\mathit{r}}$ =' + '%.3f' % r + '\n$\mathbf{\mathit{p}}$<0.001'
# ax3.text(10.5, 63.8, s=prInfo, fontproperties='Times New Roman', size=16)

# ax3.scatter(laData['Total'], filmData['Total'], marker='o',
#             color='#1F78B4', s=70, alpha=0.8, edgecolors='k', linewidths=0)

# plt.yticks(fontproperties='Times New Roman', size=14)
# plt.xticks(fontproperties='Times New Roman', size=14)
# plt.xlim((10, 24))
# plt.ylim((25, 70))
# plt.xlabel('Leaf area of agricultural lands ($\mathregular{10^4}$ $\mathregular{km^2}$)', font)
# plt.ylabel('Plastic mulch film usage ($\mathregular{10^3}$ t)', font)

# ax33 = plt.axes(rect33)
# plt.ylim((0, 1.2))
# for pro in provinceList:
#     r, p = pearsonr(laData[pro], filmData[pro])
#     if pd.isnull(p):
#         r = 0
#         p = 99
#         ax33.text(shortNameMap[pro], 0.1, s='Data not available',
#                   rotation=90, fontproperties='Times New Roman', size=12)
#     ax33.bar(shortNameMap[pro], r, color=ColormapList[pro], width=0.5)
#     if 0.01 < p < 0.05:
#         ax33.text(shortNameMap[pro], r + 0.05, s='*', rotation=90,
#                   fontproperties='Times New Roman', size=14)
#     if 0.001 < p < 0.01:
#         ax33.text(shortNameMap[pro], r + 0.05, s='**', rotation=90,
#                   fontproperties='Times New Roman', size=14)
#     if p < 0.001:
#         ax33.text(shortNameMap[pro], r + 0.05, s='***',
#                   rotation=90, fontproperties='Times New Roman', size=14)
# plt.yticks(fontproperties='Times New Roman', size=14)
# plt.xticks(fontproperties='Times New Roman', size=14)
# plt.xlabel('Province', font)
# plt.ylabel('Correlation coefficient', font)

# ax0.spines['bottom'].set_linewidth(1.5)
# ax0.spines['left'].set_linewidth(1.5)
# ax0.spines['top'].set_linewidth(1.5)
# ax0.spines['right'].set_linewidth(1.5)

# ax1.spines['bottom'].set_linewidth(1.5)
# ax1.spines['left'].set_linewidth(1.5)
# ax1.spines['top'].set_linewidth(1.5)
# ax1.spines['right'].set_linewidth(1.5)

# ax11.spines['bottom'].set_linewidth(1.5)
# ax11.spines['left'].set_linewidth(1.5)
# ax11.spines['top'].set_linewidth(1.5)
# ax11.spines['right'].set_linewidth(1.5)

# ax2.spines['bottom'].set_linewidth(1.5)
# ax2.spines['left'].set_linewidth(1.5)
# ax2.spines['top'].set_linewidth(1.5)
# ax2.spines['right'].set_linewidth(1.5)

# ax22.spines['bottom'].set_linewidth(1.5)
# ax22.spines['left'].set_linewidth(1.5)
# ax22.spines['top'].set_linewidth(1.5)
# ax22.spines['right'].set_linewidth(1.5)

# ax3.spines['bottom'].set_linewidth(1.5)
# ax3.spines['left'].set_linewidth(1.5)
# ax3.spines['top'].set_linewidth(1.5)
# ax3.spines['right'].set_linewidth(1.5)

# ax33.spines['bottom'].set_linewidth(1.5)
# ax33.spines['left'].set_linewidth(1.5)
# ax33.spines['top'].set_linewidth(1.5)
# ax33.spines['right'].set_linewidth(1.5)

plt.savefig(path + '\\UrbanizationPlot.png', dpi=300, bbox_inches='tight')
