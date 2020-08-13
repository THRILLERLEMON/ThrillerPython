# -*- coding: utf-8 -*-
# @Time    : 2020/8/12 12:12
# @Author  : THRILLER柠檬
# @Email   : thrillerlemon@outlook.com
# @File    : ShowSpectraInfo.py
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
             'size': 14, }

    data = pd.read_excel('D:\\OneDrive\\GEE_Figure\\SpectraInfo\\AllKindsSpectraInfo_meanForPython.xlsx',
                         sheet_name='Sheet1', index_col='Band')

    LabelmapList = {
        101: 'DBF',
        102: 'ENF',
        103: 'MF',
        201: 'Shrub',
        301: 'LCG',
        302: 'MCG',
        303: 'HCG',
        401: 'Crop',
        402: 'OT',
        501: 'UB',
        601: 'Water',
        602: 'Wet',
        603: 'Snow',
        701: 'DB',
        702: 'LV',
    }
    ColormapList = {
        101: '#1B7201',
        102: '#064A01',
        103: '#01B61F',
        201: '#50FF00',
        301: '#A4D081',
        302: '#88B75F',
        303: '#6E9E45',
        401: '#F2F100',
        402: '#F29B00',
        501: '#F00001',
        601: '#0058F0',
        602: '#00E0F0',
        603: '#BDF4F8',
        701: '#000000',
        702: '#9F9F9F',
    }

    fig = plt.figure(figsize=(10, 6), dpi=400)
    ax = fig.add_subplot(111)

    for pClass in list(LabelmapList.keys()):
        ax.plot(list(data.index), data[pClass], color=ColormapList[pClass],
                label=LabelmapList[pClass], linewidth=2, marker='o', ms=3, linestyle='-')

    ax.legend(loc='lower left', ncol=3, prop=fontL, frameon=False)

    # ax.set_xlim(1986, 2018)
    ax.set_ylim(-0.8, 1)
    plt.yticks(fontproperties='Times New Roman', size=14)
    plt.xticks(fontproperties='Times New Roman', size=14, rotation=90)
    ax.set_xlabel('Band', fontsize=14, fontfamily='Times New Roman')
    ax.set_ylabel('Band value', fontsize=14, fontfamily='Times New Roman')
    plt.savefig('D:\\OneDrive\\GEE_Figure\\SpectraInfo\\BnadsValueEachClass.png',
                bbox_inches='tight')


if __name__ == "__main__":
    main()
