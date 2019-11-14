# GeoAgentModel
# THRILLER柠檬
# thrillerlemon@outlook.com

import time

import matplotlib.pyplot as plt
import pandas as pd

allLinks=pd.read_csv('D:\OneDrive\SharedFile\环境经济社会可持续发展耦合模型\GeoAgent_GlobalClimate\LinkInfo.csv')




Source=allLinks.loc[:, "Source"]
Target=allLinks.loc[:, "Target"]
Distance=allLinks.loc[:, "Distance"]
Rpear=allLinks.loc[:, "Rpear"]
Ppear=allLinks.loc[:, "Ppear"]
Cij=allLinks.loc[:, "Cij"]
Wij=allLinks.loc[:, "Wij"]
Miij=allLinks.loc[:, "Miij"]

print('show plot')
# plt.plot(Distance,Rpear,'o',label = "Rpear")
# plt.plot(Distance,Ppear,'s',label = "Ppear")
# plt.plot(Distance,Cij,'x',label = "Cij")
# plt.plot(Distance,Wij,'+',label = "Wij")
# plt.plot(Distance,Miij,'d',label = "Miij")
# plt.legend(numpoints=1)
# plt.show()
print (time.strftime('%H:%M:%S',time.localtime(time.time())))

Rdes70 =Rpear.describe(percentiles=[0.7]).loc['70%']
Cdes70 =Cij.describe(percentiles=[0.7]).loc['70%']
Wdes70 =Wij.describe(percentiles=[0.7]).loc['70%']
Mdes70 =Miij.describe(percentiles=[0.7]).loc['70%']




# Filter the Links
# 1 Ppear<1e-10
# 2 Cij>Cdes70
# 3 Wij>Wdes70
# 4 Miij>Mdes70
filterLinks = allLinks[
                (allLinks["Ppear"] < 1e-10)
                & (allLinks["Cij"] > Cdes70)
                & (allLinks["Wij"] > Wdes70)
                & (allLinks["Miij"] > Mdes70)
            ].copy()
print(filterLinks)
print(allLinks)
filterLinks.to_csv('C:\\Users\\thril\\Desktop\\filterLinks.csv')

showallLinks = allLinks.iloc[:, 3:7]
boxallLinks = showallLinks.boxplot(sym = 'o',  # 异常点形状，参考marker
               vert = True,  # 是否垂直
               whis = 1.5,  # IQR，默认1.5，也可以设置区间比如[5,95]，代表强制上下边缘为数据95%和5%位置
               patch_artist = True,  # 上下四分位框内是否填充，True为填充
               meanline = False,showmeans=True,  # 是否有均值线及其形状
               showbox = True,  # 是否显示箱线
               showcaps = True,  # 是否显示边缘线
               showfliers = True,  # 是否显示异常值
               notch = False,  # 中间箱体是否缺口
               return_type='dict'  # 返回类型为字典
              ) 
plt.title('boxplot')
plt.show()


fig, axs = plt.subplots(2, 2)
kwargs = dict(histtype='stepfilled', alpha=0.3, density=True, bins=640,stacked =True)
axs[0, 0].hist(Ppear, **kwargs)
axs[0, 0].set_title('Ppear')
axs[0, 1].hist(Cij, **kwargs)
axs[0, 1].set_title('Cij')
axs[1, 0].hist(Wij, **kwargs)
axs[1, 0].set_title('Wij')
axs[1, 1].hist(Miij, **kwargs)
axs[1, 1].set_title('Miij')
plt.show()




plt.hexbin(Cij, Miij, bins=640, cmap='Blues')
plt.xlabel('Cij')
plt.ylabel('Miij')
cb = plt.colorbar()
cb.set_label('counts in bin')
plt.vlines(Cdes70,0.1, 0.3, colors='k', label='Cdes75')
plt.hlines(Mdes70,0.0, 1, colors='k', label='Mdes75')
plt.show()

plt.hexbin(Distance, Cij, bins=640, cmap='Blues')
plt.xlabel('Distance')
plt.ylabel('Cij')
cb = plt.colorbar()
cb.set_label('counts in bin')
plt.show()

plt.hexbin(Distance, Miij, bins=640, cmap='Blues')
plt.xlabel('Distance')
plt.ylabel('Miij')
cb = plt.colorbar()
cb.set_label('counts in bin')
plt.show()
