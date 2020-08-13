# -*- coding: utf-8 -*-
# @Time    : 2020/6/5 20:59
# @Author  : THRILLER柠檬
# @Email   : thrillerlemon@outlook.com
# @File    : LUCC_ChangeTimesFrequency.py
# @Software: PyCharm


import os
import time
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt


def main():
    changeTimesIndex = np.arange(0, 5, 1)
    times = np.array([38058901,
                      72425487,
                      31883301,
                      6918470,
                      176248
                      ])

    label = ['1', '1~1.5', '1.5~2', '2~2.5', '2.5~3']

    frequency = times / times.sum()
    print(changeTimesIndex)
    print(frequency * 100)
    a = frequency * 100
    print(a.sum())

    fig = plt.figure(figsize=(5, 4), dpi=400)
    ax = fig.add_subplot(111)
    ax.bar(changeTimesIndex, a,
           color=['#E1E1E1', '#33C1FF', '#B6FE8E', '#FFC801', '#FE0000'],
           label='Frequency', edgecolor='#6e6e6e')

    for a, b in zip(range(5), np.array(a)):
        ax.text(a, b + 0.3, '%.2f' % b + '%', ha='center', va='bottom', fontsize=16, fontfamily='Times New Roman')

    ax.set_yticks(np.arange(0, 60, 10))
    ax.set_yticklabels(np.arange(0, 60, 10), fontsize=16, fontfamily='Times New Roman')
    ax.set_xlim(-0.5, 4.5)
    ax.set_xticks(changeTimesIndex)
    ax.set_xticklabels(label, fontsize=16, fontfamily='Times New Roman')
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.set_xlabel('Count of unique values of each year 10 times result', fontsize=18, fontfamily='Times New Roman')
    ax.set_ylabel('Frequency(%)', fontsize=18, fontfamily='Times New Roman')
    plt.savefig('D:\\GIS_DATA\\GEE_DATA_landcover_V2\\Ori_Uncertainty\\Frequency.png', bbox_inches='tight')


if __name__ == '__main__':
    main()
