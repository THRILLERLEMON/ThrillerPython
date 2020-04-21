# -*- coding: utf-8 -*-
# @Time    : 2020/4/17 21:07
# @Author  : THRILLER柠檬
# @Email   : thrillerlemon@outlook.com
# @File    : CompareWithLCs_Agricultural_land.py
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

allCountryTrueData = pd.read_excel(
    'D:\OneDrive\SharedFile\GEE_V2\CompareWithLCs\CompareWithLCs_Agricultural_land\耕地面积_单位-平方米.xlsx', sheet_name="pingfangmi")

def FindValue(pCountryCode, pYear):
    findresult = allCountryTrueData[
        (allCountryTrueData["County_code_N"] == int(pCountryCode))
        ].copy()
    return findresult[pYear].iloc[0]


dfOut = pd.DataFrame(columns=['TrueArea', 'DataArea', 'DataSet','CountryCode','Year'])


csvPath='D:\\OneDrive\\SharedFile\\GEE_V2\\CompareWithLCs\\CompareWithLCs_Agricultural_land\\csv\\'

fig, ax = plt.subplots(figsize=(10, 10), dpi=300)

#ThisStudy1990-2014
for year in np.arange(1990, 2014, 1):
    dataCSV=pd.read_csv(csvPath+'KindArea_Agricultural_land_ThisStudy'+str(year)+'.csv')
    for tIndex, tRow in dataCSV.iterrows():
        countryCode = tRow["County_c_1"]
        dataArea=tRow["sum"]
        findedvalue = FindValue(countryCode, year)
        dic={'TrueArea':findedvalue/100000000,
             'DataArea':dataArea/100000000,
             'DataSet':'This Study',
             'CountryCode':countryCode,
             'Year':year,
             }
        dfOut=dfOut.append(dic,ignore_index=True)
dfOut=dfOut[(dfOut["TrueArea"]>1) & (dfOut["TrueArea"]<50) & (dfOut["DataArea"]>0) & (dfOut["DataArea"]<50) ]
thisDS=dfOut[dfOut['DataSet']=='This Study']
print('This Study')
print(f"均方误差(MSE)：{mean_squared_error(thisDS['TrueArea'],thisDS['DataArea'])}")
print(f"根均方误差(RMSE)：{np.sqrt(mean_squared_error(thisDS['TrueArea'],thisDS['DataArea']))}")
print(f"测试集R^2：{r2_score(thisDS['TrueArea'], thisDS['DataArea'])}")
plt.scatter(thisDS['TrueArea'], thisDS['DataArea'], marker='^', color='b', s=80,alpha=0.8,label='This Study',edgecolors='none')

#Modis2001-2014
for year in np.arange(2001, 2014, 1):
    dataCSV=pd.read_csv(csvPath+'KindArea_Agricultural_land_LC_'+str(year)+'MODIS_500.csv')
    for tIndex, tRow in dataCSV.iterrows():
        countryCode = tRow["County_c_1"]
        dataArea=tRow["sum"]
        findedvalue = FindValue(countryCode, year)
        dic={'TrueArea':findedvalue/100000000,
             'DataArea':dataArea/100000000,
             'DataSet':'MCD12Q1-V6',
             'CountryCode':countryCode,
             'Year':year,
             }
        dfOut=dfOut.append(dic,ignore_index=True)
dfOut=dfOut[(dfOut["TrueArea"]>1) & (dfOut["TrueArea"]<50) & (dfOut["DataArea"]>0) & (dfOut["DataArea"]<50) ]
thisDS=dfOut[dfOut['DataSet']=='MCD12Q1-V6']
print('MCD12Q1-V6')
print(f"均方误差(MSE)：{mean_squared_error(thisDS['TrueArea'],thisDS['DataArea'])}")
print(f"根均方误差(RMSE)：{np.sqrt(mean_squared_error(thisDS['TrueArea'],thisDS['DataArea']))}")
print(f"测试集R^2：{r2_score(thisDS['TrueArea'], thisDS['DataArea'])}")
plt.scatter(thisDS['TrueArea'], thisDS['DataArea'], marker='o', color='g',s=80,alpha=0.8,label='MCD12Q1-V6',edgecolors='none')

#LJY1995\2000\2005
for year in [1995,2000,2005]:
    dataCSV=pd.read_csv(csvPath+'KindArea_Agricultural_land_LC_'+str(year)+'LJY_1000.csv')
    for tIndex, tRow in dataCSV.iterrows():
        countryCode = tRow["County_c_1"]
        dataArea=tRow["sum"]
        findedvalue = FindValue(countryCode, year)
        dic={'TrueArea':findedvalue/100000000,
             'DataArea':dataArea/100000000,
             'DataSet':'ChinaLC1000',
             'CountryCode':countryCode,
             'Year':year,
             }
        dfOut=dfOut.append(dic,ignore_index=True)
dfOut=dfOut[(dfOut["TrueArea"]>1) & (dfOut["TrueArea"]<50) & (dfOut["DataArea"]>0) & (dfOut["DataArea"]<50) ]
thisDS=dfOut[dfOut['DataSet']=='ChinaLC1000']
print('ChinaLC1000')
print(f"均方误差(MSE)：{mean_squared_error(thisDS['TrueArea'],thisDS['DataArea'])}")
print(f"根均方误差(RMSE)：{np.sqrt(mean_squared_error(thisDS['TrueArea'],thisDS['DataArea']))}")
print(f"测试集R^2：{r2_score(thisDS['TrueArea'], thisDS['DataArea'])}")
plt.scatter(thisDS['TrueArea'], thisDS['DataArea'], marker='x', color='r', s=80,alpha=0.8,label='ChinaLC1000',edgecolors='none')

#GlobalLandCover30 2000   2010
for year in [2000,2010]:
    dataCSV=pd.read_csv(csvPath+'KindArea_Agricultural_land_LC_'+str(year)+'GlobalLandCover30_30.csv')
    for tIndex, tRow in dataCSV.iterrows():
        countryCode = tRow["County_c_1"]
        dataArea=tRow["sum"]
        findedvalue = FindValue(countryCode, year)
        dic={'TrueArea':findedvalue/100000000,
             'DataArea':dataArea/100000000,
             'DataSet':'GlobeLand30',
             'CountryCode':countryCode,
             'Year':year,
             }
        dfOut=dfOut.append(dic,ignore_index=True)
dfOut=dfOut[(dfOut["TrueArea"]>1) & (dfOut["TrueArea"]<50) & (dfOut["DataArea"]>0) & (dfOut["DataArea"]<50) ]
thisDS=dfOut[dfOut['DataSet']=='GlobeLand30']
print('GlobeLand30')
print(f"均方误差(MSE)：{mean_squared_error(thisDS['TrueArea'],thisDS['DataArea'])}")
print(f"根均方误差(RMSE)：{np.sqrt(mean_squared_error(thisDS['TrueArea'],thisDS['DataArea']))}")
print(f"测试集R^2：{r2_score(thisDS['TrueArea'], thisDS['DataArea'])}")
plt.scatter(thisDS['TrueArea'], thisDS['DataArea'], marker='v', color='c', s=80,alpha=0.8,label='GlobeLand30',edgecolors='none')

#GlobCover 2005 2009
for year in [2005,2009]:
    dataCSV=pd.read_csv(csvPath+'KindArea_Agricultural_land_LC_'+str(year)+'GlobCover_300.csv')
    for tIndex, tRow in dataCSV.iterrows():
        countryCode = tRow["County_c_1"]
        dataArea=tRow["sum"]
        findedvalue = FindValue(countryCode, year)
        dic={'TrueArea':findedvalue/100000000,
             'DataArea':dataArea/100000000,
             'DataSet':'GlobCover',
             'CountryCode':countryCode,
             'Year':year,
             }
        dfOut=dfOut.append(dic,ignore_index=True)
dfOut=dfOut[(dfOut["TrueArea"]>1) & (dfOut["TrueArea"]<50) & (dfOut["DataArea"]>0) & (dfOut["DataArea"]<50) ]
thisDS=dfOut[dfOut['DataSet']=='GlobCover']
print('GlobCover')
print(f"均方误差(MSE)：{mean_squared_error(thisDS['TrueArea'],thisDS['DataArea'])}")
print(f"根均方误差(RMSE)：{np.sqrt(mean_squared_error(thisDS['TrueArea'],thisDS['DataArea']))}")
print(f"测试集R^2：{r2_score(thisDS['TrueArea'], thisDS['DataArea'])}")
plt.scatter(thisDS['TrueArea'], thisDS['DataArea'], marker='s', color='y',s=80,alpha=0.8,label='GlobCover',edgecolors='none')

#FROMGLC 2010
dataCSV=pd.read_csv(csvPath+'KindArea_Agricultural_land_LC_2010FROMGLC_30.csv')
for tIndex, tRow in dataCSV.iterrows():
    countryCode = tRow["County_c_1"]
    dataArea=tRow["sum"]
    findedvalue = FindValue(countryCode, year)
    dic={'TrueArea':findedvalue/100000000,
         'DataArea':dataArea/100000000,
         'DataSet':'FROM-GLC',
         'CountryCode':countryCode,
         'Year':year,
         }
    dfOut=dfOut.append(dic,ignore_index=True)
dfOut=dfOut[(dfOut["TrueArea"]>1) & (dfOut["TrueArea"]<50) & (dfOut["DataArea"]>0) & (dfOut["DataArea"]<50) ]
thisDS=dfOut[dfOut['DataSet']=='FROM-GLC']
print('FROM-GLC')
print(f"均方误差(MSE)：{mean_squared_error(thisDS['TrueArea'],thisDS['DataArea'])}")
print(f"根均方误差(RMSE)：{np.sqrt(mean_squared_error(thisDS['TrueArea'],thisDS['DataArea']))}")
print(f"测试集R^2：{r2_score(thisDS['TrueArea'], thisDS['DataArea'])}")
plt.scatter(thisDS['TrueArea'], thisDS['DataArea'], marker='H', color='k',s=80,alpha=0.8,label='FROM-GLC',edgecolors='none')

#GLC 1992
dataCSV=pd.read_csv(csvPath+'KindArea_Agricultural_land_LC_1992GLC_1000.csv')
for tIndex, tRow in dataCSV.iterrows():
    countryCode = tRow["County_c_1"]
    dataArea=tRow["sum"]
    findedvalue = FindValue(countryCode, year)
    dic={'TrueArea':findedvalue/100000000,
         'DataArea':dataArea/100000000,
         'DataSet':'GLCC',
         'CountryCode':countryCode,
         'Year':year,
         }
    dfOut=dfOut.append(dic,ignore_index=True)
dfOut=dfOut[(dfOut["TrueArea"]>1) & (dfOut["TrueArea"]<50) & (dfOut["DataArea"]>0) & (dfOut["DataArea"]<50) ]
thisDS=dfOut[dfOut['DataSet']=='GLCC']
print('GLCC')
print(f"均方误差(MSE)：{mean_squared_error(thisDS['TrueArea'],thisDS['DataArea'])}")
print(f"根均方误差(RMSE)：{np.sqrt(mean_squared_error(thisDS['TrueArea'],thisDS['DataArea']))}")
print(f"测试集R^2：{r2_score(thisDS['TrueArea'], thisDS['DataArea'])}")
plt.scatter(thisDS['TrueArea'], thisDS['DataArea'], marker='+', color='m', s=80,alpha=0.8,label='GLCC',edgecolors='none')

ax.legend()
plt.xlim((0, 50))
plt.ylim((0, 50))
plt.yticks(fontproperties = 'Times New Roman', size = 18)
plt.xticks(fontproperties = 'Times New Roman', size = 18)
plt.legend(prop={'family' : 'Times New Roman', 'size'   : 18})
ax.set_xlabel('TrueArea($\mathregular{10^4hm^2}$)', fontdict={'family' : 'Times New Roman', 'size'   : 20})
ax.set_ylabel('DataArea($\mathregular{10^4hm^2}$)',fontdict={'family' : 'Times New Roman', 'size'   : 20})
ax.set_title('Agricultural land Area Compare',fontdict={'family' : 'Times New Roman', 'size'   : 20})

plt.savefig('D:\\OneDrive\\SharedFile\\GEE_V2\\CompareWithLCs\\CompareWithLCs_Agricultural_land\\scatter.png',dpi=300,bbox_inches='tight')
# plt.show()
dfOut.to_csv(
        'D:\\OneDrive\\SharedFile\\GEE_V2\\CompareWithLCs\\CompareWithLCs_Agricultural_land\\outDF.csv')
