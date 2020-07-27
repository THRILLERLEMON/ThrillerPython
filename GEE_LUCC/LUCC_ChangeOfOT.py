# GEE LC LUCC_ChangeOfPixelsInSevenTimePoint
# THRILLER柠檬
# thrillerlemon@outlook.com
# 2020年07月04日

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
    fnPath = 'D:\\OneDrive\\SharedFile\\GEE_V2\\showLUCC\\OTChange\\'
    fnHead = 'Change_TransitionNetWork'
    fnTail = '.csv'

    kindName = ['Forests', 'Shrublands', 'Grasslands', 'Croplands', 'Orchard and Terrace', 'Urban and Built-up',
                'Water Bodies', 'Desert and Low-vegetated lands']
    kindColor = ['#1B7201', '#50FF00', '#A4D081', '#F2F100', '#F29B00', '#F00001', '#0058F0', '#9F9F9F']
    colorMapList = dict(map(lambda x, y: [x, y], kindName, kindColor))

    nodeData = pd.read_csv(fnPath + 'ChangeInTimePoint_Area' + fnTail, index_col='Year')

    plt.figure(figsize=(6, 9), dpi=500)
    G = nx.DiGraph()
    for nameN in np.arange(0, 8):
        areaPer = nodeData[kindName[nameN]][1986] / nodeData.ix[1986].sum()
        G.add_node(kindName[nameN] + '_' + str(1986), area=nodeData[kindName[nameN]][1986] * 0.000000007,
                   area2=round(nodeData[kindName[nameN]][1986] * 0.0000000001, 2),
                   areaPer=str(str(int(areaPer * 100)) + '%'),
                   pos=(0.1, (nameN + 1) * 0.1), color=kindColor[nameN])

    years = [1986, 2009, 2013, 2018]
    for yearN in np.arange(1, 4):
        sourceYear = years[yearN - 1]
        targetYear = years[yearN]
        changeData = pd.read_csv(fnPath + fnHead + str(sourceYear) + '_' + str(targetYear) + fnTail)

        for nameN in np.arange(0, 8):
            areaPer = nodeData[kindName[nameN]][targetYear] / nodeData.ix[targetYear].sum()
            G.add_node(kindName[nameN] + '_' + str(targetYear),
                       area=nodeData[kindName[nameN]][targetYear] * 0.000000007,
                       # 104km2
                       area2=round(nodeData[kindName[nameN]][targetYear] * 0.0000000001, 2),
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
        sizeN = ((int(sizeNOLD) - 5) / 3)
        if sizeN < 10:
            sizeN = 10
        nx.draw_networkx_labels(g, nx.get_node_attributes(g, 'pos'), labels=nx.get_node_attributes(g, 'area2'),
                                font_size=sizeN, font_family='Times New Roman', font_color='k')
    thisEdgeColors = [G[u][v]['color'] for u, v in G.edges()]
    weight = []
    for (u, v, d) in G.edges(data=True):
        pweight = d['weight']
        if pweight > 7E10:
            weight.append(7E10 * 0.0000000001)
            continue
        weight.append(pweight * 0.0000000001)
    # weight=float(d['weight'] * 0.0000000001) for (u, v, d) in G.edges(data=True)
    nx.draw_networkx_edges(G, pos, width=weight,
                           edge_color=thisEdgeColors, arrowsize=3, connectionstyle="arc3,rad=-0.05", alpha=0.98,
                           style='solid')
    # nx.draw_networkx_labels(G, pos, font_size=5, font_family='Times New Roman', font_color='black')
    # plt.show()
    plt.axis('off')
    plt.savefig(fnPath + "CN.png")

    print(time.strftime('%H:%M:%S', time.localtime(time.time())))


if __name__ == '__main__':
    main()
