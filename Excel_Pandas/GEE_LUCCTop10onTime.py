# GEE LC YearsChangeTop10Kinds
# Get top 10 changes
# THRILLER柠檬
# thrillerlemon@outlook.com
# 2019年11月27日

import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def main():
    # ******Main******
    print(time.strftime('%H:%M:%S', time.localtime(time.time())))
    mapList = {
        101: 'DBF',
        102: 'ENF',
        103: 'MF',
        201: 'Oshrub',
        202: 'Cshrub',
        301: 'XerGra',
        302: 'TemGra',
        401: 'Crop',
        402: 'Orchard',
        501: 'Builtup',
        601: 'Water',
        602: 'Wet',
        603: 'Snow',
        701: 'Desert',
        702: 'Barren',
    }
    # 86-18 top 10 kinds
    change33Years = pd.read_csv(
        'D:\\OneDrive\\SharedFile\\GEE_V2\\showLUCC\\LUCC_ChangeOnHex(86-18)\\KindChangeArea1986_2018.csv')
    change33Top10 = change33Years.sort_values(by='ChangeArea', ascending=False).head(10)
    sourceLabel = change33Top10['Source'].map(mapList)
    targetLabel = change33Top10['Target'].map(mapList)
    change33Top10['SourceLabel'] = sourceLabel
    change33Top10['TargetLabel'] = targetLabel
    changeTop10Kinds = change33Top10['SourceLabel'] + ' to ' + change33Top10['TargetLabel']
    changeTop10Kinds = pd.Series(['Other change types']).append(changeTop10Kinds, ignore_index=True)

    YearsTop10 = pd.DataFrame({'Type': changeTop10Kinds})
    # Years
    fnPath = 'D:\\OneDrive\\SharedFile\\GEE_V2\\showLUCC\\LUCC_ChangeOnTime\\Years\\'
    fnHead = 'KindChangeArea'
    fnTail = '.csv'
    for year in np.arange(1987, 2019):
        thisYearData = pd.read_csv(fnPath + fnHead + str(year) + fnTail)
        sortData = thisYearData.sort_values(by='ChangeArea', ascending=False)
        sourceLabel = sortData['Source'].map(mapList)
        targetLabel = sortData['Target'].map(mapList)
        sortData['SourceLabel'] = sourceLabel
        sortData['TargetLabel'] = targetLabel
        sortData['ChangeLabel'] = sortData['SourceLabel'] + ' to ' + sortData['TargetLabel']
        totalCA = sortData['ChangeArea'].sum()
        totalTop10 = 0
        kindsValues = []
        for k in np.arange(1, 11):
            kind = changeTop10Kinds[k]
            thisYearKindV = sortData[(sortData['ChangeLabel'] == kind)]['ChangeArea'].values[0]
            kindsValues.append(thisYearKindV)
            totalTop10 = totalTop10 + thisYearKindV
        kindsValues.insert(0,(totalCA - totalTop10))
        YearsTop10[str(year)] = pd.Series(kindsValues)
        print('finish a year')
    YearsTop10.index = YearsTop10['Type']
    print(YearsTop10)
    YearsTop10 = YearsTop10.drop(['Type'], axis=1)
    YearsTop10T = pd.DataFrame(YearsTop10.values.T, index=YearsTop10.columns, columns=YearsTop10.index)
    print(YearsTop10T)
    YearsTop10T.plot.bar(stacked=True, color=['#8B8B8B','#ff6d4c','#d6b3b3','#D05300','#BC9900','#dcd159','#A25300','#086a10','#c6b044','#b6ff05','#78d203'],title='Top 10 Change Type')
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    main()
