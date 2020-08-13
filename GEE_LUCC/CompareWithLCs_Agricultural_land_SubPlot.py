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
    'D:\OneDrive\SharedFile\GEE_V2\CompareWithLCs\CompareWithLCs_Agricultural_land\耕地面积_单位-平方米.xlsx',
    sheet_name="pingfangmi")


def FindValue(pCountryCode, pYear):
    findresult = allCountryTrueData[
        (allCountryTrueData["County_code_N"] == int(pCountryCode))
    ].copy()
    return findresult[pYear].iloc[0]


dfOut = pd.DataFrame(columns=['TrueArea', 'DataArea', 'DataSet', 'CountryCode', 'Year'])

csvPath = 'D:\\OneDrive\\SharedFile\\GEE_V2\\CompareWithLCs\\CompareWithLCs_Agricultural_land\\csv\\'

fig = plt.figure(figsize=(20, 10), dpi=300)

ax0 = fig.add_subplot(2, 4, 1)
# ThisStudy1990-2014
for year in np.arange(1990, 2015, 1):
    dataCSV = pd.read_csv(csvPath + 'KindArea_Agricultural_land_ThisStudy' + str(year) + '.csv')
    for tIndex, tRow in dataCSV.iterrows():
        countryCode = tRow["County_c_1"]
        dataArea = tRow["sum"]
        findedvalue = FindValue(countryCode, year)
        dic = {'TrueArea': findedvalue / 100000000,
               'DataArea': dataArea / 100000000,
               'DataSet': 'This Study',
               'CountryCode': countryCode,
               'Year': year,
               }
        dfOut = dfOut.append(dic, ignore_index=True)
dfOut = dfOut[(dfOut["TrueArea"] > 1) & (dfOut["TrueArea"] < 50) & (dfOut["DataArea"] > 1) & (dfOut["DataArea"] < 50)]
# thisDS=dfOut[dfOut['DataSet']=='This Study']
# print('This Study')
# print(f"均方误差(MSE)：{mean_squared_error(thisDS['TrueArea'],thisDS['DataArea'])}")
# print(f"根均方误差(RMSE)：{np.sqrt(mean_squared_error(thisDS['TrueArea'],thisDS['DataArea']))}")
# print(f"测试集R^2：{r2_score(thisDS['TrueArea'], thisDS['DataArea'])}")
#
# model=LinearRegression()
# X = thisDS['TrueArea'].values.reshape(-1,1)
# Y = thisDS['DataArea'].values.reshape(-1,1)
# model.fit(X,Y)
# X2 = [[0], [10], [25], [40]]
# y2 = model.predict(X2)
# plt.plot(X2, y2, color='b', linewidth=2, linestyle='--')
# SStot = np.sum((Y-np.mean(Y))**2)
# SSres = np.sum((Y-model.predict(X))**2)
# print("SStot=",SStot)
# print("SSres=",SSres)
# print("R2=", 1-SSres/SStot)
# # print("model score=", model.score(X, Y))
# # # X2 = sm.add_constant(X)
# # # est = sm.OLS(Y, X2)
# # # est2 = est.fit()
# # # print(est2.summary())
#
# plt.scatter(thisDS['TrueArea'], thisDS['DataArea'], marker='^', color='b', s=45,alpha=0.8,label='This Study',edgecolors='k')
# ax0.set_xlabel('Area in Statistical Data($\mathregular{10^4hm^2}$)', fontdict={'family' : 'Times New Roman', 'size'   : 13})
# ax0.set_ylabel('Area in Dataset($\mathregular{10^4hm^2}$)', fontdict={'family' : 'Times New Roman', 'size'   : 13})
# ax0.spines['right'].set_color('none')
# ax0.spines['top'].set_color('none')
# plt.xlim((0, 50))
# plt.ylim((0, 50))
# plt.yticks(fontproperties = 'Times New Roman', size = 10)
# plt.xticks(fontproperties = 'Times New Roman', size = 10)
# plt.legend(frameon=False,borderpad=0.3,handletextpad=0.2,markerfirst=False,prop={'family' : 'Times New Roman', 'size'   :14})
# plt.text(35,42,"$\mathregular{R^2}$: "+str(format(1-SSres/SStot, '.2f')),family='Times New Roman', size=14)
# plt.text(30,39,"RMSE: "+str(format(np.sqrt(mean_squared_error(thisDS['TrueArea'],thisDS['DataArea'])), '.2f')),family='Times New Roman', size=14)
#
#
ax1 = fig.add_subplot(2, 4, 1)
# GLASS_GLC1990-2014
print('GLASS-GLC')
startY = 1990
endY = 2015
for year in np.arange(startY, endY, 1):
    dataCSV = pd.read_csv(csvPath + 'KindArea_Agricultural_land_GLASS_GLC' + str(year) + '.csv')
    for tIndex, tRow in dataCSV.iterrows():
        countryCode = tRow["County_c_1"]
        dataArea = tRow["sum"]
        findedvalue = FindValue(countryCode, year)
        dic = {'TrueArea': findedvalue / 100000000,
               'DataArea': dataArea / 100000000,
               'DataSet': 'GLASS-GLC',
               'CountryCode': countryCode,
               'Year': year,
               }
        dfOut = dfOut.append(dic, ignore_index=True)
dfOut = dfOut[(dfOut["TrueArea"] > 1) & (dfOut["TrueArea"] < 50) & (dfOut["DataArea"] > 1) & (dfOut["DataArea"] < 50)]

# do this study1990-2014
myDS = dfOut[(dfOut['DataSet'] == 'This Study') & (dfOut['Year'] <= endY) & (dfOut['Year'] >= startY)]
model = LinearRegression()
X = myDS['TrueArea'].values.reshape(-1, 1)
Y = myDS['DataArea'].values.reshape(-1, 1)
model.fit(X, Y)
X2 = [[0], [10], [25], [40]]
y2 = model.predict(X2)
plt.plot(X2, y2, color='b', linewidth=2, linestyle='--')
SStot = np.sum((Y - np.mean(Y)) ** 2)
SSres = np.sum((Y - model.predict(X)) ** 2)
thisRMSE = format(np.sqrt(mean_squared_error(myDS['TrueArea'], myDS['DataArea'])), '.2f')
thisR2 = format(1 - SSres / SStot, '.2f')
plt.scatter(myDS['TrueArea'], myDS['DataArea'], marker='^', color='b', s=45, alpha=0.5, label='This Study',
            edgecolors='k', linewidths=0.5)
# -----


# do GLASS_GLC-1990-2014
thisDS = dfOut[dfOut['DataSet'] == 'GLASS-GLC']
model = LinearRegression()
X = thisDS['TrueArea'].values.reshape(-1, 1)
Y = thisDS['DataArea'].values.reshape(-1, 1)
model.fit(X, Y)
X2 = [[0], [10], [25], [40]]
y2 = model.predict(X2)
plt.plot(X2, y2, color='tomato', linewidth=2, linestyle='--')
SStot = np.sum((Y - np.mean(Y)) ** 2)
SSres = np.sum((Y - model.predict(X)) ** 2)
compRMSE = format(np.sqrt(mean_squared_error(thisDS['TrueArea'], thisDS['DataArea'])), '.2f')
compR2 = format(1 - SSres / SStot, '.2f')
plt.scatter(thisDS['TrueArea'], thisDS['DataArea'], marker='1', color='tomato', s=45, alpha=0.5, label='GLASS-GLC',
            edgecolors='k', linewidths=0.5)

ax1.set_xlabel('Area in Statistical Data($\mathregular{10^4hm^2}$)', fontdict={'family': 'Times New Roman', 'size': 13})
ax1.set_ylabel('Area in Dataset($\mathregular{10^4hm^2}$)', fontdict={'family': 'Times New Roman', 'size': 13})
ax1.spines['right'].set_color('none')
ax1.spines['top'].set_color('none')
plt.xlim((0, 50))
plt.ylim((0, 50))
plt.yticks(fontproperties='Times New Roman', size=10)
plt.xticks(fontproperties='Times New Roman', size=10)
# plt.legend(loc=4,frameon=False,borderpad=0.3,handletextpad=0.2,markerfirst=False,prop={'family' : 'Times New Roman', 'size'   :12})
plt.text(50, 49, "Period:1990-2014" + str(), family='Times New Roman', size=12, horizontalalignment='right',
         verticalalignment='center')
plt.text(50, 46, "This Study $\mathregular{R^2}$: " + str(thisR2), family='Times New Roman', size=12,
         horizontalalignment='right', verticalalignment='center')
plt.text(50, 43, "This Study RMSE: " + str(thisRMSE), family='Times New Roman', size=12, horizontalalignment='right',
         verticalalignment='center')
plt.text(50, 40, "GLASS-GLC $\mathregular{R^2}$: " + str(compR2), family='Times New Roman', size=12,
         horizontalalignment='right', verticalalignment='center')
plt.text(50, 37, "GLASS-GLC RMSE: " + str(compRMSE), family='Times New Roman', size=12, horizontalalignment='right',
         verticalalignment='center')

ax2 = fig.add_subplot(2, 4, 2)
# Modis2001-2014
print('MCD12Q1-V6')
startY = 2001
endY = 2015
for year in np.arange(startY, endY, 1):
    dataCSV = pd.read_csv(csvPath + 'KindArea_Agricultural_land_LC_' + str(year) + 'MODIS_500.csv')
    for tIndex, tRow in dataCSV.iterrows():
        countryCode = tRow["County_c_1"]
        dataArea = tRow["sum"]
        findedvalue = FindValue(countryCode, year)
        dic = {'TrueArea': findedvalue / 100000000,
               'DataArea': dataArea / 100000000,
               'DataSet': 'MCD12Q1-V6',
               'CountryCode': countryCode,
               'Year': year,
               }
        dfOut = dfOut.append(dic, ignore_index=True)
dfOut = dfOut[(dfOut["TrueArea"] > 1) & (dfOut["TrueArea"] < 50) & (dfOut["DataArea"] > 1) & (dfOut["DataArea"] < 50)]

# do this study2001-2014
myDS = dfOut[(dfOut['DataSet'] == 'This Study') & (dfOut['Year'] <= endY) & (dfOut['Year'] >= startY)]
model = LinearRegression()
X = myDS['TrueArea'].values.reshape(-1, 1)
Y = myDS['DataArea'].values.reshape(-1, 1)
model.fit(X, Y)
X2 = [[0], [10], [25], [40]]
y2 = model.predict(X2)
plt.plot(X2, y2, color='b', linewidth=2, linestyle='--')
SStot = np.sum((Y - np.mean(Y)) ** 2)
SSres = np.sum((Y - model.predict(X)) ** 2)
thisRMSE = format(np.sqrt(mean_squared_error(myDS['TrueArea'], myDS['DataArea'])), '.2f')
thisR2 = format(1 - SSres / SStot, '.2f')
plt.scatter(myDS['TrueArea'], myDS['DataArea'], marker='^', color='b', s=45, alpha=0.5, label='This Study',
            edgecolors='k', linewidths=0.5)
# -----


# do modis2001-2014
thisDS = dfOut[dfOut['DataSet'] == 'MCD12Q1-V6']
model = LinearRegression()
X = thisDS['TrueArea'].values.reshape(-1, 1)
Y = thisDS['DataArea'].values.reshape(-1, 1)
model.fit(X, Y)
X2 = [[0], [10], [25], [40]]
y2 = model.predict(X2)
plt.plot(X2, y2, color='g', linewidth=2, linestyle='--')
SStot = np.sum((Y - np.mean(Y)) ** 2)
SSres = np.sum((Y - model.predict(X)) ** 2)
compRMSE = format(np.sqrt(mean_squared_error(thisDS['TrueArea'], thisDS['DataArea'])), '.2f')
compR2 = format(1 - SSres / SStot, '.2f')
plt.scatter(thisDS['TrueArea'], thisDS['DataArea'], marker='o', color='g', s=45, alpha=0.5, label='MCD12Q1-V6',
            edgecolors='k', linewidths=0.5)

ax2.set_xlabel('Area in Statistical Data($\mathregular{10^4hm^2}$)', fontdict={'family': 'Times New Roman', 'size': 13})
ax2.set_ylabel('Area in Dataset($\mathregular{10^4hm^2}$)', fontdict={'family': 'Times New Roman', 'size': 13})
ax2.spines['right'].set_color('none')
ax2.spines['top'].set_color('none')
plt.xlim((0, 50))
plt.ylim((0, 50))
plt.yticks(fontproperties='Times New Roman', size=10)
plt.xticks(fontproperties='Times New Roman', size=10)
# plt.legend(loc=4,frameon=False,borderpad=0.3,handletextpad=0.2,markerfirst=False,prop={'family' : 'Times New Roman', 'size'   :12})

plt.text(50, 49, "Period:2001-2014" + str(), family='Times New Roman', size=12, horizontalalignment='right',
         verticalalignment='center')
plt.text(50, 46, "This Study $\mathregular{R^2}$: " + str(thisR2), family='Times New Roman', size=12,
         horizontalalignment='right', verticalalignment='center')
plt.text(50, 43, "This Study RMSE: " + str(thisRMSE), family='Times New Roman', size=12, horizontalalignment='right',
         verticalalignment='center')
plt.text(50, 40, "MCD12Q1-V6 $\mathregular{R^2}$: " + str(compR2), family='Times New Roman', size=12,
         horizontalalignment='right', verticalalignment='center')
plt.text(50, 37, "MCD12Q1-V6 RMSE: " + str(compRMSE), family='Times New Roman', size=12, horizontalalignment='right',
         verticalalignment='center')

ax3 = fig.add_subplot(2, 4, 3)
# LJY1995\2000\2005
print('ChinaLC1000')
for year in [1995, 2000, 2005]:
    dataCSV = pd.read_csv(csvPath + 'KindArea_Agricultural_land_LC_' + str(year) + 'LJY_1000.csv')
    for tIndex, tRow in dataCSV.iterrows():
        countryCode = tRow["County_c_1"]
        dataArea = tRow["sum"]
        findedvalue = FindValue(countryCode, year)
        dic = {'TrueArea': findedvalue / 100000000,
               'DataArea': dataArea / 100000000,
               'DataSet': 'ChinaLC1000',
               'CountryCode': countryCode,
               'Year': year,
               }
        dfOut = dfOut.append(dic, ignore_index=True)
dfOut = dfOut[(dfOut["TrueArea"] > 1) & (dfOut["TrueArea"] < 50) & (dfOut["DataArea"] > 1) & (dfOut["DataArea"] < 50)]

# do this study1995\2000\2005
myDS = dfOut[(dfOut['DataSet'] == 'This Study') & (dfOut['Year'].isin([1995, 2000, 2005]))]
model = LinearRegression()
X = myDS['TrueArea'].values.reshape(-1, 1)
Y = myDS['DataArea'].values.reshape(-1, 1)
model.fit(X, Y)
X2 = [[0], [10], [25], [40]]
y2 = model.predict(X2)
plt.plot(X2, y2, color='b', linewidth=2, linestyle='--')
SStot = np.sum((Y - np.mean(Y)) ** 2)
SSres = np.sum((Y - model.predict(X)) ** 2)
thisRMSE = format(np.sqrt(mean_squared_error(myDS['TrueArea'], myDS['DataArea'])), '.2f')
thisR2 = format(1 - SSres / SStot, '.2f')
plt.scatter(myDS['TrueArea'], myDS['DataArea'], marker='^', color='b', s=45, alpha=0.5, label='This Study',
            edgecolors='k', linewidths=0.5)
# -----


# do LJY1995\2000\2005
thisDS = dfOut[dfOut['DataSet'] == 'ChinaLC1000']
model = LinearRegression()
X = thisDS['TrueArea'].values.reshape(-1, 1)
Y = thisDS['DataArea'].values.reshape(-1, 1)
model.fit(X, Y)
X2 = [[0], [10], [25], [25]]
y2 = model.predict(X2)
plt.plot(X2, y2, color='r', linewidth=2, linestyle='--')
SStot = np.sum((Y - np.mean(Y)) ** 2)
SSres = np.sum((Y - model.predict(X)) ** 2)
compRMSE = format(np.sqrt(mean_squared_error(thisDS['TrueArea'], thisDS['DataArea'])), '.2f')
compR2 = format(1 - SSres / SStot, '.2f')
plt.scatter(thisDS['TrueArea'], thisDS['DataArea'], marker='x', color='r', s=45, alpha=0.5, label='ChinaLC1000',
            edgecolors='k', linewidths=0.5)

ax3.set_xlabel('Area in Statistical Data($\mathregular{10^4hm^2}$)', fontdict={'family': 'Times New Roman', 'size': 13})
ax3.set_ylabel('Area in Dataset($\mathregular{10^4hm^2}$)', fontdict={'family': 'Times New Roman', 'size': 13})
ax3.spines['right'].set_color('none')
ax3.spines['top'].set_color('none')
plt.xlim((0, 50))
plt.ylim((0, 50))
plt.yticks(fontproperties='Times New Roman', size=10)
plt.xticks(fontproperties='Times New Roman', size=10)
# plt.legend(loc=4,frameon=False,borderpad=0.3,handletextpad=0.2,markerfirst=False,prop={'family' : 'Times New Roman', 'size'   :12})
plt.text(50, 49, "Period:1995,2000,2005" + str(), family='Times New Roman', size=12, horizontalalignment='right',
         verticalalignment='center')
plt.text(50, 46, "This Study $\mathregular{R^2}$: " + str(thisR2), family='Times New Roman', size=12,
         horizontalalignment='right', verticalalignment='center')
plt.text(50, 43, "This Study RMSE: " + str(thisRMSE), family='Times New Roman', size=12, horizontalalignment='right',
         verticalalignment='center')
plt.text(50, 40, "ChinaLC1000 $\mathregular{R^2}$: " + str(compR2), family='Times New Roman', size=12,
         horizontalalignment='right', verticalalignment='center')
plt.text(50, 37, "ChinaLC1000 RMSE: " + str(compRMSE), family='Times New Roman', size=12, horizontalalignment='right',
         verticalalignment='center')

ax4 = fig.add_subplot(2, 4, 4)
# GlobalLandCover30 2000   2010
print('GlobeLand30')
for year in [2000, 2010]:
    dataCSV = pd.read_csv(csvPath + 'KindArea_Agricultural_land_LC_' + str(year) + 'GlobalLandCover30_30.csv')
    for tIndex, tRow in dataCSV.iterrows():
        countryCode = tRow["County_c_1"]
        dataArea = tRow["sum"]
        findedvalue = FindValue(countryCode, year)
        dic = {'TrueArea': findedvalue / 100000000,
               'DataArea': dataArea / 100000000,
               'DataSet': 'GlobeLand30',
               'CountryCode': countryCode,
               'Year': year,
               }
        dfOut = dfOut.append(dic, ignore_index=True)
dfOut = dfOut[(dfOut["TrueArea"] > 1) & (dfOut["TrueArea"] < 50) & (dfOut["DataArea"] > 1) & (dfOut["DataArea"] < 50)]

# do this study2000\2010
myDS = dfOut[(dfOut['DataSet'] == 'This Study') & (dfOut['Year'].isin([2000, 2010]))]
model = LinearRegression()
X = myDS['TrueArea'].values.reshape(-1, 1)
Y = myDS['DataArea'].values.reshape(-1, 1)
model.fit(X, Y)
X2 = [[0], [10], [25], [40]]
y2 = model.predict(X2)
plt.plot(X2, y2, color='b', linewidth=2, linestyle='--')
SStot = np.sum((Y - np.mean(Y)) ** 2)
SSres = np.sum((Y - model.predict(X)) ** 2)
thisRMSE = format(np.sqrt(mean_squared_error(myDS['TrueArea'], myDS['DataArea'])), '.2f')
thisR2 = format(1 - SSres / SStot, '.2f')
plt.scatter(myDS['TrueArea'], myDS['DataArea'], marker='^', color='b', s=45, alpha=0.5, label='This Study',
            edgecolors='k', linewidths=0.5)
# -----

# do GlobeLand30 2000\2010
thisDS = dfOut[dfOut['DataSet'] == 'GlobeLand30']
model = LinearRegression()
X = thisDS['TrueArea'].values.reshape(-1, 1)
Y = thisDS['DataArea'].values.reshape(-1, 1)
model.fit(X, Y)
X2 = [[0], [10], [22]]
y2 = model.predict(X2)
plt.plot(X2, y2, color='c', linewidth=2, linestyle='--')
SStot = np.sum((Y - np.mean(Y)) ** 2)
SSres = np.sum((Y - model.predict(X)) ** 2)
compRMSE = format(np.sqrt(mean_squared_error(thisDS['TrueArea'], thisDS['DataArea'])), '.2f')
compR2 = format(1 - SSres / SStot, '.2f')
plt.scatter(thisDS['TrueArea'], thisDS['DataArea'], marker='v', color='c', s=45, alpha=0.5, label='GlobeLand30',
            edgecolors='k', linewidths=0.5)

ax4.set_xlabel('Area in Statistical Data($\mathregular{10^4hm^2}$)', fontdict={'family': 'Times New Roman', 'size': 13})
ax4.set_ylabel('Area in Dataset($\mathregular{10^4hm^2}$)', fontdict={'family': 'Times New Roman', 'size': 13})
ax4.spines['right'].set_color('none')
ax4.spines['top'].set_color('none')
plt.xlim((0, 50))
plt.ylim((0, 50))
plt.yticks(fontproperties='Times New Roman', size=10)
plt.xticks(fontproperties='Times New Roman', size=10)
# plt.legend(loc=4,frameon=False,borderpad=0.3,handletextpad=0.2,markerfirst=False,prop={'family' : 'Times New Roman', 'size'   :12})
plt.text(50, 49, "Period:2000,2010" + str(), family='Times New Roman', size=12, horizontalalignment='right',
         verticalalignment='center')
plt.text(50, 46, "This Study $\mathregular{R^2}$: " + str(thisR2), family='Times New Roman', size=12,
         horizontalalignment='right', verticalalignment='center')
plt.text(50, 43, "This Study RMSE: " + str(thisRMSE), family='Times New Roman', size=12, horizontalalignment='right',
         verticalalignment='center')
plt.text(50, 40, "GlobeLand30 $\mathregular{R^2}$: " + str(compR2), family='Times New Roman', size=12,
         horizontalalignment='right', verticalalignment='center')
plt.text(50, 37, "GlobeLand30 RMSE: " + str(compRMSE), family='Times New Roman', size=12, horizontalalignment='right',
         verticalalignment='center')

ax5 = fig.add_subplot(2, 4, 5)
# GlobCover 2005 2009
print('GlobCover')
for year in [2005, 2009]:
    dataCSV = pd.read_csv(csvPath + 'KindArea_Agricultural_land_LC_' + str(year) + 'GlobCover_300.csv')
    for tIndex, tRow in dataCSV.iterrows():
        countryCode = tRow["County_c_1"]
        dataArea = tRow["sum"]
        findedvalue = FindValue(countryCode, year)
        dic = {'TrueArea': findedvalue / 100000000,
               'DataArea': dataArea / 100000000,
               'DataSet': 'GlobCover',
               'CountryCode': countryCode,
               'Year': year,
               }
        dfOut = dfOut.append(dic, ignore_index=True)
dfOut = dfOut[(dfOut["TrueArea"] > 1) & (dfOut["TrueArea"] < 50) & (dfOut["DataArea"] > 1) & (dfOut["DataArea"] < 50)]

# do this study 2005 2009
myDS = dfOut[(dfOut['DataSet'] == 'This Study') & (dfOut['Year'].isin([2005, 2009]))]
model = LinearRegression()
X = myDS['TrueArea'].values.reshape(-1, 1)
Y = myDS['DataArea'].values.reshape(-1, 1)
model.fit(X, Y)
X2 = [[0], [10], [25], [40]]
y2 = model.predict(X2)
plt.plot(X2, y2, color='b', linewidth=2, linestyle='--')
SStot = np.sum((Y - np.mean(Y)) ** 2)
SSres = np.sum((Y - model.predict(X)) ** 2)
thisRMSE = format(np.sqrt(mean_squared_error(myDS['TrueArea'], myDS['DataArea'])), '.2f')
thisR2 = format(1 - SSres / SStot, '.2f')
plt.scatter(myDS['TrueArea'], myDS['DataArea'], marker='^', color='b', s=45, alpha=0.5, label='This Study',
            edgecolors='k', linewidths=0.5)
# -----

# do GlobCover\2005\2009
thisDS = dfOut[dfOut['DataSet'] == 'GlobCover']
model = LinearRegression()
X = thisDS['TrueArea'].values.reshape(-1, 1)
Y = thisDS['DataArea'].values.reshape(-1, 1)
model.fit(X, Y)
X2 = [[0], [10], [25], [40]]
y2 = model.predict(X2)
plt.plot(X2, y2, color='y', linewidth=2, linestyle='--')
SStot = np.sum((Y - np.mean(Y)) ** 2)
SSres = np.sum((Y - model.predict(X)) ** 2)
compRMSE = format(np.sqrt(mean_squared_error(thisDS['TrueArea'], thisDS['DataArea'])), '.2f')
compR2 = format(1 - SSres / SStot, '.2f')
plt.scatter(thisDS['TrueArea'], thisDS['DataArea'], marker='s', color='y', s=45, alpha=0.5, label='GlobCover',
            edgecolors='k', linewidths=0.5)

ax5.set_xlabel('Area in Statistical Data($\mathregular{10^4hm^2}$)', fontdict={'family': 'Times New Roman', 'size': 13})
ax5.set_ylabel('Area in Dataset($\mathregular{10^4hm^2}$)', fontdict={'family': 'Times New Roman', 'size': 13})
ax5.spines['right'].set_color('none')
ax5.spines['top'].set_color('none')
plt.xlim((0, 50))
plt.ylim((0, 50))
plt.yticks(fontproperties='Times New Roman', size=10)
plt.xticks(fontproperties='Times New Roman', size=10)
# plt.legend(loc=4,frameon=False,borderpad=0.3,handletextpad=0.2,markerfirst=False,prop={'family' : 'Times New Roman', 'size'   :12})
plt.text(50, 49, "Period:2005,2009" + str(), family='Times New Roman', size=12, horizontalalignment='right',
         verticalalignment='center')
plt.text(50, 46, "This Study $\mathregular{R^2}$: " + str(thisR2), family='Times New Roman', size=12,
         horizontalalignment='right', verticalalignment='center')
plt.text(50, 43, "This Study RMSE: " + str(thisRMSE), family='Times New Roman', size=12, horizontalalignment='right',
         verticalalignment='center')
plt.text(50, 40, "GlobCover $\mathregular{R^2}$: " + str(compR2), family='Times New Roman', size=12,
         horizontalalignment='right', verticalalignment='center')
plt.text(50, 37, "GlobCover RMSE: " + str(compRMSE), family='Times New Roman', size=12, horizontalalignment='right',
         verticalalignment='center')

ax6 = fig.add_subplot(2, 4, 6)
# FROMGLC 2010
print('FROM-GLC')
dataCSV = pd.read_csv(csvPath + 'KindArea_Agricultural_land_LC_2010FROMGLC_30.csv')
for tIndex, tRow in dataCSV.iterrows():
    countryCode = tRow["County_c_1"]
    dataArea = tRow["sum"]
    findedvalue = FindValue(countryCode, year)
    dic = {'TrueArea': findedvalue / 100000000,
           'DataArea': dataArea / 100000000,
           'DataSet': 'FROM-GLC',
           'CountryCode': countryCode,
           'Year': year,
           }
    dfOut = dfOut.append(dic, ignore_index=True)
dfOut = dfOut[(dfOut["TrueArea"] > 1) & (dfOut["TrueArea"] < 50) & (dfOut["DataArea"] > 1) & (dfOut["DataArea"] < 50)]

# do this study2010
myDS = dfOut[(dfOut['DataSet'] == 'This Study') & (dfOut['Year'] == 2010)]
model = LinearRegression()
X = myDS['TrueArea'].values.reshape(-1, 1)
Y = myDS['DataArea'].values.reshape(-1, 1)
model.fit(X, Y)
X2 = [[0], [10], [25], [40]]
y2 = model.predict(X2)
plt.plot(X2, y2, color='b', linewidth=2, linestyle='--')
SStot = np.sum((Y - np.mean(Y)) ** 2)
SSres = np.sum((Y - model.predict(X)) ** 2)
thisRMSE = format(np.sqrt(mean_squared_error(myDS['TrueArea'], myDS['DataArea'])), '.2f')
thisR2 = format(1 - SSres / SStot, '.2f')
plt.scatter(myDS['TrueArea'], myDS['DataArea'], marker='^', color='b', s=45, alpha=0.5, label='This Study',
            edgecolors='k', linewidths=0.5)
# -----


thisDS = dfOut[dfOut['DataSet'] == 'FROM-GLC']
model = LinearRegression()
X = thisDS['TrueArea'].values.reshape(-1, 1)
Y = thisDS['DataArea'].values.reshape(-1, 1)
model.fit(X, Y)
X2 = [[0], [10], [20]]
y2 = model.predict(X2)
plt.plot(X2, y2, color='k', linewidth=2, linestyle='--')
SStot = np.sum((Y - np.mean(Y)) ** 2)
SSres = np.sum((Y - model.predict(X)) ** 2)
compRMSE = format(np.sqrt(mean_squared_error(thisDS['TrueArea'], thisDS['DataArea'])), '.2f')
compR2 = format(1 - SSres / SStot, '.2f')
plt.scatter(thisDS['TrueArea'], thisDS['DataArea'], marker='H', color='k', s=40, alpha=0.5, label='FROM-GLC',
            edgecolors='k', linewidths=0.5)

ax6.set_xlabel('Area in Statistical Data($\mathregular{10^4hm^2}$)', fontdict={'family': 'Times New Roman', 'size': 13})
ax6.set_ylabel('Area in Dataset($\mathregular{10^4hm^2}$)', fontdict={'family': 'Times New Roman', 'size': 13})
ax6.spines['right'].set_color('none')
ax6.spines['top'].set_color('none')
plt.xlim((0, 50))
plt.ylim((0, 50))
plt.yticks(fontproperties='Times New Roman', size=10)
plt.xticks(fontproperties='Times New Roman', size=10)
# plt.legend(loc=4,frameon=False,borderpad=0.3,handletextpad=0.2,markerfirst=False,prop={'family' : 'Times New Roman', 'size'   :12})
plt.text(50, 49, "Period:2010" + str(), family='Times New Roman', size=12, horizontalalignment='right',
         verticalalignment='center')
plt.text(50, 46, "This Study $\mathregular{R^2}$: " + str(thisR2), family='Times New Roman', size=12,
         horizontalalignment='right', verticalalignment='center')
plt.text(50, 43, "This Study RMSE: " + str(thisRMSE), family='Times New Roman', size=12, horizontalalignment='right',
         verticalalignment='center')
plt.text(50, 40, "FROM-GLC $\mathregular{R^2}$: " + str(compR2), family='Times New Roman', size=12,
         horizontalalignment='right', verticalalignment='center')
plt.text(50, 37, "FROM-GLC RMSE: " + str(compRMSE), family='Times New Roman', size=12, horizontalalignment='right',
         verticalalignment='center')

ax7 = fig.add_subplot(2, 4, 7)
# GLC 1992
print('GLCC')
dataCSV = pd.read_csv(csvPath + 'KindArea_Agricultural_land_LC_1992GLC_1000.csv')
for tIndex, tRow in dataCSV.iterrows():
    countryCode = tRow["County_c_1"]
    dataArea = tRow["sum"]
    findedvalue = FindValue(countryCode, year)
    dic = {'TrueArea': findedvalue / 100000000,
           'DataArea': dataArea / 100000000,
           'DataSet': 'GLCC',
           'CountryCode': countryCode,
           'Year': year,
           }
    dfOut = dfOut.append(dic, ignore_index=True)
dfOut = dfOut[(dfOut["TrueArea"] > 1) & (dfOut["TrueArea"] < 50) & (dfOut["DataArea"] > 1) & (dfOut["DataArea"] < 50)]

# do this study1992
myDS = dfOut[(dfOut['DataSet'] == 'This Study') & (dfOut['Year'] == 1992)]
model = LinearRegression()
X = myDS['TrueArea'].values.reshape(-1, 1)
Y = myDS['DataArea'].values.reshape(-1, 1)
model.fit(X, Y)
X2 = [[0], [10], [25], [35]]
y2 = model.predict(X2)
plt.plot(X2, y2, color='b', linewidth=2, linestyle='--')
SStot = np.sum((Y - np.mean(Y)) ** 2)
SSres = np.sum((Y - model.predict(X)) ** 2)
thisRMSE = format(np.sqrt(mean_squared_error(myDS['TrueArea'], myDS['DataArea'])), '.2f')
thisR2 = format(1 - SSres / SStot, '.2f')
plt.scatter(myDS['TrueArea'], myDS['DataArea'], marker='^', color='b', s=45, alpha=0.5, label='This Study',
            edgecolors='k', linewidths=0.5)
# -----

thisDS = dfOut[dfOut['DataSet'] == 'GLCC']
model = LinearRegression()
X = thisDS['TrueArea'].values.reshape(-1, 1)
Y = thisDS['DataArea'].values.reshape(-1, 1)
model.fit(X, Y)
X2 = [[0], [10], [25], [40]]
y2 = model.predict(X2)
plt.plot(X2, y2, color='m', linewidth=2, linestyle='--')
SStot = np.sum((Y - np.mean(Y)) ** 2)
SSres = np.sum((Y - model.predict(X)) ** 2)
compRMSE = format(np.sqrt(mean_squared_error(thisDS['TrueArea'], thisDS['DataArea'])), '.2f')
compR2 = format(1 - SSres / SStot, '.2f')
plt.scatter(thisDS['TrueArea'], thisDS['DataArea'], marker='+', color='m', s=45, alpha=0.5, label='GLCC',
            edgecolors='k', linewidths=0.5)

ax7.set_xlabel('Area in Statistical Data($\mathregular{10^4hm^2}$)', fontdict={'family': 'Times New Roman', 'size': 13})
ax7.set_ylabel('Area in Dataset($\mathregular{10^4hm^2}$)', fontdict={'family': 'Times New Roman', 'size': 13})
ax7.spines['right'].set_color('none')
ax7.spines['top'].set_color('none')
plt.xlim((0, 50))
plt.ylim((0, 50))
plt.yticks(fontproperties='Times New Roman', size=10)
plt.xticks(fontproperties='Times New Roman', size=10)
# plt.legend(loc=4,frameon=False,borderpad=0.3,handletextpad=0.2,markerfirst=False,prop={'family' : 'Times New Roman', 'size'   :12})
plt.text(50, 49, "Period:1992" + str(), family='Times New Roman', size=12, horizontalalignment='right',
         verticalalignment='center')
plt.text(50, 46, "This Study $\mathregular{R^2}$: " + str(thisR2), family='Times New Roman', size=12,
         horizontalalignment='right', verticalalignment='center')
plt.text(50, 43, "This Study RMSE: " + str(thisRMSE), family='Times New Roman', size=12, horizontalalignment='right',
         verticalalignment='center')
plt.text(50, 40, "GLCC $\mathregular{R^2}$: " + str(compR2), family='Times New Roman', size=12,
         horizontalalignment='right', verticalalignment='center')
plt.text(50, 37, "GLCC RMSE: " + str(compRMSE), family='Times New Roman', size=12, horizontalalignment='right',
         verticalalignment='center')

# ax.set_title('Agricultural land Area Compare',fontdict={'family' : 'Times New Roman', 'size'   : 20})

plt.savefig(
    'D:\\OneDrive\\SharedFile\\GEE_V2\\CompareWithLCs\\CompareWithLCs_Agricultural_land\\AgrSat_Sub_scatter.png',
    dpi=300, bbox_inches='tight')
# plt.show()
dfOut.to_csv(
    'D:\\OneDrive\\SharedFile\\GEE_V2\\CompareWithLCs\\CompareWithLCs_Agricultural_land\\Sub_outDF.csv')
