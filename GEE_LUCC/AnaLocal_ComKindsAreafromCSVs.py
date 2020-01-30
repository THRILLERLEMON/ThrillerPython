# -*- coding: utf-8 -*-
# @Time    : 2020/1/8 17:16
# @Author  : THRILLER柠檬
# @Email   : thrillerlemon@outlook.com
# @File    : AnaLocal_ComKindsAreafromCSVs.py
# @Software: PyCharm

import numpy as np
import pandas as pd


def main():
    # combine years kinds area csv to 1 total Table
    fnPath = 'D:\\OneDrive\\SharedFile\\GEE_V2\\AnalyzeLocalArea\\KindsArea\\'
    fnHead = 'WuqiZhidanKindsArea'
    fnTail = '.csv'

    yearsData = pd.DataFrame({'Years': np.arange(1986, 2019)})
    yearsData.index = yearsData['Years']
    yearsData = yearsData.drop(['Years'], axis=1)

    for year in np.arange(1986, 2019):
        thisYearData = pd.read_csv(fnPath + fnHead + str(year) + fnTail)
        for tIndex, tRow in thisYearData.iterrows():
            kind = tRow["kind"]
            area = tRow["kindarea"]
            yearsData.loc[year, str(kind)] = area
    print(yearsData)
    yearsData.to_excel(
        'D:\\OneDrive\\SharedFile\\GEE_V2\\AnalyzeLocalArea\\' + fnHead + '_TotalAllYears.xlsx')


if __name__ == '__main__':
    main()
