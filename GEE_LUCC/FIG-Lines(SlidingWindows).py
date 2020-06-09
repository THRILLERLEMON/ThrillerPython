# -*- coding: utf-8 -*-
# @Time    : 2020/6/8 15:12
# @Author  : THRILLER柠檬
# @Email   : thrillerlemon@outlook.com
# @File    : FIG-Lines(SlidingWindows).py
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

    data = pd.read_excel('D:\\OneDrive\\GEE_Figure\\SlidWindow\\ALL.xlsx')

    years = range(1986, 2019)

    fig = plt.figure(figsize=(10, 6), dpi=400)
    ax = fig.add_subplot(111)

    ax.plot(years, data['3Window'], color='darkgreen', label='3 years Window', linewidth=2.5, linestyle='-')
    ax.plot(years, data['5Window'], color='darkorange', label='5 years Window', linewidth=2.5, linestyle='-')

    ax.legend(loc='lower right', prop=fontL, frameon=False)

    # 把x轴的刻度间隔设置为5，并存在变量里
    # x_major_locator = MultipleLocator(1)
    # 把y轴的刻度间隔设置为0.5，并存在变量里
    y_major_locator = MultipleLocator(0.05)
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
    ax.set_ylim(0.75, 0.95)

    ax.set_yticklabels(['0.70', '0.75', '0.80', '0.85', '0.90', '0.95'], fontsize=16, fontfamily='Times New Roman')
    # ax.spines['right'].set_color('none')
    # ax.spines['top'].set_color('none')
    ax.set_xlabel('Years', fontsize=18, fontfamily='Times New Roman')
    ax.set_ylabel('Accuracy', fontsize=18, fontfamily='Times New Roman')
    plt.savefig('D:\\OneDrive\\GEE_Figure\\SlidWindow\\SlidingWindow.png',
                bbox_inches='tight')


if __name__ == '__main__':
    main()
