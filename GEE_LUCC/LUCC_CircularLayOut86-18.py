# GEE LC YearsChangeKinds for network
# Get top 10 changes
# THRILLER柠檬
# thrillerlemon@outlook.com
# 2019年12月3日

import time
import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import warnings
import matplotlib.cbook

warnings.filterwarnings("ignore", category=matplotlib.cbook.mplDeprecation)


def drawlegend():
    print(time.strftime('%H:%M:%S', time.localtime(time.time())))

    labelMapList = {
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
    colorMapList = {
        101: '#78d203',
        102: '#05450a',
        103: '#086a10',
        201: '#dcd159',
        202: '#c6b044',
        301: '#b6ff05',
        302: '#54a708',
        401: '#c24f44',
        402: '#ff6d4c',
        501: '#d6b3b3',
        601: '#1c0dff',
        602: '#27ff87',
        603: '#69fff8',
        701: '#332b22',
        702: '#3b0434'
    }
    # Years
    fnPath = 'D:\\OneDrive\\SharedFile\\GEE_V2\\showLUCC\\LUCC_ChangeOnHex(86-18)\\'
    fnHead = 'KindChangeArea'
    fnTail = '.csv'

    plt.figure(figsize=(5, 5))
    G = nx.DiGraph()
    G.add_nodes_from(
        ['1', '2'])
    G.add_edge('1', '2', weight=10000000000, color='black')
    pos = nx.circular_layout(G)
    # area 2000平方千米 0.0000000005
    # rate
    nx.draw_networkx_edges(G, pos, width=[float(d['weight'] * 0.0000000005) for (u, v, d) in G.edges(data=True)],
                           edge_color='black', arrowsize=2)
    nx.draw_networkx_nodes(G, pos, node_size=1800)
    nx.draw_networkx_labels(G, pos, font_size=11, font_family='Times New Roman', font_color='w')
    plt.title('10000000000 m2')
    plt.savefig("C:\\Users\\thril\\Desktop\\legend.png", dpi=300)
    print('draw a year')


def main():
    print(time.strftime('%H:%M:%S', time.localtime(time.time())))

    labelMapList = {
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
    colorMapList = {
        101: '#78d203',
        102: '#05450a',
        103: '#086a10',
        201: '#dcd159',
        202: '#c6b044',
        301: '#b6ff05',
        302: '#54a708',
        401: '#c24f44',
        402: '#ff6d4c',
        501: '#d6b3b3',
        601: '#1c0dff',
        602: '#27ff87',
        603: '#69fff8',
        701: '#332b22',
        702: '#3b0434'
    }
    # Years
    fnPath = 'D:\\OneDrive\\SharedFile\\GEE_V2\\showLUCC\\LUCC_ChangeOnHex(86-18)\\'
    fnHead = 'KindChangeArea'
    fnTail = '.csv'

    plt.figure(figsize=(5, 5))
    G = nx.DiGraph()
    G.add_nodes_from(
        ['DBF', 'ENF', 'MF', 'Oshrub', 'Cshrub', 'XerGra', 'TemGra', 'Crop', 'Orchard', 'Builtup', 'Water', 'Wet',
         'Snow', 'Desert', 'Barren'])
    thisYearData = pd.read_csv(fnPath + fnHead + '1986_2018' + fnTail)
    sourceLabel = thisYearData['Source'].map(labelMapList)
    targetLabel = thisYearData['Target'].map(labelMapList)
    edgeColor = thisYearData['Source'].map(colorMapList)
    thisYearData['SourceLabel'] = sourceLabel
    thisYearData['TargetLabel'] = targetLabel
    thisYearData['EdgeColor'] = edgeColor
    thisYearData['ChangeType'] = thisYearData['SourceLabel'] + ' to ' + thisYearData['TargetLabel']
    # thisYearData = thisYearData.drop(
    #     ['system:index', '.geo'], axis=1)
    # print(thisYearData)
    for tIndex, tRow in thisYearData.iterrows():
        G.add_edge(tRow["SourceLabel"], tRow["TargetLabel"], weight=tRow["ChangeArea"], color=tRow["EdgeColor"])
    pos = nx.circular_layout(G)
    thisEdgeColors = [G[u][v]['color'] for u, v in G.edges()]
    # area 2000平方千米 0.0000000005
    # rate
    nx.draw_networkx_edges(G, pos, width=[float(d['weight'] * 0.0000000005) for (u, v, d) in G.edges(data=True)],
                           edge_color=thisEdgeColors, arrowsize=2, connectionstyle="arc3,rad=0.2")
    thisNodeColors = ['#78d203', '#05450a', '#086a10', '#dcd159', '#c6b044', '#b6ff05', '#54a708', '#c24f44',
                      '#ff6d4c', '#d6b3b3', '#1c0dff', '#27ff87', '#69fff8', '#332b22', '#3b0434']
    nx.draw_networkx_nodes(G, pos, node_size=1800, node_color=thisNodeColors)
    nx.draw_networkx_labels(G, pos, font_size=11, font_family='Times New Roman', font_color='w')
    # plt.title(str(year))
    # plt.show()
    # plt.legend()
    plt.savefig("C:\\Users\\thril\\Desktop\\86-18.png", dpi=300)
    print('draw a year')


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
