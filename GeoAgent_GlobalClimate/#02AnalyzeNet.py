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
import cartopy.crs as ccrs
from cartopy.io.shapereader import Reader
from cartopy.feature import ShapelyFeature

outPutPath = 'C:\\Users\\thril\\Desktop\\'


def main():
    # ******Main******
    print(time.strftime('%H:%M:%S', time.localtime(time.time())))
    geoAgentSHPpath = 'D:\\OneDrive\\SharedFile\\环境经济社会可持续发展耦合网络模型\\GeoAgent_GlobalClimate\\GlobalClimate_SHPGeoAgent.shp'
    geoAgentInfopath = 'D:\\OneDrive\\SharedFile\\环境经济社会可持续发展耦合网络模型\\GeoAgent_GlobalClimate\\PointInfo.csv'
    geoLinkspath = 'D:\\OneDrive\\SharedFile\\环境经济社会可持续发展耦合网络模型\\GeoAgent_GlobalClimate\\geoLinks1118.csv'
    allLinks = pd.read_csv(geoLinkspath, index_col=0, header=0, dtype={'Source': np.int32, 'Target': np.int32})
    allNodes = pd.read_csv(geoAgentInfopath, header=0, dtype={'label': np.int32})
    # print(allLinks)

    # draw3DNetWorkOnMaps()

    varList = {'Tem', 'Prs', 'Pre'}
    for var in varList:
        for secvar in varList:
            NetG = build2VarNetWork(
                allNodesData=allNodes,
                allLinksData=allLinks,
                VarSou=var,
                VarTar=secvar,
                weightQuota='Cij')
            draw2DNetWorkOnMap(
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


def draw2DNetWorkOnMap(showOrSave, netWorkG, geoAgentShpPath, edgeColorF, nodeColorF):
    """
    @param showOrSave 'show','save'
    @param netWorkG: netWorkG nx.DiGraph
    @param geoAgentShpPath: geoAgentShpPath shapefile by ESRI
    @param edgeColorF: edgeColorField str
    @param nodeColorF: nodeColorField str
    @return: just show or save Map
    """
    fig = plt.figure(figsize=(20, 15), dpi=300)
    mapPro = ccrs.Robinson()
    ax = fig.add_subplot(1, 1, 1, projection=mapPro)
    ax.set_global()
    ax.stock_img()
    ax.coastlines(resolution='110m', color='#818487', linewidth=0.5)
    geoAgentShp = ShapelyFeature(Reader(geoAgentShpPath).geometries(), ccrs.PlateCarree())
    ax.add_feature(geoAgentShp, linewidth=0.5, facecolor='None', edgecolor='#393A3B', alpha=0.8)

    mapTitle = 'NetWork ' + netWorkG.graph['VarSou'] + ' to ' + netWorkG.graph['VarTar'] + ' By THRILLER'
    plt.title(mapTitle)

    pos = {}
    for n, d in netWorkG.nodes(data=True):
        # transform lon & lat
        mx, my = mapPro.transform_point(d['longitude'], d['latitude'], ccrs.PlateCarree())
        pos[n] = (mx, my)
    nx.draw_networkx_edges(netWorkG, pos, width=0.15, alpha=0.7,
                           edge_color=[float(d[edgeColorF]) for (u, v, d) in netWorkG.edges(data=True)],
                           edge_cmap=plt.cm.Purples, arrows=True, arrowstyle='fancy', arrowsize=2,
                           connectionstyle="arc3,rad=0.1")
    # first draw point's edge in black to set Point edge
    nx.draw_networkx_nodes(netWorkG, pos, node_size=[netWorkG.degree(n) * 1.4 for n in netWorkG],
                           node_color='k')
    nx.draw_networkx_nodes(netWorkG, pos, node_size=[netWorkG.degree(n) * 1.3 for n in netWorkG],
                           node_color=[d[nodeColorF] for n, d in netWorkG.nodes(data=True)], cmap=plt.cm.OrRd)

    if showOrSave == 'show':
        # max windows
        plt.get_current_fig_manager().window.showMaximized()
        plt.show()
    if showOrSave == 'save':
        plt.savefig(outPutPath + mapTitle + ".png")


def draw3DNetWorkOnMaps():
    pass


def analysisNetWork(netWorkG):
    A = nx.adjacency_matrix(netWorkG)
    degree = nx.degree(netWorkG)


# Run main
if __name__ == "__main__":
    main()
