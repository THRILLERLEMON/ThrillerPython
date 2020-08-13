# GEE_LUCCKindsPercent
# THRILLER柠檬
# thrillerlemon@outlook.com
# 2020年07月26日

import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def main():
    # ******Main******
    print(time.strftime('%H:%M:%S', time.localtime(time.time())))
    fnPath = 'D:\\OneDrive\\SharedFile\\GEE_V2\\showLUCC\\CropChange\\'
    fnHead = 'CropAreahm2'
    fnTail = '.xlsx'
    AreaData = pd.read_excel(fnPath + fnHead + fnTail, sheet_name='Sheet1', index_col=0)

    ColormapList = {
        'Gansu': '#FCA47F',
        'Henan': '#FCDDD0',
        'Inner Mongolia': '#7C5240',
        'Ningxia': '#E65517',
        'Qinghai': '#7BF4C3',
        'Shanxi': '#2B5444',
        'Shaanxi': '#109C64'
    }

    fig = plt.figure(figsize=(9, 3.6), dpi=300)
    ax = fig.add_subplot(111)
    width = 0.5
    bottom = pd.Series(np.zeros(len(AreaData.index)), index=AreaData.index)
    for sheng in AreaData.columns:
        ax.bar([str(j) for j in list(AreaData[sheng].index)], list(AreaData[sheng] / 10000), width, label=str(sheng),
               color=ColormapList[sheng], bottom=list(bottom))
        bottom = bottom.add(AreaData[sheng] / 10000)

    font = {'family': 'Times New Roman',
            'weight': 'normal',
            'size': 14}

    plt.yticks(fontproperties='Times New Roman', size=12)
    plt.xticks(fontproperties='Times New Roman', size=12, rotation=45)
    ax.set_ylim(0, 1600)
    ax.set_xlim(-1, 26)
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    plt.xlabel('Year', font)
    plt.ylabel('Croplands Area($\mathregular{10^4hm^2}$)', font)
    plt.legend(loc='upper left', ncol=4, prop={'family': 'Times New Roman', 'size': 12}, frameon=False)

    plt.savefig(fnPath + "CroplandsAreaChange.png", bbox_inches='tight')


if __name__ == '__main__':
    main()
