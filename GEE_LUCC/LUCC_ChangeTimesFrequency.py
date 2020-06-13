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
    ori_changeTimes = np.arange(0, 26, 1)
    ori_times = np.array([73873865.13,
                          12387625.4,
                          20783437.11,
                          10321284.72,
                          11769137.27,
                          7211123.6,
                          5205406.835,
                          3114572.706,
                          2287229.584,
                          1160757.027,
                          650521.4745,
                          342677.5137,
                          165826.0078,
                          77382.38824,
                          34598.3451,
                          15275.24314,
                          6116.215686,
                          2340,
                          899.8431373,
                          312,
                          91,
                          24,
                          5,
                          2,
                          3,
                          1])

    times = np.array(
        [73873865.13, 12387625.40, 20783437.11, 10321284.72, 11769137.27, 7211123.60, 12418487.63, 645553.56])

    changeTimesIndex = np.arange(0, 8, 1)
    changeTimes = ['0', '1', '2', '3', '4', '5', '6~10', '>10']

    frequency = times / times.sum()
    print(changeTimesIndex)
    print(frequency * 100)
    a = frequency * 100
    print(a.sum())

    fig = plt.figure(figsize=(7, 4), dpi=400)
    ax = fig.add_subplot(111)
    ax.bar(changeTimesIndex, a,
           color=['#ffffff', '#8aa8ce', '#b9d5ed', '#fffec5', '#ffe88b', '#ffb457', '#f9783f', '#db4f36'],
           label='Frequency', edgecolor='#6e6e6e')
    ax.set_yticks(np.arange(0, 55, 5))
    ax.set_yticklabels(np.arange(0, 55, 5), fontsize=16, fontfamily='Times New Roman')
    ax.set_xlim(-0.5, 7.5)
    ax.set_xticks(changeTimesIndex)
    ax.set_xticklabels(changeTimes, fontsize=16, fontfamily='Times New Roman')
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.set_xlabel('Number of Changes', fontsize=18, fontfamily='Times New Roman')
    ax.set_ylabel('Frequency(%)', fontsize=18, fontfamily='Times New Roman')
    plt.savefig('D:\\OneDrive\\SharedFile\\GEE_V2\\ChangeTimes\\Frequency.png',
                dpi=500, bbox_inches='tight')


if __name__ == '__main__':
    main()
