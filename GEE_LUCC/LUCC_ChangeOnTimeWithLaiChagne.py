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
        201: 'Lgrass',
        202: 'Shrub',
        301: 'Mgrass',
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
    # 各类33年总的LA增加或者减少（不是绝对值）
    typesChangeLAtotal = dfOut.groupby('ChangeType')['ChangeLA'].sum()
    dfOut['ChangeLA_ABS'] = dfOut['ChangeLA'].abs()
    dfOut['ChangeLA_Percent'] = dfOut['ChangeLA_ABS'] / dfOut['ChangeLA_ABS'].sum(axis=0)
    # 各类别变化占比,变化的绝对值
    typesChangeLAabsTotal=dfOut.groupby('ChangeType')['ChangeLA_ABS'].sum()
    typesChangeLA_Percent=typesChangeLAabsTotal/ dfOut['ChangeLA_ABS'].sum(axis=0)
    typesChangeLA_Percent=typesChangeLA_Percent.sort_values(ascending=False)
    typesByChangeLASort=list(typesChangeLA_Percent.index)
    # 画累计百分比分布图
    plt.figure(figsize=(12, 5), dpi=300)
    cpfTypes=cumulative_percent(typesChangeLA_Percent)
    typesChangeLAFig = pd.DataFrame([typesChangeLA_Percent, pd.Series(cpfTypes[1:], index=typesChangeLA_Percent.index),typesChangeLAtotal])
    typesChangeLAFig = pd.DataFrame(typesChangeLAFig.values.T, index=typesChangeLAFig.columns, columns=typesChangeLAFig.index)
    typesChangeLAFig.to_csv(
        'D:\\OneDrive\\SharedFile\\GEE_V2\\showLUCC\\LUCC_ChangeOnTimeWithLAIchange_InLP_HotPot\\ChangeTypes_LA_ChangePercent.csv')
    plt.bar(x=range(41), height=np.array(cpfTypes[:41]))
    # plt.bar(x=range(len(typesByChangeLASort)+1), height=np.array(cpfTypes[:40]))
    # plt.xticks(list(range(len(typesByChangeLASort)+1)), [' ']+typesByChangeLASort, rotation=90,fontsize=5)
    plt.xlabel('Land Cover change Types',fontsize=10,fontfamily='Times New Roman')
    plt.ylabel('Ratio',fontsize=10,fontfamily='Times New Roman')
    plt.xticks(list(range(41)), [' ']+typesByChangeLASort[:40], rotation=90,fontsize=10,fontfamily='Times New Roman')
    plt.yticks(np.arange(0,1.1,0.1),fontsize=10,fontfamily='Times New Roman')
    for a, b in zip(range(41), np.array(cpfTypes[:41])):
        plt.text(a, b+0.01, '%.2f' % b, ha='center', va='bottom',fontsize=8,fontfamily='Times New Roman')
    plt.title('Cumulative ratio of leaf area change in various types of Land Cover change',fontfamily='Times New Roman')
    plt.savefig('D:\\OneDrive\\SharedFile\\GEE_V2\\showLUCC\\LUCC_ChangeOnTimeWithLAIchange_InLP_HotPot\\ChangeTypes_LA_ChangePercent.png',bbox_inches='tight')


    # 假设只绘出LA变化量最大的前40种类型
    topTypesNum=40
    needShowTypes=list(typesByChangeLASort)[:topTypesNum]
    topTypes= dfOut[dfOut['ChangeType'].isin(needShowTypes)]
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
    ax=topTypes.plot.scatter(figsize=(10,5),x='ChangeType_Index', y='ChangeLA_UnitArea',ylim=[-0.6,0.6],s=12,c=topTypes['Year'],secondary_y=True)
    # ax=topTypes.plot.scatter(figsize=(10,5),x='ChangeType_Index', y='ChangeLA_UnitArea',ylim=[-0.6,0.6],s=10,c=topTypes['Year'],norm=cNorm, cmap=cm,secondary_y=True)

    def mul10(x):
        return x*0.1

    secaxy = ax.secondary_yaxis('right',functions=(mul10,mul10))
    secaxy.set_ylabel('Years mean change of leaf area per unit area($\mathregular{m^2}$)',fontsize=12,fontfamily='Times New Roman')
    secaxy.set_color('darkorange')
    secaxy.set_yticks(np.arange(-0.06,0.06,0.01))

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
    typesByChangeLA_UnitAreaSort=list(typesChangeLA_UnitArea.index)
    changeType_Index = range(topTypesNum)
    type_Index_Map = dict(map(lambda x, y: [x, y], typesByChangeLA_UnitAreaSort, changeType_Index))
    topTypes['ChangeType_Index'] = topTypes['ChangeType'].map(type_Index_Map)
    topTypes=topTypes.sort_values(by='ChangeType_Index',ascending=True)
    topTypes.to_csv(
        'D:\\OneDrive\\SharedFile\\GEE_V2\\showLUCC\\LUCC_ChangeOnTimeWithLAIchange_InLP_HotPot\\Annual_ChangeType_LA_Change_UnitArea_ByLAUnitAreaMean.csv')

    # topTypes.plot.scatter(figsize=(10,5),x='ChangeType_Index', y='ChangeLA_UnitArea',s=10,c=topTypes['Year'],norm=cNorm, cmap=cm)

    ###
    ax=topTypes.plot.scatter(figsize=(12,5),x='ChangeType_Index', y='ChangeLA_UnitArea',ylim=[-0.6,0.6],s=12,c=topTypes['Year'],norm=cNorm, cmap=cm,secondary_y=True,legend=False)



    def mul10(x):
        return x*0.1
    secaxy = ax.secondary_yaxis('right',functions=(mul10,mul10))
    secaxy.set_ylabel('mean',fontsize=10,fontfamily='Times New Roman')
    secaxy.set_color('darkorange')
    ax.plot(range(topTypesNum),list(typesChangeLA_UnitAreaGroupMul10.sort_values(ascending=False)),color='darkorange')
    ####
    plt.xticks(changeType_Index, typesByChangeLA_UnitAreaSort, rotation=90,fontsize=10,fontfamily='Times New Roman')
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
