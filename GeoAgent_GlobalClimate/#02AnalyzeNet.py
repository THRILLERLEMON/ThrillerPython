# -*- coding: utf-8 -*-
# @Time    : 2019/11/6 00:00
# @Author  : THRILLER柠檬
# @Email   : thrillerlemon@outlook.com
# @File    : #02AnalyzeNet.py
# @Software: PyCharm
# GeoAgentModel
# 02AnalyzeNetwork

import time
import itertools
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import networkx as nx
import multinetx as mx
import cartopy.crs as ccrs
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.collections import LineCollection
from cartopy.io.shapereader import Reader
from cartopy.feature import ShapelyFeature
from cartopy.mpl.patch import geos_to_path
from matplotlib.patches import Rectangle, PathPatch
from matplotlib.text import TextPath
import mpl_toolkits.mplot3d.art3d as art3d

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

    # draw2NetWorkOn3DMaps(NetG1,NetG2, geoAgentSHPpath, 'weight', 'tem_skew_mean')
    draw3DNetWork_2difVar(allNodes, allLinks, geoAgentSHPpath, 'Prs', 'Pre', 'Cij')
    # varList = {'Tem', 'Prs', 'Pre'}
    # for var in varList:
    #     for secvar in varList:
    #         NetG = build2VarNetWork(
    #             allNodesData=allNodes,
    #             allLinksData=allLinks,
    #             VarSou=var,
    #             VarTar=secvar,
    #             weightQuota='Cij')
    #         draw2DNetWorkOnMap(
    #             showOrSave='save',
    #             netWorkG=NetG,
    #             geoAgentShpPath=geoAgentSHPpath,
    #             edgeColorF='weight',
    #             nodeColorF='tem_skew_mean')

    print(time.strftime('%H:%M:%S', time.localtime(time.time())))


# SubFunction
def buildNetWork_2Var(allNodesData, allLinksData, VarSou, VarTar, weightQuota):
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


def draw2DNetWork_2Var(showOrSave, netWorkG, geoAgentShpPath, edgeColorF, nodeColorF):
    """
    @param showOrSave 'show','save'
    @param netWorkG: netWorkG nx.DiGraph
    @param geoAgentShpPath: geoAgentShpPath shapefile by ESRI
    @param edgeColorF: edgeColorField str
    @param nodeColorF: nodeColorField str
    @return: just show or save Map
    """
    fig = plt.figure(figsize=(20, 15), dpi=300)
    targetPro = ccrs.Robinson()
    ax = fig.add_subplot(1, 1, 1, projection=targetPro)
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
        mx, my = targetPro.transform_point(d['longitude'], d['latitude'], ccrs.PlateCarree())
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


def draw2NetWorkOn3DMaps(netWorkG1, netWorkG2, geoAgentShpPath, edgeColorF, nodeColorF):
    fig = plt.figure(figsize=(10, 10), dpi=200)
    ax = Axes3D(fig, xlim=[-180, 180], ylim=[-90, 90])
    ax2 = Axes3D(fig, xlim=[-180, 180], ylim=[-90, 90])
    ax.set_zlim(bottom=0)
    ax2.set_zlim(bottom=0.2)
    target_projection = ccrs.PlateCarree()
    feature = ShapelyFeature(Reader(geoAgentShpPath).geometries(), ccrs.PlateCarree())
    geoms = feature.geometries()
    geoms = [target_projection.project_geometry(geom, feature.crs) for geom in geoms]
    paths = list(itertools.chain.from_iterable(geos_to_path(geom) for geom in geoms))
    segments = []
    for path in paths:
        vertices = [vertex for vertex, _ in path.iter_segments()]
        vertices = np.asarray(vertices)
        segments.append(vertices)

    lc = LineCollection(segments, color='black', linewidths=0.1)
    ax.add_collection3d(lc, 0)

    pos = {}
    for n, d in netWorkG1.nodes(data=True):
        # transform lon & lat
        mx, my = target_projection.transform_point(d['longitude'], d['latitude'], ccrs.PlateCarree())
        pos[n] = (mx, my)

    Netedges1 = nx.draw_networkx_edges(netWorkG1, pos, width=0.15, alpha=0.7, arrows=False, edge_color='b')
    Netedges2 = nx.draw_networkx_edges(netWorkG2, pos, width=0.15, alpha=0.7, arrows=False, edge_color='r')
    ax.add_collection3d(Netedges1, 0)
    ax.add_collection3d(Netedges2, 0.2)
    # first draw point's edge in black to set Point edge
    # nx.draw_networkx_nodes(netWorkG, pos, ax=ax, node_size=[netWorkG.degree(n) * 1.4 for n in netWorkG],
    #                        node_color='k')
    Netnodes = nx.draw_networkx_nodes(netWorkG1, pos, ax=ax2, node_size=[netWorkG1.degree(n) * 1.3 for n in netWorkG1],
                                      node_color=[d[nodeColorF] for n, d in netWorkG1.nodes(data=True)],
                                      cmap=plt.cm.OrRd)

    # ax.plot(Netnodes,0.4)

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.get_current_fig_manager().window.showMaximized()
    plt.show()


def draw3DNetWork_2difVar(allNodesData, allLinksData, geoAgentShpPath, SouVar, TarVar, weightQuota):
    fig = plt.figure(figsize=(10, 10), dpi=200)
    ax = Axes3D(fig, xlim=[-180, 180], ylim=[-90, 90])
    ax.set_zlim(bottom=0)

    # drwa background
    soup = Rectangle((-180, -90), 360, 180, color='#EA8512', ec='#FE8800', alpha=0.5)
    ax.add_patch(soup)
    art3d.pathpatch_2d_to_3d(soup, z=0, zdir="z")
    ax.text(-180, -90, 0, SouVar, color='k')
    tarp = Rectangle((-180, -90), 360, 180, color='#2D43CC', ec='#0122F9', alpha=0.5)
    ax.add_patch(tarp)
    art3d.pathpatch_2d_to_3d(tarp, z=0.5, zdir="z")
    ax.text(-180, -90, 0.5, TarVar, color='k')
    target_projection = ccrs.PlateCarree()
    feature = ShapelyFeature(Reader(geoAgentShpPath).geometries(), ccrs.PlateCarree())
    geoms = feature.geometries()
    geoms = [target_projection.project_geometry(geom, feature.crs) for geom in geoms]
    paths = list(itertools.chain.from_iterable(geos_to_path(geom) for geom in geoms))
    segments = []
    for path in paths:
        vertices = [vertex for vertex, _ in path.iter_segments()]
        vertices = np.asarray(vertices)
        segments.append(vertices)
    lc = LineCollection(segments, color='#FE8800', linewidths=0.1)
    lc2 = LineCollection(segments, color='#0122F9', linewidths=0.1)
    ax.add_collection3d(lc, 0)
    ax.add_collection3d(lc2, 0.5)

    # draw Sou net
    NetGS = buildNetWork_2Var(
        allNodesData=allNodesData,
        allLinksData=allLinksData,
        VarSou=SouVar,
        VarTar=SouVar,
        weightQuota=weightQuota)
    posS = {}
    for n, d in NetGS.nodes(data=True):
        # transform lon & lat
        mx, my = target_projection.transform_point(d['longitude'], d['latitude'], ccrs.PlateCarree())
        posS[n] = (mx, my)
    NetedgesS = nx.draw_networkx_edges(NetGS, posS, width=0.5, alpha=0.7, arrows=False, edge_color='#F95301')
    ax.add_collection3d(NetedgesS, 0)
    # first draw point's edge in black to set Point edge
    # nx.draw_networkx_nodes(netWorkG, pos, ax=ax, node_size=[netWorkG.degree(n) * 1.4 for n in netWorkG],
    #                        node_color='k')
    nx.draw_networkx_nodes(NetGS, posS, node_size=[NetGS.degree(n) * 0.5 for n in NetGS],
                           node_color='#F95301')

    ### draw Tar net
    NetGT = buildNetWork_2Var(
        allNodesData=allNodesData,
        allLinksData=allLinksData,
        VarSou=TarVar,
        VarTar=TarVar,
        weightQuota=weightQuota)
    posTall = {}
    for n, d in NetGT.nodes(data=True):
        # transform lon & lat
        mx, my = target_projection.transform_point(d['longitude'], d['latitude'], ccrs.PlateCarree())
        posTall[n] = (mx, my)
    NetedgesT = nx.draw_networkx_edges(NetGT, posTall, width=0.5, alpha=0.7, arrows=False, edge_color='#0122F9')
    ax.add_collection3d(NetedgesT, 0.5)
    posT = {}
    Tdegeq0 = []
    for an in NetGT:
        if NetGT.degree(an) == 0:
            Tdegeq0.append(an)
    NetGT.remove_nodes_from(Tdegeq0)
    for n, d in NetGT.nodes(data=True):
        # transform lon & lat
        mx, my = target_projection.transform_point(d['longitude'], d['latitude'], ccrs.PlateCarree())
        posT[n] = (mx, my, 0.5, NetGT.degree(n))

    for key, value in posT.items():
        xi = value[0]
        yi = value[1]
        zi = value[2]
        ax.scatter(xi, yi, zi, alpha=0.8, c='#0122F9', linewidths=value[3] * 0.5)

    ### draw ST net
    NetGST = buildNetWork_2Var(
        allNodesData=allNodesData,
        allLinksData=allLinksData,
        VarSou=SouVar,
        VarTar=TarVar,
        weightQuota=weightQuota)
    pos = {}
    # delete nodes which degree eq 0
    degeq0 = []
    for an in NetGST:
        if NetGST.degree(an) == 0:
            degeq0.append(an)
    NetGST.remove_nodes_from(degeq0)
    for n, d in NetGST.nodes(data=True):
        # transform lon & lat
        mx, my = target_projection.transform_point(d['longitude'], d['latitude'], ccrs.PlateCarree())
        # pos[n] = (mx, my, 0.2)
        if NetGST.in_degree(n) == 0:
            pos[n] = (mx, my, 0)
        else:
            pos[n] = (mx, my, 0.5)
    for key, value in pos.items():
        xi = value[0]
        yi = value[1]
        zi = value[2]
        if zi != 0:
            ax.scatter(xi, yi, zi, alpha=0.8, c='#0122F9')
        else:
            ax.scatter(xi, yi, zi, alpha=0.8, c='#F95301')

    for u, v, d in NetGST.edges(data=True):
        if d['Source'] == d['Target']:
            x = np.array((pos[u][0], pos[v][0]))
            y = np.array((pos[u][1], pos[v][1]))
            z = np.array((0, 0.5))
            ax.plot(x, y, z, c='g', alpha=0.6, linewidth=0.5)
            ax.scatter(pos[u][0], pos[u][1], 0, alpha=0.8, c='#F95301')
        x = np.array((pos[u][0], pos[v][0]))
        y = np.array((pos[u][1], pos[v][1]))
        z = np.array((pos[u][2], pos[v][2]))
        ax.plot(x, y, z, c='g', alpha=0.6, linewidth=0.5)

    ax.set_xlabel('longitude')
    ax.set_ylabel('latitude')
    ax.set_zlabel('NetWorkLayer')
    plt.get_current_fig_manager().window.showMaximized()
    plt.show()


def analysisNetWork(netWorkG):
    A = nx.adjacency_matrix(netWorkG)
    degree = nx.degree(netWorkG)


# Run main
if __name__ == "__main__":
    main()
