# -*- coding: utf-8 -*-
# @Time    : 2020/6/8 15:12
# @Author  : THRILLER柠檬
# @Email   : thrillerlemon@outlook.com
# @File    : FIG-FillBetween(LAIchange).py
# @Software: PyCharm


import os
import time
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator
from sklearn.linear_model import LinearRegression


def main():
    fontL = {'family': 'Times New Roman',
             'size': 16, }

    data = pd.read_excel(
        'D:\\GIS_DATA\\GEE_DATA_landcover_V2\\NOAA_LAI_ChangeSlope1986-2018_1000m\\NOAA_LAI_ChangeForPython.xlsx')

    years = range(1986, 2019)

    fig = plt.figure(figsize=(10, 6), dpi=400)
    ax = fig.add_subplot(111)

    labels = ["p25", "p75"]

    ax.fill_between(years, data['p25'], data['p75'], alpha=0.8, color='#b3e093', label='Percentile Range(25-75)')

    # ax.stackplot(years, data['p25'], data['p75'], colors=['w','yellowgreen'],labels=labels)
    ax.plot(years, data['Mean'], color='g', label='Mean', linewidth=2, linestyle='-', marker='o', ms=5)

    model = LinearRegression()
    X = data['year'].values.reshape(-1, 1)
    Y = data['Mean'].values.reshape(-1, 1)
    model.fit(X, Y)
    X2 = [[1986], [1995], [2005], [2018]]
    y2 = model.predict(X2)
    plt.plot(X2, y2, color='tomato', linewidth=2, linestyle='--', label='Trend line')

    ax.legend(loc='upper left', prop=fontL, frameon=False)

    # 把x轴的刻度间隔设置为5，并存在变量里
    # x_major_locator = MultipleLocator(1)
    # 把y轴的刻度间隔设置为0.5，并存在变量里
    y_major_locator = MultipleLocator(0.5)
    # ax.xaxis.set_major_locator(x_major_locator)
    ax.yaxis.set_major_locator(y_major_locator)

    # ax.set_yticks(np.arange(0,1.8,0.5))
    ax.set_xticks(years)
    # label_X = [int(i) for i in list(ax.get_xticks())]
    # label_X = ['1986','1987','1988','1989','1990','1991','1992','1993','1994','1995',
    #            '1996','1997','1998','1999','2000','2001','2002','2003','2004','2005',
    #            '2006','2007','2008','2009','2010','2011','2012','2013','2014','2015','2016','2017','2018']
    label_X = ['', '', '', '', '1990', '', '', '', '', '1995',
               '', '', '', '', '2000', '', '', '', '', '2005',
               '', '', '', '', '2010', '', '', '', '', '2015', '', '', '']
    ax.set_xticklabels(label_X, fontsize=16, fontfamily='Times New Roman')
    ax.set_xlim(1986, 2018)
    ax.set_ylim(0, 1.5)

    ax.set_yticklabels(list(ax.get_yticks()), fontsize=16, fontfamily='Times New Roman')
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.set_xlabel('Years', fontsize=18, fontfamily='Times New Roman')
    ax.set_ylabel('LAI', fontsize=18, fontfamily='Times New Roman')
    plt.savefig('D:\\GIS_DATA\\GEE_DATA_landcover_V2\\NOAA_LAI_ChangeSlope1986-2018_1000m\\LAIchangePython.png',
                bbox_inches='tight')


if __name__ == '__main__':
    main()
