# -*- coding: utf-8 -*-
# @Time    : 2020/6/8 15:12
# @Author  : THRILLER柠檬
# @Email   : thrillerlemon@outlook.com
# @File    : FIG-LandsatUseandAccuracyInfo.py
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

    data = pd.read_excel('D:\\OneDrive\\GEE_Figure\\分类精度和使用景数\\分类精度和使用景数.xlsx')

    years = range(1986, 2019)

    fig = plt.figure(figsize=(10, 6), dpi=400)
    ax1 = fig.add_subplot(111)

    ax1.fill_between(years, data['min'], data['Accuracy range'], alpha=0.8, color='thistle', label='Accuracy range')

    ax1.plot(years, data['Training accuracy of all(mean)'], color='purple', label='Training accuracy of all(mean)',
             linewidth=2, linestyle='-')

    ax1.legend(loc='upper left', prop=fontL, frameon=False)

    ax2 = ax1.twinx()
    ax2.bar(x=range(1986, 2012), height=np.array(data['Used Landsat 5 scenes'].head(26).values), color='#4D9EDE',
            label='Landsat 5 scenes')
    ax2.bar(x=2012, height=np.array(527), color='#59DB5A', label='Landsat 7 scenes')
    ax2.bar(x=range(2013, 2019), height=np.array([484, 607, 598, 545, 571, 791]), color='#F78F3D',
            label='Landsat 8 scenes')
    ax2.set_yticks(np.arange(0, 1400, 200))
    ax2.set_yticklabels(['0', '200', '400', '600', '800', '1000', '1200'], fontsize=16, fontfamily='Times New Roman')
    ax2.set_ylim(0, 1200)
    ax2.legend(loc=7, bbox_to_anchor=(0.95, 0.59), prop=fontL, frameon=False)

    # ax.set_yticks(np.arange(0,1.8,0.5))
    ax1.set_xticks(years)
    # label_X = [int(i) for i in list(ax.get_xticks())]
    # label_X = ['1986','1987','1988','1989','1990','1991','1992','1993','1994','1995',
    #            '1996','1997','1998','1999','2000','2001','2002','2003','2004','2005',
    #            '2006','2007','2008','2009','2010','2011','2012','2013','2014','2015','2016','2017','2018']
    label_X = ['', '', '', '', '1990', '', '', '', '', '1995',
               '', '', '', '', '2000', '', '', '', '', '2005',
               '', '', '', '', '2010', '', '', '', '', '2015', '', '', '']
    ax1.set_xticklabels(label_X, fontsize=16, fontfamily='Times New Roman')
    ax1.set_xlim(1985.4, 2018.6)
    ax1.set_ylim(0.83, 0.93)
    ax1.set_yticks(np.arange(0.83, 0.95, 0.02))
    ax1.set_yticklabels(['0.83', '0.85', '0.87', '0.89', '0.91', '0.93'], fontsize=16, fontfamily='Times New Roman')
    # ax1.spines['right'].set_color('none')
    #     # ax1.spines['top'].set_color('none')
    ax1.set_xlabel('Years', fontsize=18, fontfamily='Times New Roman')
    ax1.set_ylabel('Accuracy', fontsize=18, fontfamily='Times New Roman')
    plt.savefig('D:\\OneDrive\\GEE_Figure\\分类精度和使用景数\\分类精度和使用景数.png',
                bbox_inches='tight')


if __name__ == '__main__':
    main()
