# -*- coding: utf-8 -*-
# @Time    : 2019/11/11 00:00
# @Author  : THRILLER柠檬
# @Email   : thrillerlemon@outlook.com
# @File    : #03ChangeNodeV.py
# @Software: PyCharm
# GeoAgentModel
# 03ChangeNodeValue


import time

import pandas as pd
import numpy as np

# Input Data
dictData = {
    'Tem': 'D:\\OneDrive\\SharedFile\\环境经济社会可持续发展耦合网络模型\\GeoAgent_GlobalClimate\\GlobalClimateagentInfomean_2m_air_temperature8085.csv',
    'Prs': 'D:\\OneDrive\\SharedFile\\环境经济社会可持续发展耦合网络模型\\GeoAgent_GlobalClimate\\GlobalClimateagentInfosurface_pressure8085.csv',
    'Pre': 'D:\\OneDrive\\SharedFile\\环境经济社会可持续发展耦合网络模型\\GeoAgent_GlobalClimate\\GlobalClimateagentInfototal_precipitation8085.csv'
}



def main():
    # ******Main******
    print(time.strftime('%H:%M:%S', time.localtime(time.time())))
    allLinks = pd.read_csv(
        'D:\OneDrive\SharedFile\环境经济社会可持续发展耦合网络模型\GeoAgent_GlobalClimate\LinkInfo_Fig\geoLinks.csv', index_col=0, header=0)
    changeNodeID = 91199060
    changeNodeValue(allLinks,changeNodeID,'PercentChange',120)

    print(time.strftime('%H:%M:%S', time.localtime(time.time())))


# ******SubFunction******
def changeNodeValue(links, nodeid, changeType, changePar):
    linksOfNode = links[(links["Source"] == nodeid) | (links["Target"] == nodeid)]
    print(linksOfNode)
    linksOfNode.sort_values(by="Cij",inplace=True,ascending=False)
    print(linksOfNode)
    print('over test')
    pass


# Run main
if __name__ == "__main__":
    main()
