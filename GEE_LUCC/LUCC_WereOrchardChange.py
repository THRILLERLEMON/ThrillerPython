# GEE LC WereOrchardChange
# THRILLER柠檬
# thrillerlemon@outlook.com
# 2020年05月25日

import time
import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import warnings
import matplotlib.cbook

warnings.filterwarnings("ignore", category=matplotlib.cbook.mplDeprecation)


def main():
    print(time.strftime('%H:%M:%S', time.localtime(time.time())))
    fnPath = 'D:\\OneDrive\\SharedFile\\GEE_V2\\WereOrchardChange\\'
    fnHead = 'WereOrchardKindChangeArea'
    fnTail = '.csv'

    kindName = ['Other', 'Grasslands', 'Orchard and Terrace', 'Forests', 'Croplands']
    kindColor = ['#9f9f9f', '#4d86bd', '#f6903c', '#58a95a', '#d12026']
    colorMapList = dict(map(lambda x, y: [x, y], kindName, kindColor))

    nodeData = pd.read_csv(fnPath + 'WereOrchardChangeArea' + fnTail, index_col='Year')

    plt.figure(figsize=(9, 4.5), dpi=500)
    G = nx.DiGraph()
    for nameN in np.arange(0, 5):
        areaPer = nodeData[kindName[nameN]][1986] / nodeData.ix[1986].sum()
        G.add_node(kindName[nameN] + '_' + str(1986), area=nodeData[kindName[nameN]][1986] * 0.000000013,
                   areaPer=str(str(int(areaPer * 100)) + '%'),
                   pos=(0.1, (nameN + 1) * 0.1), color=kindColor[nameN])

    years = [1986, 1995, 2000, 2005, 2010, 2015, 2018]
    for yearN in np.arange(1, 7):
        sourceYear = years[yearN - 1]
        targetYear = years[yearN]
        changeData = pd.read_csv(fnPath + fnHead + str(sourceYear) + '_' + str(targetYear) + fnTail)

        for nameN in np.arange(0, 5):
            areaPer = nodeData[kindName[nameN]][targetYear] / nodeData.ix[targetYear].sum()
            G.add_node(kindName[nameN] + '_' + str(targetYear),
                       area=nodeData[kindName[nameN]][targetYear] * 0.000000013,
                       areaPer=str(str(int(areaPer * 100)) + '%'),
                       pos=(yearN * 0.1 + 0.1, (nameN + 1) * 0.1), color=kindColor[nameN])
        changeData['SourceLabel'] = changeData['Source'] + '_' + str(sourceYear)
        changeData['TargetLabel'] = changeData['Target'] + '_' + str(targetYear)
        changeData['EdgeColor'] = changeData['Source'].map(colorMapList)
        for tIndex, tRow in changeData.iterrows():
            G.add_edge(tRow["SourceLabel"], tRow["TargetLabel"], weight=tRow["ChangeArea"], color=tRow["EdgeColor"])
    pos = nx.get_node_attributes(G, 'pos')
    color = nx.get_node_attributes(G, 'color')
    size = nx.get_node_attributes(G, 'area').values()
    nx.draw_networkx_nodes(G, pos, node_color=color.values(), node_size=list(size), alpha=0.98, edgecolors='#2E2E2E',
                           linewidths=0.6)
    for i, node in enumerate(G.nodes(data=True)):
        g = G.subgraph([node[0]])
        areaPer = node[1]['areaPer']
        sizeNOLD = areaPer[0:len(areaPer) - 1]
        sizeN = ((int(sizeNOLD) - 5) / 70) * 18
        if sizeN < 8:
            sizeN = 7
        nx.draw_networkx_labels(g, nx.get_node_attributes(g, 'pos'), labels=nx.get_node_attributes(g, 'areaPer'),
                                font_size=sizeN, font_family='Times New Roman', font_color='k')
    thisEdgeColors = [G[u][v]['color'] for u, v in G.edges()]
    nx.draw_networkx_edges(G, pos, width=[float(d['weight'] * 0.00000000013) for (u, v, d) in G.edges(data=True)],
                           edge_color=thisEdgeColors, arrowsize=3, connectionstyle="arc3,rad=-0.05", alpha=0.98,
                           style='solid')
    # nx.draw_networkx_labels(G, pos, font_size=5, font_family='Times New Roman', font_color='black')
    # plt.show()
    plt.savefig(fnPath + "CN.png")

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
