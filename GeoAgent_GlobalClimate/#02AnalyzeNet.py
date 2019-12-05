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


def main():
    # ******Main******
    print(time.strftime('%H:%M:%S', time.localtime(time.time())))
    allLinks = pd.read_csv(
        'D:\OneDrive\SharedFile\环境经济社会可持续发展耦合网络模型\GeoAgent_GlobalClimate\geoLinks1118.csv', index_col=0, header=0)
    # print(allLinks)
    temNetG = buildNetWork(allLinks, 'Tem', 'Tem', 'Cij')
    drawNetWorkOnMap(temNetG)

    print(time.strftime('%H:%M:%S', time.localtime(time.time())))


# SubFunction
def buildNetWork(allLinksData, VarSou, VarTar, weightQuota):
    netWorkDF = allLinksData[(allLinksData["VarSou"] == VarSou) & (allLinksData["VarTar"] == VarTar)]
    G = nx.DiGraph(VarSou=VarSou, VarTar=VarTar)
    for lIndex, lRow in netWorkDF.iterrows():
        thisSou = lRow["Source"]
        # thisSou = lRow["Source"].astype(np.int32)
        thisTar = lRow["Target"]
        # thisTar = lRow["Target"].astype(np.int32)
        thisRpear = lRow["Rpear"]
        thisCij = lRow["Cij"]
        thisWij = lRow["Wij"]
        thisMIij = lRow["MIij"]
        # thisDistance = lRow["Distance"]
        G.add_edge(thisSou, thisTar, weight=lRow[weightQuota],
                   Rpear=thisRpear,
                   Cij=thisCij,
                   Wij=thisWij,
                   MIij=thisMIij,
                   # distance=thisDistance
                   )
    return G


def drawNetWorkOnMap(netWorkG):
    worldMap = Basemap(
        projection='kav7',
        lon_0=0,
        resolution='l',
    )
    geoAgentSHPpath = 'D:\\OneDrive\\SharedFile\\环境经济社会可持续发展耦合网络模型\\GeoAgent_GlobalClimate\\GlobalClimate_SHPGeoAgent'
    geoAgentInfopath = 'D:\\OneDrive\\SharedFile\\环境经济社会可持续发展耦合网络模型\\GeoAgent_GlobalClimate\\PointInfo.csv'
    geoAgentInfo = pd.read_csv(geoAgentInfopath, index_col=0, header=0)
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
    worldMap.readshapefile(geoAgentSHPpath, 'GeoAgent', linewidth=0.5)
    # worldMap.bluemarble()
    plt.title('NetWork ' + netWorkG.graph['VarSou'] + ' to ' + netWorkG.graph['VarTar'] + ' By THRILLER')

    pos = {}
    for lIndex, lRow in geoAgentInfo.iterrows():
        thisPoint = lRow['label']
        # convert lat and lon to map projection
        mx, my = worldMap(lRow['longitude'], lRow['latitude'])
        pos[thisPoint] = (mx, my)

    nx.draw_networkx_edges(netWorkG, pos, width=0.5,
                           edge_color=[float(d['weight']) for (u, v, d) in netWorkG.edges(data=True)],
                           alpha=[float(d['weight']) for (u, v, d) in netWorkG.edges(data=True)],
                           edge_cmap=plt.cm.Blues, arrows=False, connectionstyle="arc3,rad=0.1")

    nx.draw_networkx_nodes(netWorkG, pos, node_size=[netWorkG.degree(n) * 1.7 for n in netWorkG],
                           node_color='k')
    nx.draw_networkx_nodes(netWorkG, pos, node_size=[netWorkG.degree(n) * 1.5 for n in netWorkG],
                           node_color=[netWorkG.degree(n) for n in netWorkG], cmap=plt.cm.Oranges)
    # nx.draw_networkx_labels(netWorkG, pos, font_size=11, font_family='Times New Roman', font_color='k')

    # max windows
    plt.get_current_fig_manager().window.showMaximized()
    plt.show()


def analysisNetWork(netWorkG):
    A = nx.adjacency_matrix(netWorkG)
    degree = nx.degree(netWorkG)


# Run main
if __name__ == "__main__":
    main()
