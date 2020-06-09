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


def main():
    print(time.strftime('%H:%M:%S', time.localtime(time.time())))
    mapList = {
        101: 'DBF',
        102: 'ENF',
        103: 'MF',
        201: 'Mgrass',
        202: 'Shrub',
        301: 'Lgrass',
        302: 'Hgrass',
        401: 'Crop',
        402: 'Orchard',
        501: 'Builtup',
        601: 'Water',
        602: 'Wet',
        603: 'Snow',
        701: 'Desert',
        702: 'Barren',
    }

    dfOut = pd.DataFrame(columns=['Source', 'Target', 'Year','ChangeType','ChangeArea','ChangeLA','ChangeLA_UnitArea'])

    font = {'family': 'Times New Roman',
            # 'style': 'italic',
            'weight': 'normal',
            'color': 'b',
            'size': 10,
            }

    # Read Files
    fnPath = 'D:\\OneDrive\\SharedFile\\GEE_V2\\showLUCC\\LUCC_ChangeOnTimeWithLAIchange_InLP_HotPot\\CSVs'
    filenames = os.listdir(fnPath)
    for i, filename in enumerate(filenames):
        thisYearData = pd.read_csv(fnPath+'\\'+filename)
        sourceLabel = thisYearData['Source'].map(mapList)
        targetLabel = thisYearData['Target'].map(mapList)
        thisYearData['SourceLabel'] = sourceLabel
        thisYearData['TargetLabel'] = targetLabel
        thisYearData['ChangeType'] = thisYearData['SourceLabel'] + ' to ' + thisYearData['TargetLabel']
        thisYearData['ChangeLA_UnitArea'] = thisYearData['ChangeLA'] / thisYearData['ChangeArea']
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
    PaA = pd.DataFrame({'ChangeLA_Percent': typesChangeLA_Percent, 'ChangeAreaMean': typesChangeAreaMean})
    PaA = PaA.sort_values(by='ChangeLA_Percent', ascending=False)
    typesByChangeLASort = list(PaA.index)

    # 假设只绘出LA变化量最大的前37种类型
    topTypesNum = 37

    # 画累计百分比分布图
    fig = plt.figure(figsize=(12, 5), dpi=500)
    ax = fig.add_subplot(111)
    cpfTypes = cumulative_percent(typesChangeLA_Percent.sort_values(ascending=False))
    typesChangeLAFig = pd.DataFrame(
        [PaA['ChangeLA_Percent'], PaA['ChangeAreaMean'], pd.Series(cpfTypes[1:], index=PaA.index), typesChangeLAtotal])
    typesChangeLAFig = pd.DataFrame(typesChangeLAFig.values.T, index=typesChangeLAFig.columns,
                                    columns=typesChangeLAFig.index)
    typesChangeLAFig.to_csv(
        'D:\\OneDrive\\SharedFile\\GEE_V2\\showLUCC\\LUCC_ChangeOnTimeWithLAIchange_InLP_HotPot\\ChangeTypes_LA_ChangePercent.csv')

    ax2 = ax.twinx()
    ax2.plot(range(topTypesNum), typesChangeLAFig['ChangeAreaMean'].head(topTypesNum), color='lightcoral')

    ax.plot(range(topTypesNum), np.array(cpfTypes[1:topTypesNum + 1]), linewidth=1, linestyle='-', marker='o', ms=2,
            color='k')
    ax.bar(x=range(topTypesNum),
           height=np.array(typesChangeLA_Percent.sort_values(ascending=False).head(topTypesNum).values),
           color='cornflowerblue')

    # secaxy = aax.secondary_yaxis('right')
    # secaxy.set_ylabel('Change area($\mathregular{m^2}$)',fontsize=12,fontfamily='Times New Roman')
    # secaxy.set_color('darkorange')

    # plt.bar(x=range(len(typesByChangeLASort)+1), height=np.array(cpfTypes[:40]))
    # plt.xticks(list(range(len(typesByChangeLASort)+1)), [' ']+typesByChangeLASort, rotation=90,fontsize=5)
    ax.set_xlabel('Land Cover change Types', fontsize=10, fontfamily='Times New Roman')
    ax.set_ylabel('Cumulative Ratio', fontsize=10, fontfamily='Times New Roman')
    ax.set_xticks(list(range(topTypesNum)))
    ax.set_xticklabels(typesByChangeLASort[:topTypesNum], rotation=90, fontsize=10, fontfamily='Times New Roman')
    ax.set_xlim(-1, topTypesNum)
    ax.set_yticks(np.arange(0, 1.1, 0.1))
    ax.set_yticklabels([0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0], fontsize=10,
                       fontfamily='Times New Roman')
    for a, b in zip(range(topTypesNum),
                    np.array(typesChangeLA_Percent.sort_values(ascending=False).head(topTypesNum).values)):
        ax.text(a, b + 0.01, '%.2f' % b, ha='center', va='bottom', fontsize=8, fontfamily='Times New Roman')

    ax2.set_ylabel('Mean change area of years($\mathregular{10^4km^2}$)', fontsize=10, fontfamily='Times New Roman')
    ax2.set_yticklabels([0, 0, 2, 4, 6, 8], fontsize=10,
                        fontfamily='Times New Roman')
    # plt.title('Cumulative ratio of leaf area change in various types of Land Cover change',fontfamily='Times New Roman')
    plt.savefig(
        'D:\\OneDrive\\SharedFile\\GEE_V2\\showLUCC\\LUCC_ChangeOnTimeWithLAIchange_InLP_HotPot\\ChangeTypes_LA_ChangePercent.png',
        bbox_inches='tight')

    needShowTypes = list(typesByChangeLASort)[:topTypesNum]
    topTypes = dfOut[dfOut['ChangeType'].isin(needShowTypes)]
    # 计算出每一类的单位面积被的LA变化量
    typesChangeLA_UnitAreaGroupMean = topTypes.groupby('ChangeType')['ChangeLA_UnitArea'].mean()
    typesChangeLA_UnitAreaGroupMul10 = topTypes.groupby('ChangeType')['ChangeLA_UnitArea'].mean().multiply(10)
    # typesChangeLA_UnitAreaGroupMul10 = topTypes.groupby('ChangeType')['ChangeLA_UnitArea'].quantile(0.8)
    cm = plt.get_cmap('cool')
    cNorm = matplotlib.colors.Normalize(vmin=1987, vmax=2018)
    # 画散点图===根据LA变化量排序
    changeType_Index = range(topTypesNum)
    type_Index_Map = dict(map(lambda x, y: [x, y], needShowTypes, changeType_Index))
    topTypes['ChangeType_Index'] = topTypes['ChangeType'].map(type_Index_Map)
    topTypes=topTypes.sort_values(by='ChangeType_Index',ascending=True)
    topTypes.to_csv(
        'D:\\OneDrive\\SharedFile\\GEE_V2\\showLUCC\\LUCC_ChangeOnTimeWithLAIchange_InLP_HotPot\\Annual_ChangeType_LA_Change_UnitArea_ByLAChange.csv')
    # plt.scatter(x=topTypes['ChangeType_Index'],y=topTypes['ChangeLA_UnitArea'],s=10,c=topTypes['Year'],norm=cNorm, cmap=cm)
    ax = topTypes.plot.scatter(figsize=(11, 5), x='ChangeType_Index', y='ChangeLA_UnitArea', ylim=[-0.5, 0.5], s=12,
                               c=topTypes['Year'], secondary_y=True)
    # ax=topTypes.plot.scatter(figsize=(10,5),x='ChangeType_Index', y='ChangeLA_UnitArea',ylim=[-0.6,0.6],s=10,c=topTypes['Year'],norm=cNorm, cmap=cm,secondary_y=True)

    def mul10(x):
        return x*0.1

    secaxy = ax.secondary_yaxis('right',functions=(mul10,mul10))
    secaxy.set_ylabel('Years mean change of leaf area per unit area($\mathregular{m^2}$)',fontsize=12,fontfamily='Times New Roman')
    secaxy.set_color('darkorange')
    secaxy.set_yticks(np.arange(-0.05, 0.05, 0.01))

    lineData = pd.DataFrame({"type": needShowTypes})
    lineData_Index_Map = dict(map(lambda x, y: [x, y], list(typesChangeLA_UnitAreaGroupMul10.index), list(typesChangeLA_UnitAreaGroupMul10.values)))
    lineData['Mul10']=lineData['type'].map(lineData_Index_Map)

    ax.plot(range(topTypesNum),list(lineData['Mul10']),color='darkorange')
    plt.xticks(changeType_Index, needShowTypes, rotation=90,fontsize=12,fontfamily='Times New Roman')
    plt.title('Change of leaf area per unit area in various types of Land Cover change',fontsize=12,fontfamily='Times New Roman')

    # plt.show()
    plt.savefig('D:\\OneDrive\\SharedFile\\GEE_V2\\showLUCC\\LUCC_ChangeOnTimeWithLAIchange_InLP_HotPot\\Annual_ChangeType_LA_Change_UnitArea_ByLAChange.png',dpi=300,bbox_inches='tight')


    # 画散点图===根据单位面积的LA变化量排序
    typesChangeLA_UnitArea=typesChangeLA_UnitAreaGroupMean.sort_values(ascending=False)
    typesByChangeLA_UnitAreaSort = list(typesChangeLA_UnitArea.index)
    changeType_Index = range(topTypesNum)
    type_Index_Map = dict(map(lambda x, y: [x, y], typesByChangeLA_UnitAreaSort, changeType_Index))
    topTypes['ChangeType_Index'] = topTypes['ChangeType'].map(type_Index_Map)
    topTypes = topTypes.sort_values(by='ChangeType_Index', ascending=True)
    topTypes.to_csv(
        'D:\\OneDrive\\SharedFile\\GEE_V2\\showLUCC\\LUCC_ChangeOnTimeWithLAIchange_InLP_HotPot\\Annual_ChangeType_LA_Change_UnitArea_ByLAUnitAreaMean.csv')

    # topTypes.plot.scatter(figsize=(10,5),x='ChangeType_Index', y='ChangeLA_UnitArea',s=10,c=topTypes['Year'],norm=cNorm, cmap=cm)

    ### 每种转化类型按照时间绘制曲线
    fig = plt.figure(figsize=(11, 5), dpi=300)
    ax = fig.add_subplot(111)
    for type in typesByChangeLA_UnitAreaSort:
        thisType = topTypes[topTypes['ChangeType'] == type]
        ax.plot(np.arange(1987, 2019, 1), list(thisType['ChangeLA_UnitArea']))
    plt.savefig(
        'D:\\OneDrive\\SharedFile\\GEE_V2\\showLUCC\\LUCC_ChangeOnTimeWithLAIchange_InLP_HotPot\\Annual_ChangeType_LA_Change_UnitArea_Lines.png',
        dpi=300, bbox_inches='tight')

    ### 更换纵坐标和颜色的值，绘图，横坐标为转换类型，纵坐标为时间、颜色为平均LA变化值
    # cm0 = plt.get_cmap('bwr')
    # cNorm0 = matplotlib.colors.Normalize(vmin=-0.5, vmax=0.5)
    # ax0 = topTypes.plot.scatter(figsize=(11, 5), x='ChangeType_Index', y='Year',  s=25,edgecolors='black',linewidths=0.1,
    #                            c=topTypes['ChangeLA_UnitArea'], norm=cNorm0, cmap=cm0, secondary_y=True, legend=False)
    # plt.yticks(range(1987,2019),fontsize=10,fontfamily='Times New Roman')
    # plt.xticks(changeType_Index, typesByChangeLA_UnitAreaSort, rotation=90,fontsize=10,fontfamily='Times New Roman')
    # plt.savefig('D:\\OneDrive\\SharedFile\\GEE_V2\\showLUCC\\LUCC_ChangeOnTimeWithLAIchange_InLP_HotPot\\Hist2d.png',dpi=300,bbox_inches='tight')

    fig = plt.figure(figsize=(14, 6), dpi=500)
    rect1 = [0, 0.1, 0.6, 0.8]  # [左, 下, 宽, 高] 规定的矩形区域 （全部是0~1之间的数，表示比例）
    rect2 = [0.7, 0.1, 0.14, 0.8]
    rect3 = [0.84, 0.1, 0.14, 0.8]
    # ax1 = fig.add_subplot(121)
    ax1 = plt.axes(rect1)
    cm0 = plt.get_cmap('bwr')
    cNorm0 = matplotlib.colors.Normalize(vmin=-0.5, vmax=0.5)
    ax1.scatter(x=topTypes['ChangeType_Index'], y=topTypes['Year'], s=40, edgecolors='black', linewidths=0.2,
                c=topTypes['ChangeLA_UnitArea'], norm=cNorm0, cmap=cm0)
    ax1.set_yticks(range(1987, 2019))
    ax1.set_yticklabels(range(1987, 2019), fontsize=10, fontfamily='Times New Roman')
    ax1.set_ylim(1986, 2019)
    ax1.set_xticks(changeType_Index)
    ax1.set_xticklabels(typesByChangeLA_UnitAreaSort, rotation=90, fontsize=10, fontfamily='Times New Roman')
    ax1.set_xlabel('Land Cover change Types', fontsize=12, fontfamily='Times New Roman')
    ax1.set_ylabel('Change of leaf area index in types of Land Cover change', fontsize=12, fontfamily='Times New Roman')
    ax11 = ax1.twinx()
    ax11.plot(range(topTypesNum), list(typesChangeLA_UnitAreaGroupMean.sort_values(ascending=False)), color='limegreen',
              label='Years mean change of leaf area index in types change')
    ax11.set_yticks(np.arange(0.0050, 0.0275, 0.0025))
    ax11.set_yticklabels(['', '0.0075', '0.0100', '0.0125', '0.0150', '0.0175', '0.0200', '0.0225', '0.0250', ''],
                         fontsize=10, fontfamily='Times New Roman')
    ax11.set_ylabel('Change of leaf area index($\mathregular{m^2/m^2}$)', fontsize=12,
                    fontfamily='Times New Roman')

    # ax11.set_ylabel('Change of leaf area per unit area($\mathregular{m^2}$)', fontsize=12, fontfamily='Times New Roman')

    tem = pd.read_csv(
        'D:\\OneDrive\\SharedFile\\GEE_V2\\showLUCC\\LUCC_ChangeOnTimeWithLAIchange_InLP_HotPot\\Change_ERA5_TEM.csv')
    pre = pd.read_csv(
        'D:\\OneDrive\\SharedFile\\GEE_V2\\showLUCC\\LUCC_ChangeOnTimeWithLAIchange_InLP_HotPot\\Change_ERA5_PRE.csv')
    pre['mean'] = pre['mean'].apply(lambda x: x * 1000)
    temMean = tem['mean'].mean()
    temChange = tem['mean'].apply(lambda x: x - temMean)
    preMean = pre['mean'].mean()
    preChange = pre['mean'].apply(lambda x: x - preMean)
    ax2 = plt.axes(rect2)
    # ax2 = fig.add_subplot(122)
    ax2.barh(tem['year'], temChange, color='darkorange', label='Average air temperature at 2m height')
    ax2.yaxis.tick_right()
    ax2.axvline(0, color='k', linewidth=0.5)
    ax2.set_yticks(range(1987, 2019))
    # ax2.set_yticklabels(range(1987,2019),fontsize=10,fontfamily='Times New Roman')
    ax2.set_ylim(1986, 2019)
    ax2.set_xticks(np.arange(-1, 1, 0.5))
    # ax2.set_xticklabels(['','280.5','281.0','281.5','282.0','282.5', ''], fontsize=10,fontfamily='Times New Roman')
    ax2.set_xlabel('Air temperature(K)', fontsize=12, fontfamily='Times New Roman')

    ax3 = plt.axes(rect3)
    ax3.barh(pre['year'], preChange, color='lightseagreen', label='Total precipitation')
    ax3.yaxis.tick_right()
    ax3.axvline(0, color='k', linewidth=0.5)
    ax3.set_yticks(range(1987, 2019))
    ax3.set_yticklabels(range(1987, 2019), fontsize=10, fontfamily='Times New Roman')
    ax3.set_ylim(1986, 2019)
    ax3.set_xticks(np.arange(-100, 150, 50))
    # ax3.set_xticklabels(['','0.040','0.045','0.050','0.055','0.060',''], fontsize=10,fontfamily='Times New Roman')
    ax3.set_xlabel('Precipitation(mm)', fontsize=12, fontfamily='Times New Roman')

    ax11.legend(loc=8, bbox_to_anchor=(2, 0.2), borderaxespad=0.)
    ax2.legend(loc=8, bbox_to_anchor=(3.2, 0.5), borderaxespad=0.)
    ax3.legend(loc=8, bbox_to_anchor=(2, 0.8), borderaxespad=0.)

    plt.savefig('D:\\OneDrive\\SharedFile\\GEE_V2\\showLUCC\\LUCC_ChangeOnTimeWithLAIchange_InLP_HotPot\\Hist2d.png',
                dpi=300, bbox_inches='tight')

    ###
    ax = topTypes.plot.scatter(figsize=(11, 5), x='ChangeType_Index', y='ChangeLA_UnitArea', ylim=[-0.5, 0.5], s=12,
                               c=topTypes['Year'], norm=cNorm, cmap=cm, secondary_y=True, legend=False)

    def mul10(x):
        return x * 0.1

    secaxy = ax.secondary_yaxis('right', functions=(mul10, mul10))
    secaxy.set_ylabel('mean', fontsize=10, fontfamily='Times New Roman')
    secaxy.set_color('darkorange')
    ax.plot(range(topTypesNum), list(typesChangeLA_UnitAreaGroupMul10.sort_values(ascending=False)), color='lawngreen')
    ####
    plt.xticks(changeType_Index, typesByChangeLA_UnitAreaSort, rotation=90, fontsize=10, fontfamily='Times New Roman')
    # plt.yticks(np.arange(-0.6, 0.6, 0.1), fontsize=12, fontfamily='Times New Roman')
    plt.xlabel('Land Cover change Types',fontsize=12,fontfamily='Times New Roman')
    plt.ylabel('Change of leaf area per unit area($\mathregular{m^2}$)',fontsize=12,fontfamily='Times New Roman')

    plt.title('Change of leaf area per unit area in various types of Land Cover change',fontsize=12,fontfamily='Times New Roman')
    # plt.show()
    plt.savefig('D:\\OneDrive\\SharedFile\\GEE_V2\\showLUCC\\LUCC_ChangeOnTimeWithLAIchange_InLP_HotPot\\Annual_ChangeType_LA_Change_UnitArea_ByLAUnitAreaMean.png',dpi=300,bbox_inches='tight')


    # out all records
    dfOut.to_csv(
        'D:\\OneDrive\\SharedFile\\GEE_V2\\showLUCC\\LUCC_ChangeOnTimeWithLAIchange_InLP_HotPot\\Annual_ChangeType_with_LA_Change_UnitArea_ALL.csv')
    print(time.strftime('%H:%M:%S', time.localtime(time.time())))

def cumulative_percent(percentData):
    """Return normalized cumulative distribution from discrete distribution."""
    cpf=[]
    cpf.append(0.0) #赋初值0.0
    for i in range(0,len(percentData)): #遍历离散分布列表各元素
        cpf.append(cpf[i]+percentData[i]) #前一累积分布值加上该点的概率
    return cpf

if __name__ == '__main__':
    main()
