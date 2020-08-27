# -*- coding: utf-8 -*-
# @Time    : 2020/4/24 21:07
# @Author  : THRILLER柠檬
# @Email   : thrillerlemon@outlook.com
# @File    : FIG-StaForGEELC-LP.py
# @Software: PyCharm

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

path = 'D:\\OneDrive\\SharedFile\\GEE_V2\\StaForGEELC\\'

gpData = pd.read_excel(path + '\\LPsta.xlsx', sheet_name="粮食产量", index_col='Year')
# 10^4t
gpData = gpData / 1e6

incomeData = pd.read_excel(path + '\\农村居民人均纯收入.xlsx', sheet_name="Sheet4", index_col='Year')
# Annual per Capita Net Income of Rural Households yuan
incomeData = incomeData / 1000

laData = pd.read_excel(path + '\\LPsta.xlsx', sheet_name="LA", index_col='Year')
# 10^4km^2
laData = laData / 1e10
fertilizerData = pd.read_excel(
    path + '\\LPsta.xlsx', sheet_name="化肥使用量(折纯量)(吨)", index_col='Year')
# 10^4t
fertilizerData = fertilizerData / 10000
machineryData = pd.read_excel(
    path + '\\LPsta.xlsx', sheet_name="农业机械总动力(万千瓦)", index_col='Year')
# 10^6kw
machineryData = machineryData / 100
filmData = pd.read_excel(
    path + '\\LPsta.xlsx', sheet_name="农用塑料薄膜使用量(吨)", index_col='Year')
# 10^3t
filmData = filmData / 1e3

provinceList = ['Shanxi', 'Shaanxi', 'Gansu',
                'Inner Mongolia', 'Ningxia', 'Henan', 'Qinghai']

shortNameMap = {
    'Shanxi': 'SX',
    'Shaanxi': 'SaX',
    'Gansu': 'GS',
    'Inner Mongolia': 'IM',
    'Ningxia': 'NX',
    'Henan': 'HN',
    'Qinghai': 'QH'
}

ColormapList = {
    'Gansu': '#FCA47F',
    'Henan': '#FCDDD0',
    'Inner Mongolia': '#7C5240',
    'Ningxia': '#E65517',
    'Qinghai': '#7BF4C3',
    'Shanxi': '#2B5444',
    'Shaanxi': '#109C64'
}

fig = plt.figure(figsize=(12, 12), dpi=300)

rect0 = [0, 0.58, 1.03, 0.3]
rect1 = [0, 0.23, 0.3, 0.3]  # [左, 下, 宽, 高] 规定的矩形区域 （全部是0~1之间的数，表示比例）
rect2 = [0.37, 0.23, 0.3, 0.3]
rect3 = [0.73, 0.23, 0.3, 0.3]
rect11 = [0, 0, 0.3, 0.16]
rect22 = [0.37, 0, 0.3, 0.16]
rect33 = [0.73, 0, 0.3, 0.16]

font = {'family': 'Times New Roman',
        'weight': 'normal',
        'size': 14}

ax0 = plt.axes(rect0)
bottom = pd.Series(np.zeros(len(gpData.index)), index=gpData.index)
for sheng in gpData.columns:
    ax0.bar([j for j in list(gpData[sheng].index)], list(gpData[sheng]), 0.6,
            label=str(sheng) + ' (' + shortNameMap[sheng] + ')', color=ColormapList[sheng], bottom=list(bottom))
    bottom = bottom.add(gpData[sheng])
plt.yticks(fontproperties='Times New Roman', size=14)
plt.xticks(fontproperties='Times New Roman', size=14)
ax0.set_ylim(0, 55)
ax0.set_xlim(1985.5, 2015.5)

plt.xlabel('Year', font)
plt.ylabel('Grain production ($\mathregular{10^6}$ t)', font)
plt.legend(loc='upper left', ncol=4, prop={'family': 'Times New Roman', 'size': 14}, frameon=False)

ax000 = ax0.twinx()
ax000.plot(list(incomeData.index), list(incomeData['Income']), color='#2A557F',
           label='Annual per capita net income of rural households', linewidth=2, linestyle='-')
plt.yticks(fontproperties='Times New Roman', size=14)
# plt.xticks(fontproperties='Times New Roman', size=14)
ax000.set_ylim(0, 10)
# ax000.set_xlim(1985.5, 2015.5)

# plt.xlabel('Year', font)
plt.ylabel('Net income (Thousand Yuan)', font)
plt.legend(loc=(0.1, 1.1), ncol=4, prop={'family': 'Times New Roman', 'size': 14}, frameon=False)

ax1 = plt.axes(rect1)

ax1.scatter(laData['Total'], fertilizerData['Total'], marker='o',
            color='#1F78B4', s=70, alpha=0.8, edgecolors='k', linewidths=0)

model = LinearRegression()
X = laData['Total'].values.reshape(-1, 1)
Y = fertilizerData['Total'].values.reshape(-1, 1)
model.fit(X, Y)
X2 = [[12], [22]]
y2 = model.predict(X2)
plt.plot(X2, y2, color='r', linewidth=2, linestyle='--')
SStot = np.sum((Y - np.mean(Y)) ** 2)
SSres = np.sum((Y - model.predict(X)) ** 2)
compR2 = format(1 - SSres / SStot, '.2f')
plt.yticks(fontproperties='Times New Roman', size=14)
plt.xticks(fontproperties='Times New Roman', size=14)
r, p = pearsonr(laData['Total'], fertilizerData['Total'])
print(r, p, compR2)

prInfo = '$\mathbf{\mathit{r}}$ =' + '%.3f' % r + '\n$\mathbf{\mathit{p}}$<0.001'
ax1.text(10.5, 503, s=prInfo, fontproperties='Times New Roman', size=16)

plt.xlim((10, 24))
plt.ylim((200, 550))
plt.xlabel('Leaf area of agricultural lands ($\mathregular{10^4}$ $\mathregular{km^2}$)', font)
plt.ylabel('Chemical fertilizer usage ($\mathregular{10^4}$ t)', font)

ax11 = plt.axes(rect11)
plt.ylim((0, 1.2))
for pro in provinceList:
    r, p = pearsonr(laData[pro], fertilizerData[pro])
    ax11.bar(shortNameMap[pro], r, color=ColormapList[pro], width=0.5)
    if 0.01 < p < 0.05:
        ax11.text(shortNameMap[pro], r + 0.05, s='*', rotation=90,
                  fontproperties='Times New Roman', size=14)
    if 0.001 < p < 0.01:
        ax11.text(shortNameMap[pro], r + 0.05, s='**', rotation=90,
                  fontproperties='Times New Roman', size=14)
    if p < 0.001:
        ax11.text(shortNameMap[pro], r + 0.05, s='***',
                  rotation=90, fontproperties='Times New Roman', size=14)
plt.yticks(fontproperties='Times New Roman', size=14)
plt.xticks(fontproperties='Times New Roman', size=14)
plt.xlabel('Province', font)
plt.ylabel('Correlation coefficient', font)

ax2 = plt.axes(rect2)

ax2.scatter(laData['Total'], machineryData['Total'], marker='o',
            color='#1F78B4', s=70, alpha=0.8, edgecolors='k', linewidths=0)
model = LinearRegression()
X = laData['Total'].values.reshape(-1, 1)
Y = machineryData['Total'].values.reshape(-1, 1)
model.fit(X, Y)
X2 = [[12], [22]]
y2 = model.predict(X2)
plt.plot(X2, y2, color='r', linewidth=2, linestyle='--')
SStot = np.sum((Y - np.mean(Y)) ** 2)
SSres = np.sum((Y - model.predict(X)) ** 2)
compR2 = format(1 - SSres / SStot, '.2f')

r, p = pearsonr(laData['Total'], machineryData['Total'])
print(r, p, compR2)

prInfo = '$\mathbf{\mathit{r}}$ =' + '%.3f' % r + '\n$\mathbf{\mathit{p}}$<0.001'
ax2.text(10.5, 89, s=prInfo, fontproperties='Times New Roman', size=16)

plt.yticks(fontproperties='Times New Roman', size=14)
plt.xticks(fontproperties='Times New Roman', size=14)
plt.xlim((10, 24))
plt.ylim((20, 100))
plt.xlabel('Leaf area of agricultural lands ($\mathregular{10^4}$ $\mathregular{km^2}$)', font)
plt.ylabel('Machinery power ($\mathregular{10^6}$ kilowatts)', font)

ax22 = plt.axes(rect22)
plt.ylim((0, 1.2))
for pro in provinceList:
    r, p = pearsonr(laData[pro], machineryData[pro])
    ax22.bar(shortNameMap[pro], r, color=ColormapList[pro], width=0.5)
    if 0.01 < p < 0.05:
        ax22.text(shortNameMap[pro], r + 0.05, s='*', rotation=90,
                  fontproperties='Times New Roman', size=14)
    if 0.001 < p < 0.01:
        ax22.text(shortNameMap[pro], r + 0.05, s='**', rotation=90,
                  fontproperties='Times New Roman', size=14)
    if p < 0.001:
        ax22.text(shortNameMap[pro], r + 0.05, s='***',
                  rotation=90, fontproperties='Times New Roman', size=14)
plt.yticks(fontproperties='Times New Roman', size=14)
plt.xticks(fontproperties='Times New Roman', size=14)
plt.xlabel('Province', font)
plt.ylabel('Correlation coefficient', font)

ax3 = plt.axes(rect3)

model = LinearRegression()
X = laData['Total'].values.reshape(-1, 1)
Y = filmData['Total'].values.reshape(-1, 1)
model.fit(X, Y)
X2 = [[12], [22]]
y2 = model.predict(X2)
plt.plot(X2, y2, color='r', linewidth=2, linestyle='--')
SStot = np.sum((Y - np.mean(Y)) ** 2)
SSres = np.sum((Y - model.predict(X)) ** 2)
compR2 = format(1 - SSres / SStot, '.2f')
r, p = pearsonr(laData['Total'], filmData['Total'])
print(r, p, compR2)
prInfo = '$\mathbf{\mathit{r}}$ =' + '%.3f' % r + '\n$\mathbf{\mathit{p}}$<0.001'
ax3.text(10.5, 63.8, s=prInfo, fontproperties='Times New Roman', size=16)

ax3.scatter(laData['Total'], filmData['Total'], marker='o',
            color='#1F78B4', s=70, alpha=0.8, edgecolors='k', linewidths=0)

plt.yticks(fontproperties='Times New Roman', size=14)
plt.xticks(fontproperties='Times New Roman', size=14)
plt.xlim((10, 24))
plt.ylim((25, 70))
plt.xlabel('Leaf area of agricultural lands ($\mathregular{10^4}$ $\mathregular{km^2}$)', font)
plt.ylabel('Plastic mulch film usage ($\mathregular{10^3}$ t)', font)

ax33 = plt.axes(rect33)
plt.ylim((0, 1.2))
for pro in provinceList:
    r, p = pearsonr(laData[pro], filmData[pro])
    if pd.isnull(p):
        r = 0
        p = 99
        ax33.text(shortNameMap[pro], 0.1, s='Data not available',
                  rotation=90, fontproperties='Times New Roman', size=12)
    ax33.bar(shortNameMap[pro], r, color=ColormapList[pro], width=0.5)
    if 0.01 < p < 0.05:
        ax33.text(shortNameMap[pro], r + 0.05, s='*', rotation=90,
                  fontproperties='Times New Roman', size=14)
    if 0.001 < p < 0.01:
        ax33.text(shortNameMap[pro], r + 0.05, s='**', rotation=90,
                  fontproperties='Times New Roman', size=14)
    if p < 0.001:
        ax33.text(shortNameMap[pro], r + 0.05, s='***',
                  rotation=90, fontproperties='Times New Roman', size=14)
plt.yticks(fontproperties='Times New Roman', size=14)
plt.xticks(fontproperties='Times New Roman', size=14)
plt.xlabel('Province', font)
plt.ylabel('Correlation coefficient', font)

ax0.spines['bottom'].set_linewidth(1.5)
ax0.spines['left'].set_linewidth(1.5)
ax0.spines['top'].set_linewidth(1.5)
ax0.spines['right'].set_linewidth(1.5)

ax1.spines['bottom'].set_linewidth(1.5)
ax1.spines['left'].set_linewidth(1.5)
ax1.spines['top'].set_linewidth(1.5)
ax1.spines['right'].set_linewidth(1.5)

ax11.spines['bottom'].set_linewidth(1.5)
ax11.spines['left'].set_linewidth(1.5)
ax11.spines['top'].set_linewidth(1.5)
ax11.spines['right'].set_linewidth(1.5)

ax2.spines['bottom'].set_linewidth(1.5)
ax2.spines['left'].set_linewidth(1.5)
ax2.spines['top'].set_linewidth(1.5)
ax2.spines['right'].set_linewidth(1.5)

ax22.spines['bottom'].set_linewidth(1.5)
ax22.spines['left'].set_linewidth(1.5)
ax22.spines['top'].set_linewidth(1.5)
ax22.spines['right'].set_linewidth(1.5)

ax3.spines['bottom'].set_linewidth(1.5)
ax3.spines['left'].set_linewidth(1.5)
ax3.spines['top'].set_linewidth(1.5)
ax3.spines['right'].set_linewidth(1.5)

ax33.spines['bottom'].set_linewidth(1.5)
ax33.spines['left'].set_linewidth(1.5)
ax33.spines['top'].set_linewidth(1.5)
ax33.spines['right'].set_linewidth(1.5)

plt.savefig(path + '\\StaForGEELC-AddIncome.png', dpi=300, bbox_inches='tight')
