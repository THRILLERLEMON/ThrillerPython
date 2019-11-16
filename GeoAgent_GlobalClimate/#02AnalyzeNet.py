# GeoAgentModel
# 02AnalyzeNetwork
# THRILLER柠檬
# thrillerlemon@outlook.com
# 2019年11月6日

import time

import matplotlib.pyplot as plt
import pandas as pd
import networkx as nx
import numpy as np


def main():
    # ******Main******
    print(time.strftime('%H:%M:%S', time.localtime(time.time())))
    allLinks = pd.read_csv(
        'D:\OneDrive\SharedFile\环境经济社会可持续发展耦合网络模型\GeoAgent_GlobalClimate\LinkInfo_Fig\geoLinks.csv', index_col=0, header=0)
    print(allLinks)
    G = nx.Graph()
    for lIndex, lRow in allLinks.iterrows():
        thisSou = lRow["Source"].astype(np.int32)
        thisTar = lRow["Target"].astype(np.int32)
        thisRpear = lRow["Rpear"]
        thisCij = lRow["Cij"]
        thisWij = lRow["Wij"]
        thisMIij = lRow["MIij"]
        thisDistance = lRow["Distance"]
        G.add_edge(thisSou, thisTar, weight=thisWij,
                   crosscor=thisCij, distance=thisDistance)
    A = nx.adjacency_matrix(G)
    degree = nx.degree(G)
    # print(degree)
    nx.draw(G)
    plt.show()

    print(time.strftime('%H:%M:%S', time.localtime(time.time())))


# Run main
if __name__ == "__main__":
    main()
