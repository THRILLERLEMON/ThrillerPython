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

    fnPath = 'D:\\OneDrive\\SharedFile\\GEE_V2\KindArea\\'
    fnHead = 'ALL-RepairForPython'
    fnTail = '.xlsx'
    KindsAreaData = pd.read_excel(fnPath + fnHead + fnTail, index_col=0)

    for year in np.arange(1986, 2019):
        KindsAreaData[str(year) + 'Per'] = KindsAreaData[year] / KindsAreaData[year].sum() * 100
        KindsAreaData = KindsAreaData.drop(year, axis=1)
    Stds = []
    Means = []
    for tIndex, tRow in KindsAreaData.iterrows():
        Stds.append(tRow.std())
        Means.append(tRow.mean())
    KindsAreaData['std'] = Stds
    KindsAreaData['mean'] = Means
    width = 0.4

    fig = plt.figure(figsize=(10, 5), dpi=400)
    ax = fig.add_subplot(111)
    ax.bar('Forest', KindsAreaData['mean'][101], width, yerr=KindsAreaData['std'][101], label=LabelmapList[101],
           color=ColormapList[101])
    ax.bar('Forest', KindsAreaData['mean'][102], width, yerr=KindsAreaData['std'][102],
           bottom=KindsAreaData['mean'][101], label=LabelmapList[102], color=ColormapList[102])
    ax.bar('Forest', KindsAreaData['mean'][103], width, yerr=KindsAreaData['std'][103],
           bottom=KindsAreaData['mean'][101] + KindsAreaData['mean'][102], label=LabelmapList[103],
           color=ColormapList[103])
    ForestsPer = KindsAreaData['mean'][101] + KindsAreaData['mean'][102] + KindsAreaData['mean'][103]
    ax.text('Forest', ForestsPer + 1, str('%.2f' % ForestsPer) + '%', ha='center', va='bottom', fontsize=12,
            fontfamily='Times New Roman')

    ax.bar('Shrublands', KindsAreaData['mean'][201], width, yerr=KindsAreaData['std'][201], label=LabelmapList[201],
           color=ColormapList[201])
    ShrublandsPer = KindsAreaData['mean'][201]
    ax.text('Shrublands', ShrublandsPer + 1, str('%.2f' % ShrublandsPer) + '%', ha='center', va='bottom', fontsize=12,
            fontfamily='Times New Roman')

    ax.bar('Grasslands', KindsAreaData['mean'][301], width, yerr=KindsAreaData['std'][301], label=LabelmapList[301],
           color=ColormapList[301])
    ax.bar('Grasslands', KindsAreaData['mean'][302], width, yerr=KindsAreaData['std'][302],
           bottom=KindsAreaData['mean'][301], label=LabelmapList[302], color=ColormapList[302])
    ax.bar('Grasslands', KindsAreaData['mean'][303], width, yerr=KindsAreaData['std'][303],
           bottom=KindsAreaData['mean'][301] + KindsAreaData['mean'][302], label=LabelmapList[303],
           color=ColormapList[303])
    GrasslandsPer = KindsAreaData['mean'][301] + KindsAreaData['mean'][302] + KindsAreaData['mean'][303]
    ax.text('Grasslands', GrasslandsPer + 1, str('%.2f' % GrasslandsPer) + '%', ha='center', va='bottom', fontsize=12,
            fontfamily='Times New Roman')

    ax.bar('Agricultural\nlands', KindsAreaData['mean'][401], width, yerr=KindsAreaData['std'][401],
           label=LabelmapList[401], color=ColormapList[401])
    ax.bar('Agricultural\nlands', KindsAreaData['mean'][402], width, yerr=KindsAreaData['std'][402],
           bottom=KindsAreaData['mean'][401], label=LabelmapList[402], color=ColormapList[402])
    AgriculturalPer = KindsAreaData['mean'][401] + KindsAreaData['mean'][402]
    ax.text('Agricultural\nlands', AgriculturalPer + 1.3, str('%.2f' % AgriculturalPer) + '%', ha='center', va='bottom',
            fontsize=12,
            fontfamily='Times New Roman')

    ax.bar('Urban and\nBuilt-up', KindsAreaData['mean'][501], width, yerr=KindsAreaData['std'][501],
           label=LabelmapList[501], color=ColormapList[501])
    UrbanPer = KindsAreaData['mean'][501]
    ax.text('Urban and\nBuilt-up', UrbanPer + 1, str('%.2f' % UrbanPer) + '%', ha='center', va='bottom', fontsize=12,
            fontfamily='Times New Roman')

    ax.bar('Water\nBodies', KindsAreaData['mean'][601], width, yerr=KindsAreaData['std'][601], label=LabelmapList[601],
           color=ColormapList[601])
    ax.bar('Water\nBodies', KindsAreaData['mean'][602], width, yerr=KindsAreaData['std'][602],
           bottom=KindsAreaData['mean'][601], label=LabelmapList[602], color=ColormapList[602])
    ax.bar('Water\nBodies', KindsAreaData['mean'][603], width, yerr=KindsAreaData['std'][603],
           bottom=KindsAreaData['mean'][601] + KindsAreaData['mean'][602], label=LabelmapList[603],
           color=ColormapList[603])
    WaterPer = KindsAreaData['mean'][601] + KindsAreaData['mean'][602] + KindsAreaData['mean'][603]
    ax.text('Water\nBodies', WaterPer + 1, str('%.2f' % WaterPer) + '%', ha='center', va='bottom', fontsize=12,
            fontfamily='Times New Roman')

    ax.bar('Desert and\nLow-vegetated lands', KindsAreaData['mean'][701], width, yerr=KindsAreaData['std'][701],
           label=LabelmapList[701], color=ColormapList[701])
    ax.bar('Desert and\nLow-vegetated lands', KindsAreaData['mean'][702], width, yerr=KindsAreaData['std'][702],
           bottom=KindsAreaData['mean'][701], label=LabelmapList[702], color=ColormapList[702])
    DesertPer = KindsAreaData['mean'][701] + KindsAreaData['mean'][702]
    ax.text('Desert and\nLow-vegetated lands', DesertPer + 1, str('%.2f' % DesertPer) + '%', ha='center', va='bottom',
            fontsize=12,
            fontfamily='Times New Roman')

    font = {'family': 'Times New Roman',
            'weight': 'normal',
            'size': 14}

    plt.yticks(fontproperties='Times New Roman', size=12)
    plt.xticks(fontproperties='Times New Roman', size=12)
    ax.set_ylim(0, 50)
    plt.xlabel('Class', font)
    plt.ylabel('Area Ratio(%)', font)
    plt.legend(loc='upper right', ncol=3, prop={'family': 'Times New Roman', 'size': 12}, frameon=False)

    plt.savefig(fnPath + "KindsPercent.png", bbox_inches='tight')


if __name__ == '__main__':
    main()
