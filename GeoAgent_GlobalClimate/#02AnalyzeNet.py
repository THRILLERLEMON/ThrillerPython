# -*- coding: utf-8 -*-
# @Time    : 2019/11/6 00:00
# @Author  : THRILLER柠檬
# @Email   : thrillerlemon@outlook.com
# @File    : #02AnalyzeNet.py
# @Software: PyCharm
# GeoAgentModel
# 02AnalyzeNetwork

import time

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import networkx as nx
from mpl_toolkits.basemap import Basemap as Basemap

outPutPath = 'C:\\Users\\thril\\Desktop\\'


def main():
    # ******Main******
    print(time.strftime('%H:%M:%S', time.localtime(time.time())))
    geoAgentSHPpath = 'D:\\OneDrive\\SharedFile\\环境经济社会可持续发展耦合网络模型\\GeoAgent_GlobalClimate\\GlobalClimate_SHPGeoAgent'
    geoAgentInfopath = 'D:\\OneDrive\\SharedFile\\环境经济社会可持续发展耦合网络模型\\GeoAgent_GlobalClimate\\PointInfo.csv'
    geoLinkspath = 'D:\\OneDrive\\SharedFile\\环境经济社会可持续发展耦合网络模型\\GeoAgent_GlobalClimate\\geoLinks1118.csv'
    allLinks = pd.read_csv(geoLinkspath, index_col=0, header=0, dtype={'Source': np.int32, 'Target': np.int32})
    allNodes = pd.read_csv(geoAgentInfopath, header=0, dtype={'label': np.int32})
    # print(allLinks)

    varList = {'Tem', 'Prs', 'Pre'}

    for var in varList:
        for secvar in varList:
            NetG = build2VarNetWork(
                allNodesData=allNodes,
                allLinksData=allLinks,
                VarSou=var,
                VarTar=secvar,
                weightQuota='Cij')
            drawNetWorkOnMap(
                showOrSave='save',
                netWorkG=NetG,
                geoAgentShpPath=geoAgentSHPpath,
                edgeColorF='weight',
                nodeColorF='tem_skew_mean')

    print(time.strftime('%H:%M:%S', time.localtime(time.time())))


# SubFunction
def build2VarNetWork(allNodesData, allLinksData, VarSou, VarTar, weightQuota):
    """
    @param allNodesData: allNodesData pandas.df
    @param allLinksData: allLinksData pandas.df
    @param VarSou: VarSou str
    @param VarTar: VarTar str
    @param weightQuota: weightQuota str
    @return: G nx.DiGraph
    """
    netWorkDF = allLinksData[(allLinksData["VarSou"] == VarSou) & (allLinksData["VarTar"] == VarTar)]
    G = nx.DiGraph(VarSou=VarSou, VarTar=VarTar)
    for nIndex, nRow in allNodesData.iterrows():
        nodeID = nRow['label']
        G.add_node(nodeID)
        for nf in allNodesData.columns.values:
            G.node[nodeID][nf] = nRow[nf]
    for lIndex, lRow in netWorkDF.iterrows():
        thisSou = lRow["Source"]
        thisTar = lRow["Target"]
        G.add_edge(thisSou, thisTar, weight=lRow[weightQuota])
        for lf in netWorkDF.columns.values:
            G.edges[thisSou, thisTar][lf] = lRow[lf]
    return G


def drawNetWorkOnMap(showOrSave, netWorkG, geoAgentShpPath, edgeColorF, nodeColorF):
    """
    @param showOrSave 'show','save'
    @param netWorkG: netWorkG nx.DiGraph
    @param geoAgentShpPath: geoAgentShpPath shapefile by ESRI
    @param edgeColorF: edgeColorField str
    @param nodeColorF: nodeColorField str
    @return: just show Map
    """
    plt.figure(figsize=(16, 9), dpi=200)
    worldMap = Basemap(
        projection='kav7',
        lon_0=0,
        resolution='l',
    )
    # Now draw the map
    # worldMap.drawcountries(linewidth=0.5)
    # worldMap.drawstates()
    # worldMap.drawcoastlines(linewidth=0.5)
    # fill in color
    # worldMap.fillcontinents(color='gray', lake_color='#7396FE')
    # worldMap.drawmapboundary(fill_color='#7396FE', color='#404243', linewidth=0.5)
    # draw lon and lat
    # worldMap.drawparallels(np.arange(-90., 91., 30.))
    # worldMap.drawmeridians(np.arange(-180., 181., 30.))
    # worldMap.bluemarble(scale=0.5, alpha=0.8)
    # worldMap.shadedrelief()
    worldMap.etopo(scale=0.5, alpha=0.5)
    worldMap.readshapefile(geoAgentShpPath, 'GeoAgent', color='#818487', linewidth=0.5)
    mapTitle = 'NetWork ' + netWorkG.graph['VarSou'] + ' to ' + netWorkG.graph['VarTar'] + ' By THRILLER'
    plt.title(mapTitle)

    pos = {}
    for n, d in netWorkG.nodes(data=True):
        # convert lat and lon to map projection
        mx, my = worldMap(d['longitude'], d['latitude'])
        pos[n] = (mx, my)
    nx.draw_networkx_edges(netWorkG, pos, width=0.5, alpha=0.9,
                           edge_color=[float(d[edgeColorF]) for (u, v, d) in netWorkG.edges(data=True)],
                           edge_cmap=plt.cm.Purples, arrows=False, connectionstyle="arc3,rad=0.1")
    # first draw point's edge in black
    nx.draw_networkx_nodes(netWorkG, pos, node_size=[netWorkG.degree(n) * 1.7 for n in netWorkG],
                           node_color='k')
    nx.draw_networkx_nodes(netWorkG, pos, node_size=[netWorkG.degree(n) * 1.5 for n in netWorkG],
                           node_color=[d[nodeColorF] for n, d in netWorkG.nodes(data=True)], cmap=plt.cm.OrRd)
    # nx.draw_networkx_labels(netWorkG, pos, font_size=11, font_family='Times New Roman', font_color='k')

    if showOrSave == 'show':
        # max windows
        plt.get_current_fig_manager().window.showMaximized()
        plt.show()
    if showOrSave == 'save':
        plt.savefig(outPutPath + mapTitle + ".png")


def analysisNetWork(netWorkG):
    A = nx.adjacency_matrix(netWorkG)
    degree = nx.degree(netWorkG)


# Run main
if __name__ == "__main__":
    main()
