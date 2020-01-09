# GEE LC YearsChangeKinds for network
# Get top 10 changes
# THRILLER柠檬
# thrillerlemon@outlook.com
# 2019年12月3日

import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def main():
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
    # Years
    fnPath = 'D:\\OneDrive\\SharedFile\\GEE_V2\\showLUCC\\LUCC_ChangeOnTime\\Years\\'
    fnHead = 'KindChangeArea'
    fnTail = '.csv'
    dfOut = pd.DataFrame(columns=['Source', 'Target', 'weight', 'Start', 'End', 'ChangeType'])

    for year in np.arange(1987, 2019):
        thisYearData = pd.read_csv(fnPath + fnHead + str(year) + fnTail)
        sourceLabel = thisYearData['Source'].map(mapList)
        targetLabel = thisYearData['Target'].map(mapList)
        thisYearData['SourceLabel'] = sourceLabel
        thisYearData['TargetLabel'] = targetLabel
        thisYearData['ChangeType'] = thisYearData['SourceLabel'] + ' to ' + thisYearData['TargetLabel']
        thisYearData.rename(columns={'ChangeRate': 'weight'}, inplace=True)
        thisYearData = thisYearData.drop(
            ['system:index', '.geo', 'SourceLabel', 'TargetLabel', 'ChangeArea'], axis=1)
        # thisYearData = thisYearData[['Source', 'Target', 'weight','ChangeType']]
        thisYearData['Start'] = year - 1
        thisYearData['End'] = year
        print(thisYearData)
        dfOut = dfOut.append(thisYearData)

    dfOut = dfOut.fillna(0)
    print(dfOut)
    dfOut.to_csv(
        'D:\\OneDrive\\SharedFile\\GEE_V2\\showLUCC\\LUCC_ChangeOnTime\\Years\\YearsChangeTypeValue.csv')
    print(time.strftime('%H:%M:%S', time.localtime(time.time())))


def mainold():
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
    # Years
    fnPath = 'D:\\OneDrive\\SharedFile\\GEE_V2\\showLUCC\\LUCC_ChangeOnTime\\Years\\'
    fnHead = 'KindChangeArea'
    fnTail = '.csv'
    # first year to set index
    thisYearData1987 = pd.read_csv(fnPath + fnHead + str(1987) + fnTail)
    sourceLabel1987 = thisYearData1987['Source'].map(mapList)
    targetLabel1987 = thisYearData1987['Target'].map(mapList)
    thisYearData1987['SourceLabel'] = sourceLabel1987
    thisYearData1987['TargetLabel'] = targetLabel1987
    thisYearData1987['ChangeLabel'] = thisYearData1987['SourceLabel'] + ' to ' + thisYearData1987['TargetLabel']
    thisYearData1987.index = thisYearData1987['ChangeLabel']
    thisYearData1987 = thisYearData1987.drop(
        ['system:index', '.geo', 'SourceLabel', 'TargetLabel', 'ChangeArea', 'ChangeLabel'], axis=1)
    thisYearData1987.rename(columns={'ChangeRate': str(1987)}, inplace=True)
    thisYearData1987 = thisYearData1987[['Source', 'Target', '1987']]

    for year in np.arange(1988, 2019):
        thisYearData = pd.read_csv(fnPath + fnHead + str(year) + fnTail)
        sourceLabel = thisYearData['Source'].map(mapList)
        targetLabel = thisYearData['Target'].map(mapList)
        thisYearData['SourceLabel'] = sourceLabel
        thisYearData['TargetLabel'] = targetLabel
        thisYearData['ChangeLabel'] = thisYearData['SourceLabel'] + ' to ' + thisYearData['TargetLabel']
        thisYearData.index = thisYearData['ChangeLabel']
        thisYearData = thisYearData.drop(
            ['system:index', '.geo', 'SourceLabel', 'TargetLabel', 'ChangeArea', 'ChangeLabel'], axis=1)
        thisYearData.rename(columns={'ChangeRate': str(year)}, inplace=True)
        thisYearData1987 = pd.merge(thisYearData1987, thisYearData, how='outer', on=['Source', 'Target'])
    thisYearData1987 = thisYearData1987.fillna(0)
    print(thisYearData1987)
    thisYearData1987.to_csv(
        'D:\\OneDrive\\SharedFile\\GEE_V2\\showLUCC\\LUCC_ChangeOnTime\\Years\\YearsChangeTypeValue.csv')
    print(time.strftime('%H:%M:%S', time.localtime(time.time())))


if __name__ == '__main__':
    main()
