# -*- coding: utf-8 -*-
# @Time    : 2020/7/1 10:51
# @Author  : THRILLER柠檬
# @Email   : thrillerlemon@outlook.com
# @File    : FIG-KindAreas.py
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
        'D:\\OneDrive\\SharedFile\\GEE_V2\\showLUCC\\LUCC_ChangeOnHex(86-18)\\KindsAreaChange.xlsx')

    years = range(1986, 2019)

    for index, col in data.iteritems():
        fig = plt.figure(figsize=(4.8, 1.8), dpi=400)
        ax = fig.add_subplot(111)
        plt.plot(years, list(col), color='k', label=str(index), linewidth=2, linestyle='-', marker='o', ms=5)

        model = LinearRegression()
        X = np.array(years).reshape(-1, 1)
        Y = np.array(col).reshape(-1, 1)
        model.fit(X, Y)
        X2 = [[1986], [1995], [2005], [2018]]
        y2 = model.predict(X2)
        plt.plot(X2, y2, color='tomato', linewidth=2.5, linestyle='--', label='Trend line')

        # 把x轴的刻度间隔设置为10，并存在变量里
        x_major_locator = MultipleLocator(6)
        ax.xaxis.set_major_locator(x_major_locator)
        plt.xlim(1985, 2019)

        ax.xaxis.tick_top()
        ax.tick_params(pad=2.5, width=2.2, length=5.5)
        plt.yticks(fontproperties='Times New Roman', size=18)
        plt.xticks(fontproperties='Times New Roman', size=18)
        # plt.xlabel('Year', fontproperties='Times New Roman', size=18)
        # plt.ylabel('Area($\mathregular{10^4km^2}$)',fontproperties='Times New Roman', size=18)
        ax.spines['right'].set_color('none')
        ax.spines['bottom'].set_color('none')
        plt.savefig('D:\\OneDrive\\SharedFile\\GEE_V2\\showLUCC\\LUCC_ChangeOnHex(86-18)\\Fig' + str(index) + '.png',
                    bbox_inches='tight', transparent=True)


if __name__ == '__main__':
    main()
