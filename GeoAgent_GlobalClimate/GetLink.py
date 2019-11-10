# GeoAgentModel
# THRILLER柠檬
# thrillerlemon@outlook.com

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

def cross_cor(Ti, Tj,dataNum):
    maxTimeLag = int(np.round(dataNum * 0.7))
    std_i = Ti.std()
    mean_i = Ti.mean()
    C_taus=[]
    for iTimeLag in np.arange(1, maxTimeLag):
        Tj_tau = Tj[np.hstack([range(iTimeLag, dataNum), range(0, iTimeLag)])]
        std_tau = Tj_tau.std()
        mean_tau = Tj_tau.mean()
        Ti_m_Ttau = Ti * Tj_tau
        mean_Ti_m_Ttau = Ti_m_Ttau.mean()
        Cij_tau = (mean_Ti_m_Ttau - mean_i * mean_tau) / (std_i * std_tau)
        C_taus = np.hstack([C_taus, Cij_tau])
    theta = C_taus.max()
    # minCs=C_taus.min()
    # maxCs = C_taus.max()
    # if abs(minCs)<abs(maxCs):
    #     theta = maxCs
    # else:
    #     theta = minCs
    mean_C_taus = C_taus.mean()
    std_C_taus = C_taus.std()
    Wij=(abs(theta)-mean_C_taus)/std_C_taus
    return theta,Wij


# Load Data
fnTem='D:\OneDrive\SharedFile\草地MTE工作\GeoAgent_GlobalClimate\GlobalClimateagentInfomean_2m_air_temperature8085.csv';
dataTem = np.loadtxt(fnTem, delimiter=',', skiprows=1)

labelData = dataTem[..., 0].astype(np.int32)
dataTem = np.delete(dataTem, 0, axis=1)
[agentNum, dataNum] = dataTem.shape

# cross-correlation
G = nx.Graph()
for iAgent in np.arange(0,agentNum):
    thisAgent = dataTem[iAgent, ...]
    otherAgent = np.delete(dataTem, iAgent, axis=0)
    labelOther = np.delete(labelData, iAgent, axis=0)
    # C_W = []
    for iOther in np.arange(0,agentNum-1):
        [link_C, link_W] = cross_cor(thisAgent, otherAgent[iOther, ...], dataNum)
        G.add_edge(labelData[iAgent], labelOther[iOther], weight=link_W, crosscor=link_C)
        # C_W.append([link_C, link_W])
    # print(C_W)
nx.draw(G)
plt.show()
print('GOOD!')


