# GeoAgentModel
# 01BuildNetWork
# THRILLER柠檬
# thrillerlemon@outlook.com
# 2019年11月1日

# 📌对构建网络链接进行代码实现，打算计算出多个相关关系指标来进行关系的判定
# ✅1、地理空间距离——————Done！
# ✅2、Pearson相关性和显著性——————Done！
# ✅3、互相关和由互相关计算得来的互相关权重；加入时间滞后——————Done！
# ✅4、Mutual Information（互信息）——————Done！
# 📌对这些指标的阈值进行确定，进而筛选出冗余更小的连接


import math
import time

import numpy as np
import pandas as pd
import scipy.stats as st
from geopy.distance import geodesic
from scipy import ndimage
from scipy.integrate import dblquad
from scipy.stats import gaussian_kde

# Input Data
dictData = {
    'Tem': 'D:\\OneDrive\\SharedFile\\环境经济社会可持续发展耦合网络模型\\GeoAgent_GlobalClimate\\GlobalClimateagentInfomean_2m_air_temperature8085.csv',
    'Prs': 'D:\\OneDrive\\SharedFile\\环境经济社会可持续发展耦合网络模型\\GeoAgent_GlobalClimate\\GlobalClimateagentInfosurface_pressure8085.csv',
    'Pre': 'D:\\OneDrive\\SharedFile\\环境经济社会可持续发展耦合网络模型\\GeoAgent_GlobalClimate\\GlobalClimateagentInfototal_precipitation8085.csv'
}


def main():
    # ******Main******
    print(time.strftime('%H:%M:%S', time.localtime(time.time())))
    # Load Point info
    fnPoi = 'D:\\OneDrive\\SharedFile\\环境经济社会可持续发展耦合网络模型\\GeoAgent_GlobalClimate\\PointInfo.csv'
    dataPoi = pd.read_csv(fnPoi)
    # set index for point info
    idIndex = 'label'
    lonIndex = 'longitude'
    latIndex = 'latitude'
    poiPos = pd.DataFrame(
        {'id': dataPoi.loc[:, idIndex], 'longitude': dataPoi.loc[:, lonIndex], 'latitude': dataPoi.loc[:, latIndex]})

    # Load Data
    # Data like
    # label  Data_Time1  Data_Time2  Data_Time3  Data_Time4 ...
    # [int]  [double]    [double]    [double]    [double]
    # 00000  0.001       0.002       0.67        1.34
    # 00001  0.003       0.022       0.69        2.34
    # ...    ...         ...         ...         ...
    # This data must have the same index with pointInfo

    kindsLinks=[]
    for key in dictData:
        for secKey in dictData:
            if key == secKey:
                rSing = GetRsing(key)
                kindsLinks.append(rSing)
            else:
                rMult = GetRmult(key, secKey)
                kindsLinks.append(kindsLinks)

    # Tem_sing = GetRsing('Tem')
    # Tem_sing_Dis = GetDistance(TEMPLinks, poiPos)
    # Tem_sing_Dis.to_csv('C:\\Users\\thril\\Desktop\\Tem_sing_Dis.csv')

    # Prs2Tem_mult = GetRmult('Prs','Tem')
    # Prs2Tem_mult_Dis = GetDistance(Prs2Tem_mult, poiPos)
    # Prs2Tem_mult_Dis.to_csv('C:\\Users\\thril\\Desktop\\Prs2Tem_mult_Dis.csv')
    # kindsLinks =[Tem_sing_Dis, Prs2Tem_mult_Dis]
    
    # Tem_sing_Dis = pd.read_csv(
    #     'D:\OneDrive\SharedFile\环境经济社会可持续发展耦合网络模型\GeoAgent_GlobalClimate\LinkInfo_Fig\Tem_sing_Dis.csv')
    # Prs2Tem_mult_Dis = pd.read_csv(
    #     'D:\OneDrive\SharedFile\环境经济社会可持续发展耦合网络模型\GeoAgent_GlobalClimate\LinkInfo_Fig\Prs2Tem_mult_Dis.csv')

    # geoLinks save all the Links
    geoLinks = pd.concat(kindsLinks, ignore_index=True)
    geoLinks.to_csv(
        'D:\OneDrive\SharedFile\环境经济社会可持续发展耦合网络模型\GeoAgent_GlobalClimate\LinkInfo_Fig\geoLinks.csv')

    print(time.strftime('%H:%M:%S', time.localtime(time.time())))
    print('GOOD!')


# ******SubFunction******
def GetDistance(links, poiPosDF):
    links['Distance'] = None
    for lIndex, lRow in links.iterrows():
        thisSou = lRow["Source"]
        thisTar = lRow["Target"]
        souPoi = poiPosDF[poiPosDF["id"] == thisSou].copy()
        tarPoi = poiPosDF[poiPosDF["id"] == thisTar].copy()
        dist = geodesic((souPoi.iloc[0]['latitude'], souPoi.iloc[0]['longitude']),
                        (tarPoi.iloc[0]['latitude'], tarPoi.iloc[0]['longitude']))
        links.loc[lIndex, 'Distance'] = dist.km
    return links


def GetRsing(VarName):
    data = pd.read_csv(dictData[VarName])
    dataValues = data.values
    labelData = dataValues[..., 0].astype(np.int32)
    dataValues = np.delete(dataValues, 0, axis=1)
    [agentNum, dataNum] = dataValues.shape
    singLinks = pd.DataFrame(
        columns=('VarSou', 'VarTar', 'Source', 'Target', 'Rpear', 'Ppear', 'Cij', 'Wij', 'MIij'))
    for iAgent in np.arange(0, agentNum):
        thisAgent = dataValues[iAgent, ...]
        otherAgent = np.delete(dataValues, iAgent, axis=0)
        labelOther = np.delete(labelData, iAgent, axis=0)
        for iOther in np.arange(0, agentNum - 1):
            [Rpear, Ppear, link_C, link_W, linkMI] = correlation(
                thisAgent, otherAgent[iOther, ...], dataNum)
            singLinks = singLinks.append(pd.DataFrame(
                {
                    'VarSou': [VarName],
                    'VarTar': [VarName],
                    'Source': [labelData[iAgent]],
                    'Target': [labelOther[iOther]],
                    'Rpear': [Rpear],
                    'Ppear': [Ppear],
                    'Cij': [link_C],
                    'Wij': [link_W],
                    'MIij': [linkMI],
                }), ignore_index=True)

    pRpear = singLinks.loc[:, "Rpear"]
    pPpear = singLinks.loc[:, "Ppear"]
    pCij = singLinks.loc[:, "Cij"]
    pWij = singLinks.loc[:, "Wij"]
    pMiij = singLinks.loc[:, "MIij"]
    Cdes70 = pCij.describe(percentiles=[0.7]).loc['70%']
    Wdes70 = pWij.describe(percentiles=[0.7]).loc['70%']
    Mdes70 = pMiij.describe(percentiles=[0.7]).loc['70%']
    # Filter the Links
    # 1 Ppear<1e-10
    # 2 Cij>Cdes70
    # 3 Wij>Wdes70
    # 4 Miij>Mdes70
    filteredLinks = singLinks[
        (singLinks["Ppear"] < 1e-10)
        & (singLinks["Cij"] > Cdes70)
        & (singLinks["Wij"] > Wdes70)
        & (singLinks["MIij"] > Mdes70)
    ].copy()
    return filteredLinks


def GetRmult(VarSouName, VarTarName):
    dataSou = pd.read_csv(dictData[VarSouName])
    dataTar = pd.read_csv(dictData[VarTarName])
    DataSouV = dataSou.values
    DataTarV = dataTar.values
    labelSou = DataSouV[..., 0].astype(np.int32)
    labelTar = DataTarV[..., 0].astype(np.int32)
    SouValues = np.delete(DataSouV, 0, axis=1)
    TarValues = np.delete(DataTarV, 0, axis=1)
    [agentNum, dataNum] = SouValues.shape
    multLinks = pd.DataFrame(
        columns=('VarSou', 'VarTar', 'Source', 'Target', 'Rpear', 'Ppear', 'Cij', 'Wij', 'MIij'))
    for iSou in np.arange(0, agentNum):
        thisSou = SouValues[iSou, ...]
        for iTar in np.arange(0, agentNum - 1):
            [Rpear, Ppear, link_C, link_W, linkMI] = correlation(
                thisSou, TarValues[iTar, ...], dataNum)
            multLinks = multLinks.append(pd.DataFrame(
                {
                    'VarSou': [VarSouName],
                    'VarTar': [VarTarName],
                    'Source': [labelSou[iSou]],
                    'Target': [labelTar[iTar]],
                    'Rpear': [Rpear],
                    'Ppear': [Ppear],
                    'Cij': [link_C],
                    'Wij': [link_W],
                    'MIij': [linkMI],
                }), ignore_index=True)

    pRpear = multLinks.loc[:, "Rpear"]
    pPpear = multLinks.loc[:, "Ppear"]
    pCij = multLinks.loc[:, "Cij"]
    pWij = multLinks.loc[:, "Wij"]
    pMiij = multLinks.loc[:, "MIij"]
    Cdes70 = pCij.describe(percentiles=[0.7]).loc['70%']
    Wdes70 = pWij.describe(percentiles=[0.7]).loc['70%']
    Mdes70 = pMiij.describe(percentiles=[0.7]).loc['70%']
    # Filter the Links
    # 1 Ppear<1e-10
    # 2 Cij>Cdes70
    # 3 Wij>Wdes70
    # 4 Miij>Mdes70
    filteredLinks = multLinks[
        (multLinks["Ppear"] < 1e-10)
        & (multLinks["Cij"] > Cdes70)
        & (multLinks["Wij"] > Wdes70)
        & (multLinks["MIij"] > Mdes70)
    ].copy()
    return filteredLinks

# ******Correlation Function******


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


# Run main
if __name__ == "__main__":
    main()
