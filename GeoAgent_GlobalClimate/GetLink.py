# GeoAgentModel
# THRILLER柠檬
# thrillerlemon@outlook.com

# 📌对构建网络链接进行代码实现，打算计算出多个相关关系指标来进行关系的判定
# ✅1、地理空间距离——————Done！
# ✅2、Pearson相关性和显著性——————Done！
# ✅3、互相关和由互相关计算得来的互相关权重；加入时间滞后——————Done！
# ❎4、Mutual Information（互信息）——————Working...
# 📌下一步就是对这些指标的阈值进行确定，进而筛选出冗余更小的连接

import math
import dit
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import scipy.stats as st
from scipy import ndimage
from scipy.stats import gaussian_kde
from scipy.integrate import dblquad
from geopy.distance import geodesic


def mutual_information_2d(x, y, binNum=64, sigma=1, normalized=False):
    # cite https://gist.github.com/GaelVaroquaux/ead9898bd3c973c40429
    """
    Computes (normalized) mutual information between two 1D variate from a
    joint histogram.
    Parameters
    ----------
    x : 1D array
        first variable
    y : 1D array
        second variable
    sigma: float
        sigma for Gaussian smoothing of the joint histogram
    Returns
    -------
    nmi: float
        the computed similariy measure
    """

    EPS = np.finfo(float).eps

    bins = (binNum, binNum)

    jh = np.histogram2d(x, y, bins=bins)[0]

    # smooth the jh with a gaussian filter of given sigma
    ndimage.gaussian_filter(jh, sigma=sigma, mode='constant', output=jh)
    # compute marginal histograms
    jh = jh + EPS
    sh = np.sum(jh)
    jh = jh / sh
    s1 = np.sum(jh, axis=0).reshape((-1, jh.shape[0]))
    s2 = np.sum(jh, axis=1).reshape((jh.shape[1], -1))

    # Normalised Mutual Information of:
    # Studholme,  jhill & jhawkes (1998).
    # "A normalized entropy measure of 3-D medical image alignment".
    # in Proc. Medical Imaging 1998, vol. 3338, San Diego, CA, pp. 132-143.
    if normalized:
        mi = ((np.sum(s1 * np.log2(s1)) + np.sum(s2 * np.log2(s2)))
              / np.sum(jh * np.log2(jh))) - 1
    else:
        mi = (np.sum(jh * np.log2(jh)) - np.sum(s1 * np.log2(s1))
              - np.sum(s2 * np.log2(s2)))
    return mi


def correlation(Ti, Tj, dataNum):
    # ******Pearsonr
    Rpear, Ppear = st.pearsonr(Ti, Tj)

    # ******cross_cor
    maxTimeLag = int(np.round(dataNum * 0.7))
    std_i = Ti.std()
    mean_i = Ti.mean()
    C_taus = []
    for iTimeLag in np.arange(1, maxTimeLag):
        Tj_tau = Tj[np.hstack([range(iTimeLag, dataNum), range(0, iTimeLag)])]
        std_tau = Tj_tau.std()
        mean_tau = Tj_tau.mean()
        Ti_m_Ttau = Ti * Tj_tau
        mean_Ti_m_Ttau = Ti_m_Ttau.mean()
        Cij_tau = (mean_Ti_m_Ttau - mean_i * mean_tau) / (std_i * std_tau)
        C_taus = np.hstack([C_taus, Cij_tau])
    Cij = C_taus.max()
    # minCs=C_taus.min()
    # maxCs = C_taus.max()
    # if abs(minCs)<abs(maxCs):
    #     Cij = maxCs
    # else:
    #     Cij = minCs
    mean_C_taus = C_taus.mean()
    std_C_taus = C_taus.std()
    Wij = (abs(Cij) - mean_C_taus) / std_C_taus

    # ******MutualInformation
    MI = mutual_information_2d(Ti, Tj, 64, 1, True)

    # # Constants
    # MIN_DOUBLE = 4.9406564584124654e-324
    #                     # The minimum size of a Float64; used here to prevent the
    #                     #  logarithmic function from hitting its undefined region
    #                     #  at its asymptote of 0.
    # INF = float('inf')  # The floating-point representation for "infinity"
    # # Kernel estimation
    # gkde_i = gaussian_kde(Ti)
    # gkde_j = gaussian_kde(Tj)
    # gkde_ij = gaussian_kde([Ti, Tj])
    # print(gkde_i(Ti.min()))
    # print(gkde_i(Ti.max()))
    # print(gkde_j(Tj.min()))
    # print(gkde_j(Tj.max()))
    # print(gkde_ij([Ti.min(),Tj.min()]))
    # mutual_info = lambda a, b: gkde_ij([a, b]) * math.log((gkde_ij([a, b]) / (gkde_i(a) * gkde_j(b))) + MIN_DOUBLE)
    # print('cal one')
    # for target_list in expression_list:
    #     pass
    # (minfo_xy, err_xy) = dblquad(mutual_info, Ti.min(), Ti.max(), lambda a: Tj.min(), lambda a: Tj.max())
    # ## https://stackoverflow.com/questions/8363085/continuous-mutual-information-in-python/8363237

    return Rpear, Ppear, Cij, Wij, MI


# ******Main******
# Load Point info
fnPoi = 'D:\OneDrive\SharedFile\草地MTE工作\GeoAgent_GlobalClimate\PointInfo.csv'
dataPoi = np.loadtxt(fnPoi, delimiter=',', skiprows=1)

# Load Data
fnTem = 'D:\OneDrive\SharedFile\草地MTE工作\GeoAgent_GlobalClimate\GlobalClimateagentInfomean_2m_air_temperature8085.csv'
dataTem = np.loadtxt(fnTem, delimiter=',', skiprows=1)


labelData = dataPoi[..., 1].astype(np.int32)
lonData = dataPoi[..., 3]
latData = dataPoi[..., 2]
dataTem = np.delete(dataTem, 0, axis=1)
[agentNum, dataNum] = dataTem.shape

# correlation
C_W = []
G = nx.Graph()
for iAgent in np.arange(0, agentNum):
    thisAgent = dataTem[iAgent, ...]
    otherAgent = np.delete(dataTem, iAgent, axis=0)
    labelOther = np.delete(labelData, iAgent, axis=0)

    for iOther in np.arange(0, agentNum - 1):
        dist = geodesic((latData[iAgent], lonData[iAgent]),
                        (latData[iOther], lonData[iOther]))
        [Rpear, Ppear, link_C, link_W, linkMI] = correlation(
            thisAgent, otherAgent[iOther, ...], dataNum)
        G.add_edge(labelData[iAgent], labelOther[iOther],
                   weight=link_W, crosscor=link_C)
        C_W.append([labelData[iAgent], labelOther[iOther],
                    dist, Rpear, Ppear, link_C, link_W, linkMI])
        print(labelData[iAgent], labelOther[iOther],
              dist.km, Rpear, Ppear, link_C, link_W, linkMI)
    # print(C_W)

    # test
    # A = nx.adjacency_matrix(G)
    # degree = nx.degree(G)
    # print(degree)
    # nx.draw(G)
    # plt.show()
    print('ok a agent', iAgent)
df = pd.DataFrame(C_W)
df.to_csv('C:\\Users\\thril\\Desktop\\out.csv')
print('GOOD!')
