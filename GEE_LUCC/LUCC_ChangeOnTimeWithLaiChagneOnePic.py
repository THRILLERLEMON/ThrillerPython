# -*- coding: utf-8 -*-
# @Time    : 2020/3/19 15:55
# @Author  : THRILLER柠檬
# @Email   : thrillerlemon@outlook.com
# @File    : LUCC_ChangeOnTimeWithLaiChagne.py
# @Software: PyCharm

import os
import time
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, BoundaryNorm


def main():
    print(time.strftime('%H:%M:%S', time.localtime(time.time())))
    mapList = {
        101: 'DBF',
        102: 'ENF',
        103: 'MF',
        201: 'Shrub',
        301: 'Lgrass',
        302: 'Mgrass',
        303: 'Hgrass',
        401: 'Crop',
        402: 'Orchard',
        501: 'Builtup',
        601: 'Water',
        602: 'Wet',
        603: 'Snow',
        701: 'Desert',
        702: 'Barren',
    }

    fontL = {'family': 'Times New Roman',
             'size': 14,
             }

    dfOut = pd.DataFrame(columns=['Source', 'Target', 'Year', 'ChangeType', 'ChangeArea', 'ChangeLA'])

    # Read Files
    fnPath = 'D:\\OneDrive\\SharedFile\\GEE_V2\\showLUCC\\LUCC_ChangeOnTimeWithLAIchange_InLP_HotPotMKSen\\CSVs'
    filenames = os.listdir(fnPath)
    for i, filename in enumerate(filenames):
        thisYearData = pd.read_csv(fnPath + '\\' + filename)
        sourceLabel = thisYearData['Source'].map(mapList)
        targetLabel = thisYearData['Target'].map(mapList)
        thisYearData['SourceLabel'] = sourceLabel
        thisYearData['TargetLabel'] = targetLabel
        thisYearData['ChangeType'] = thisYearData['SourceLabel'] + ' to ' + thisYearData['TargetLabel']
        thisYearData = thisYearData.drop(
            ['system:index', '.geo', 'SourceLabel', 'TargetLabel'], axis=1)
        # print(thisYearData)
        dfOut = dfOut.append(thisYearData)

    dfOut = dfOut.fillna(0)
    # 各类别变化的面积多年平均
    typesChangeAreaMean = dfOut.groupby('ChangeType')['ChangeArea'].mean()
    # 各类33年总的LA增加或者减少（不是绝对值）
    typesChangeLAtotal = dfOut.groupby('ChangeType')['ChangeLA'].sum()
    typesChangeLA_Percent = typesChangeLAtotal / dfOut['ChangeLA'].sum(axis=0)

    typesChangeAreatotal = dfOut.groupby('ChangeType')['ChangeArea'].sum()
    typesChangeArea_Percent = typesChangeAreatotal / dfOut['ChangeArea'].sum(axis=0)

    PaA = pd.DataFrame({'ChangeLA_Percent': typesChangeLA_Percent, 'ChangeArea_Percent': typesChangeArea_Percent,
                        'ChangeAreaMean': typesChangeAreaMean})
    PaA = PaA.sort_values(by='ChangeLA_Percent', ascending=False)

    typesByChangeLASort = list(PaA.index)

    # 假设只绘出LA变化量最大的前40种类型
    topTypesNum = 35

    # 画累计百分比分布图
    fig = plt.figure(figsize=(10, 5), dpi=500)
    ax = fig.add_subplot(111)
    cpfTypes = cumulative_percent(typesChangeLA_Percent.sort_values(ascending=False))
    apfAreaTypes = cumulative_percent(typesChangeArea_Percent.sort_values(ascending=False))
    typesChangeLAFig = pd.DataFrame(
        [PaA['ChangeLA_Percent'],
         PaA['ChangeArea_Percent'],
         PaA['ChangeAreaMean'],
         pd.Series(cpfTypes[1:], index=PaA.index, name='LAC_cumulative_per'),
         pd.Series(apfAreaTypes[1:], index=PaA.index, name='AC_cumulative_per'),
         typesChangeLAtotal])
    typesChangeLAFig = pd.DataFrame(typesChangeLAFig.values.T, index=typesChangeLAFig.columns,
                                    columns=typesChangeLAFig.index)
    typesChangeLAFig = typesChangeLAFig[typesChangeLAFig['ChangeAreaMean'] > 100000]
    typesChangeLAFig.to_csv(
        'D:\\OneDrive\\SharedFile\\GEE_V2\\showLUCC\\LUCC_ChangeOnTimeWithLAIchange_InLP_HotPotMKSen\\OnePic\\ChangeTypes_LA_ChangePercent.csv')

    ax.plot(range(topTypesNum), typesChangeLAFig['ChangeAreaMean'].head(topTypesNum), color='lightcoral', linewidth=1,
            linestyle='-', marker='o', ms=2, label='Mean change area in years')

    ax2 = ax.twinx()
    ax2.plot(range(topTypesNum), np.array(typesChangeLAFig['LAC_cumulative_per'].head(topTypesNum).values), linewidth=1,
             color='k', label='Cumulative Ratio')
    ax2.bar(x=range(topTypesNum), height=np.array(typesChangeLAFig['ChangeLA_Percent'].head(topTypesNum).values),
            color='cornflowerblue', label='Ratio of the change in leaf area to the total')

    ax2.set_xlabel('Land Cover change Types', fontsize=10, fontfamily='Times New Roman')
    ax2.set_ylabel('Ratio', fontsize=10, fontfamily='Times New Roman')

    ax2.set_xlim(-1, topTypesNum)
    ax2.set_yticks(np.arange(0, 1.1, 0.1))
    ax2.set_yticklabels([0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0], fontsize=10,
                        fontfamily='Times New Roman')
    for a, b in zip(range(10), np.array(typesChangeLA_Percent.sort_values(ascending=False).head(10).values)):
        ax2.text(a, b + 0.01, '%.2f' % b, ha='center', va='bottom', fontsize=7, fontfamily='Times New Roman')

    ax.set_xticks(list(range(topTypesNum)))
    ax.set_xticklabels(typesByChangeLASort[:topTypesNum], rotation=90, fontsize=10, fontfamily='Times New Roman')
    ax.set_ylabel('Change area($\mathregular{10^4km^2}$)', fontsize=10, fontfamily='Times New Roman')
    ax.set_ylim(0, )
    ax.set_yticklabels([0, 2, 4, 6, 8, 10, 12], fontsize=10,
                       fontfamily='Times New Roman')
    ax.legend(loc=7, bbox_to_anchor=(1, 0.4), prop=fontL, frameon=False)
    ax2.legend(loc=7, bbox_to_anchor=(1, 0.6), prop=fontL, frameon=False)
    # plt.title('Cumulative ratio of leaf area change in various types of Land Cover change',fontfamily='Times New Roman')
    plt.savefig(
        'D:\\OneDrive\\SharedFile\\GEE_V2\\showLUCC\\LUCC_ChangeOnTimeWithLAIchange_InLP_HotPotMKSen\\OnePic\\ChangeTypes_LA_ChangePercent.png',
        bbox_inches='tight')

    # --------------------------------------------------------------
    # Read Files
    dfOut2 = pd.DataFrame(
        columns=['Source', 'Target', 'Year', 'ChangeType', 'ChangeLAI'])
    fnPath2 = 'D:\\OneDrive\\SharedFile\\GEE_V2\\showLUCC\\LUCC_ChangeOnTimeWithLAIchange_InLP_HotPotMKSen\\OnePic\\LAIchange_InStudyArea_MKSen'
    filenames2 = os.listdir(fnPath2)
    for i, filename in enumerate(filenames2):
        thisYearData = pd.read_csv(fnPath2 + '\\' + filename)
        sourceLabel = thisYearData['Source'].map(mapList)
        targetLabel = thisYearData['Target'].map(mapList)
        thisYearData['SourceLabel'] = sourceLabel
        thisYearData['TargetLabel'] = targetLabel
        thisYearData['ChangeType'] = thisYearData['SourceLabel'] + ' to ' + thisYearData['TargetLabel']
        thisYearData = thisYearData.drop(
            ['system:index', '.geo', 'SourceLabel', 'TargetLabel'], axis=1)
        dfOut2 = dfOut2.append(thisYearData)
    dfOut2 = dfOut2.fillna(0)
    # --------------------------------------------------------------

    needShowTypes = list(typesByChangeLASort)[:topTypesNum]

    # typesChangeLAIGroupMeanAll = dfOut2.groupby('ChangeType')['ChangeLAI'].mean()
    # typesChangeLAIGroupMeanAll.to_csv(
    #     'D:\\OneDrive\\SharedFile\\GEE_V2\\showLUCC\\LUCC_ChangeOnTimeWithLAIchange_InLP_HotPotMKSen\\OnePic\\Annual_ChangeType_TypesChangeLAIGroupMeanAll.csv')

    topTypes = dfOut2[dfOut2['ChangeType'].isin(needShowTypes)]
    # 计算出每一类的平均LAI变化量
    typesChangeLAIGroupMean = topTypes.groupby('ChangeType')['ChangeLAI'].mean()
    typesChangeLAI = typesChangeLAIGroupMean.sort_values(ascending=False)
    # typesByChangeLAISort = list(typesChangeLAI.index)
    changeType_Index = range(topTypesNum)
    type_Index_Map = dict(map(lambda x, y: [x, y], typesByChangeLASort, changeType_Index))
    topTypes['ChangeType_Index'] = topTypes['ChangeType'].map(type_Index_Map)
    topTypes = topTypes.sort_values(by='ChangeType_Index', ascending=True)
    topTypes.to_csv(
        'D:\\OneDrive\\SharedFile\\GEE_V2\\showLUCC\\LUCC_ChangeOnTimeWithLAIchange_InLP_HotPotMKSen\\OnePic\\ChangeType_LAI_EveryYear.csv')
    typesChangeLAI.to_csv(
        'D:\\OneDrive\\SharedFile\\GEE_V2\\showLUCC\\LUCC_ChangeOnTimeWithLAIchange_InLP_HotPotMKSen\\OnePic\\ChangeType_LAI_Group.csv')

    fig = plt.figure(figsize=(13, 6), dpi=500)
    rectCB = [0, 0.99, 0.4, 0.45]
    rect1 = [0, 0.1, 0.55, 0.8]  # [左, 下, 宽, 高] 规定的矩形区域 （全部是0~1之间的数，表示比例）
    rect2 = [0.59, 0.1, 0.15, 0.8]
    rect3 = [0.74, 0.1, 0.15, 0.8]
    # ax1 = fig.add_subplot(121)

    ax11 = plt.axes(rect1)
    ax11.yaxis.tick_right()
    ax11.plot(range(topTypesNum), np.array(typesChangeLAFig['LAC_cumulative_per'].head(topTypesNum).values),
              color='#2C4063', linewidth=2.5, alpha=0.95, linestyle='-',
              label='Cumulative ratio of the change in leaf area to the total')
    # ax11.set_yticks(np.arange(0.0050, 0.03, 0.0025))
    # ax11.set_yticklabels(
    #     ['', '0.0075', '0.0100', '0.0125', '0.0150', '0.0175', '0.0200', '0.0225', '0.0250', '0.0275', ''], fontsize=10,
    #     fontfamily='Times New Roman')
    ax11.set_ylabel('Ratio', fontsize=14, fontfamily='Times New Roman')

    ax11.set_xlim(-1, topTypesNum)
    ax11.set_yticks(np.arange(0, 1.1, 0.1))
    ax11.set_yticklabels([0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0], fontsize=12,
                         fontfamily='Times New Roman')
    width = 0.4
    figIndex = np.arange(0, topTypesNum, 1)
    ax11.bar(x=figIndex - width / 2, height=np.array(typesChangeLAFig['ChangeLA_Percent'].head(topTypesNum).values),
             width=width,
             alpha=0.95, edgecolor='#3C6EC7', linewidth=0.8, color='#5DADEC',
             label='Ratio of the change in leaf area to the total')
    ax11.bar(x=figIndex + width / 2, height=np.array(typesChangeLAFig['ChangeArea_Percent'].head(topTypesNum).values),
             width=width,
             alpha=0.95, edgecolor='#5C2775', linewidth=0.8, color='#C9ADD3',
             label='Ratio of the area to the total')

    ax1 = ax11.twinx()

    # cm0 = plt.get_cmap('bwr')
    # cNorm0 = matplotlib.colors.Normalize(vmin=-0.5, vmax=0.5)
    cm0 = ListedColormap(['#F40000', '#FD7600', '#FACB01', '#FFE8A5', '#DFFFBF', '#D0FF73', '#4DE600', '#287201'])
    cNorm0 = BoundaryNorm([-0.4, -0.3, -0.2, -0.1, 0, 0.1, 0.2, 0.3, 0.4], cm0.N)
    axcolorbar = ax1.scatter(x=topTypes['ChangeType_Index'], y=topTypes['Year'], s=50, edgecolors='black',
                             linewidths=0.2,
                             c=topTypes['ChangeLAI'], norm=cNorm0, cmap=cm0)
    ax1.set_yticks(range(1987, 2019))
    ax1.set_yticklabels(range(1987, 2019), fontsize=12, fontfamily='Times New Roman')
    ax1.set_ylim(1986, 2019)
    ax11.set_xticks(changeType_Index)
    ax11.set_xticklabels(typesByChangeLASort, rotation=90, fontsize=12, fontfamily='Times New Roman')
    ax11.set_xlabel('Land Cover Change Types', fontsize=14, fontfamily='Times New Roman')
    # ax1.set_ylabel('Year', fontsize=12, fontfamily='Times New Roman')

    axCB = plt.axes(rectCB)
    axCB.spines['top'].set_visible(False)
    axCB.spines['right'].set_visible(False)
    axCB.spines['bottom'].set_visible(False)
    axCB.spines['left'].set_visible(False)
    cb = fig.colorbar(axcolorbar, ax=axCB, orientation='horizontal')
    # cb.set_ticks([-0.5, -0.4, -0.3, -0.2, -0.1, 0, 0.1, 0.2, 0.3, 0.4, 0.5])
    # cb.set_ticklabels([-0.5, -0.4, -0.3, -0.2, -0.1, 0, 0.1, 0.2, 0.3, 0.4, 0.5])
    for l in cb.ax.xaxis.get_ticklabels():
        l.set_family('Times New Roman')
        l.set_size(14)
    cb.set_label('Change of LAI in types of Land Cover change', fontsize=14, fontfamily='Times New Roman')

    tem = pd.read_csv(
        'D:\\OneDrive\\SharedFile\\GEE_V2\\showLUCC\\LUCC_ChangeOnTimeWithLAIchange_InLP_HotPotMKSen\\OnePic\\Change_ERA5_TEM_StudyArea.csv')
    pre = pd.read_csv(
        'D:\\OneDrive\\SharedFile\\GEE_V2\\showLUCC\\LUCC_ChangeOnTimeWithLAIchange_InLP_HotPotMKSen\\OnePic\\Change_ERA5_PRE_StudyArea.csv')
    pre['mean'] = pre['mean'].apply(lambda x: x * 1000)
    temMean = tem['mean'].mean()
    temChange = tem['mean'].apply(lambda x: x - temMean)
    preMean = pre['mean'].mean()
    preChange = pre['mean'].apply(lambda x: x - preMean)
    ax2 = plt.axes(rect2)
    # ax2 = fig.add_subplot(122)
    ax2.barh(tem['year'], temChange, color='darkorange', label='Annual anomaly of average air temperature at 2m height')
    # ax2.yaxis.tick_right()
    ax2.axvline(0, color='k', linewidth=0.5)
    ax2.set_yticks(range(1987, 2019))
    ax2.set_yticklabels([], fontsize=10, fontfamily='Times New Roman')
    ax2.set_ylim(1986, 2019)
    ax2.set_xticks(np.arange(-1, 1, 0.5))
    ax2.set_xticklabels(['-1', '-0.5', '0', '0.5', '1'], fontsize=12, fontfamily='Times New Roman')
    ax2.set_xlabel('Air temperature(K)', fontsize=14, fontfamily='Times New Roman')

    ax3 = plt.axes(rect3)
    ax3.barh(pre['year'], preChange, color='lightseagreen', label='Annual anomaly of total precipitation')
    ax3.yaxis.tick_right()
    ax3.axvline(0, color='k', linewidth=0.5)
    ax3.set_yticks([])
    ax3.set_yticklabels([], fontsize=10, fontfamily='Times New Roman')
    ax3.set_ylim(1986, 2019)
    ax3.set_xticks(np.arange(-50, 200, 50))
    ax3.set_xticklabels(['-50', '0', '50', '100', '150'], fontsize=12, fontfamily='Times New Roman')
    ax3.yaxis.set_label_position("right")
    # ax3.set_ylabel('Year', fontsize=12, fontfamily='Times New Roman')
    ax3.set_xlabel('Precipitation(mm)', fontsize=14, fontfamily='Times New Roman')

    ax11.legend(loc=8, bbox_to_anchor=(2, 0.2), prop=fontL, frameon=False)
    ax2.legend(loc=8, bbox_to_anchor=(3.4, 0.5), prop=fontL, frameon=False)
    ax3.legend(loc=8, bbox_to_anchor=(2.2, 0.8), prop=fontL, frameon=False)

    plt.savefig(
        'D:\\OneDrive\\SharedFile\\GEE_V2\\showLUCC\\LUCC_ChangeOnTimeWithLAIchange_InLP_HotPotMKSen\\OnePic\\PointHist.png',
        dpi=500, bbox_inches='tight')

    # out all records
    dfOut.to_csv(
        'D:\\OneDrive\\SharedFile\\GEE_V2\\showLUCC\\LUCC_ChangeOnTimeWithLAIchange_InLP_HotPotMKSen\\OnePic\\Annual_ChangeTypes_ALL.csv')
    print(time.strftime('%H:%M:%S', time.localtime(time.time())))


def cumulative_percent(percentData):
    """Return normalized cumulative distribution from discrete distribution."""
    cpf = []
    cpf.append(0.0)  # 赋初值0.0
    for i in range(0, len(percentData)):  # 遍历离散分布列表各元素
        cpf.append(cpf[i] + percentData[i])  # 前一累积分布值加上该点的概率
    return cpf


if __name__ == '__main__':
    main()
