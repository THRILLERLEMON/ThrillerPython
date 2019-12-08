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


def draw3DNetWork_2difVar(allNodesData, allLinksData, geoAgentShpPath, SouVar, TarVar, weightQuota):
    souBGC = '#F3B600'
    souGAC = '#704300'
    souNodeC = '#FF7335'
    souEdgeC = '#FD7E00'
    tarBGC = '#004FCC'
    tarGAC = '#005562'
    tarNodeC = '#1927FF'
    tarEdgeC = '#2600F1'
    twoLayerEdgeC = '#26F100'
    twoLayerdis = 0.5
    fig = plt.figure(figsize=(10, 10), dpi=200)
    ax = Axes3D(fig, xlim=[-180, 180], ylim=[-90, 90])
    ax.grid(False)

    ### drwa background
    souBG = Rectangle((-180, -90), 360, 180, color=souBGC, ec=souGAC, alpha=0.3)
    ax.add_patch(souBG)
    art3d.pathpatch_2d_to_3d(souBG, z=0, zdir="z")
    ax.text(170, 90, 0, SouVar, color='k')
    tarBG = Rectangle((-180, -90), 360, 180, color=tarBGC, ec=tarGAC, alpha=0.3)
    ax.add_patch(tarBG)
    art3d.pathpatch_2d_to_3d(tarBG, z=twoLayerdis, zdir="z")
    ax.text(170, 90, 0.5, TarVar, color='k')
    # add ageAgent
    target_projection = ccrs.PlateCarree()
    feaGeoAgent = ShapelyFeature(Reader(geoAgentShpPath).geometries(), ccrs.PlateCarree())
    gemsGA = feaGeoAgent.geometries()
    gemsGA = [target_projection.project_geometry(geom, feaGeoAgent.crs) for geom in gemsGA]
    pathsGA = list(itertools.chain.from_iterable(geos_to_path(geom) for geom in gemsGA))
    segsGA = []
    for path in pathsGA:
        vertices = [vertex for vertex, _ in path.iter_segments()]
        vertices = np.asarray(vertices)
        segsGA.append(vertices)
    lc = LineCollection(segsGA, color=souGAC, linewidths=0.1, alpha=0.6)
    ax.add_collection3d(lc, 0)
    lc2 = LineCollection(segsGA, color=tarGAC, linewidths=0.1, alpha=0.6)
    ax.add_collection3d(lc2, twoLayerdis)

    ### draw Sou net
    NetGS = buildNetWork_2Var(
        allNodesData=allNodesData,
        allLinksData=allLinksData,
        VarSou=SouVar,
        VarTar=SouVar,
        weightQuota=weightQuota)
    posSou = {}
    for n, d in NetGS.nodes(data=True):
        # transform lon & lat
        mx, my = target_projection.transform_point(d['longitude'], d['latitude'], ccrs.PlateCarree())
        posSou[n] = (mx, my)
    NetedgesS = nx.draw_networkx_edges(NetGS, posSou, width=0.5, alpha=0.7, arrows=False, edge_color=souEdgeC)
    ax.add_collection3d(NetedgesS, 0)
    # Use this ax's ticks will disappear
    # nx.draw_networkx_nodes(NetGS, posS, node_size=[NetGS.degree(n) * 0.5 for n in NetGS],
    #                        node_color=souDarkC)
    posSou = {}
    Sdegeq0 = []
    for an in NetGS:
        if NetGS.degree(an) == 0:
            Sdegeq0.append(an)
    NetGS.remove_nodes_from(Sdegeq0)
    for n, d in NetGS.nodes(data=True):
        # transform lon & lat
        mx, my = target_projection.transform_point(d['longitude'], d['latitude'], ccrs.PlateCarree())
        posSou[n] = (mx, my, 0, NetGS.degree(n))

    for key, value in posSou.items():
        xi = value[0]
        yi = value[1]
        zi = value[2]
        ax.scatter(xi, yi, zi, alpha=0.8, c=souNodeC, s=value[3] * 0.5)

    ### draw Tar net
    NetGT = buildNetWork_2Var(
        allNodesData=allNodesData,
        allLinksData=allLinksData,
        VarSou=TarVar,
        VarTar=TarVar,
        weightQuota=weightQuota)
    posTar = {}
    for n, d in NetGT.nodes(data=True):
        # transform lon & lat
        mx, my = target_projection.transform_point(d['longitude'], d['latitude'], ccrs.PlateCarree())
        posTar[n] = (mx, my)
    NetedgesT = nx.draw_networkx_edges(NetGT, posTar, width=0.5, alpha=0.7, arrows=False, edge_color=tarEdgeC)
    ax.add_collection3d(NetedgesT, twoLayerdis)
    posTar = {}
    Tdegeq0 = []
    for an in NetGT:
        if NetGT.degree(an) == 0:
            Tdegeq0.append(an)
    NetGT.remove_nodes_from(Tdegeq0)
    for n, d in NetGT.nodes(data=True):
        # transform lon & lat
        mx, my = target_projection.transform_point(d['longitude'], d['latitude'], ccrs.PlateCarree())
        posTar[n] = (mx, my, twoLayerdis, NetGT.degree(n))

    for key, value in posTar.items():
        xi = value[0]
        yi = value[1]
        zi = value[2]
        ax.scatter(xi, yi, zi, alpha=0.8, c=tarNodeC, s=value[3] * 0.5)

    ### draw Sou to Tar net
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
        if NetGST.in_degree(n) == 0:
            pos[n] = (mx, my, 0, NetGST.degree(n))
        else:
            pos[n] = (mx, my, twoLayerdis, NetGST.degree(n))
    for key, value in pos.items():
        xi = value[0]
        yi = value[1]
        zi = value[2]
        if zi != 0:
            degreeTar = 0
            try:
                degreeTar = posTar[key][3]
            except:
                degreeTar = 0
            finally:
                ax.scatter3D(xi, yi, zi, alpha=0.8, c=tarNodeC, s=(value[3] + degreeTar) * 0.5)
        else:
            degreeSou = 0
            try:
                degreeSou = posSou[key][3]
            except:
                degreeSou = 0
            finally:
                ax.scatter3D(xi, yi, zi, alpha=0.8, c=souNodeC, s=(value[3] + degreeSou) * 0.5)

    for u, v, d in NetGST.edges(data=True):
        if d['Source'] == d['Target']:
            x = np.array((pos[u][0], pos[v][0]))
            y = np.array((pos[u][1], pos[v][1]))
            z = np.array((0, twoLayerdis))
            ax.plot(x, y, z, c=twoLayerEdgeC, alpha=0.7, linewidth=0.5)
            degreeSou = 0
            try:
                degreeSou = posSou[d['Source']][3]
            except:
                degreeSou = 0
            finally:
                ax.scatter3D(pos[u][0], pos[u][1], 0, alpha=0.8, c=souNodeC, s=(pos[d['Source']][3] + degreeSou) * 0.5)
        x = np.array((pos[u][0], pos[v][0]))
        y = np.array((pos[u][1], pos[v][1]))
        z = np.array((pos[u][2], pos[v][2]))
        ax.plot(x, y, z, c=twoLayerEdgeC, alpha=0.7, linewidth=0.5)

    ### show fig
    ax.set_xlabel('longitude')
    ax.set_ylabel('latitude')
    ax.set_zlabel('NetWork Layer')
    ax.get_zaxis().set_ticks([])
    mapTitle = 'NetWork ' + SouVar + ' to ' + TarVar + ' By THRILLER'
    ax.set_title(mapTitle)
    plt.get_current_fig_manager().window.showMaximized()
    plt.show()


def analysisNetWork(netWorkG):
    A = nx.adjacency_matrix(netWorkG)
    degree = nx.degree(netWorkG)


# Run main
if __name__ == "__main__":
    main()
