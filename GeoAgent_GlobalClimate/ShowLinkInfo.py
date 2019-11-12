# GeoAgentModel
# THRILLER柠檬
# thrillerlemon@outlook.com

import time
import pandas as pd
import matplotlib.pyplot as plt

LinkInfo=pd.read_csv('D:\OneDrive\SharedFile\草地MTE工作\GeoAgent_GlobalClimate\LinkInfo.csv')


Source=LinkInfo.loc[:, "Source"]
Target=LinkInfo.loc[:, "Target"]
Distance=LinkInfo.loc[:, "Distance"]
Rpear=LinkInfo.loc[:, "Rpear"]
Ppear=LinkInfo.loc[:, "Ppear"]
Cij=LinkInfo.loc[:, "Cij"]
Wij=LinkInfo.loc[:, "Wij"]
Miij=LinkInfo.loc[:, "Miij"]

print('show plot')
# plt.plot(Distance,Rpear,'o',label = "Rpear")
# plt.plot(Distance,Ppear,'s',label = "Ppear")
# plt.plot(Distance,Cij,'x',label = "Cij")
# plt.plot(Distance,Wij,'+',label = "Wij")
# plt.plot(Distance,Miij,'d',label = "Miij")
# plt.legend(numpoints=1)
# plt.show()
print (time.strftime('%H:%M:%S',time.localtime(time.time())))

Rdes75 =Rpear.describe().loc['75%']
Cdes75 =Cij.describe().loc['75%']
Wdes75 =Wij.describe().loc['75%']
Mdes75 =Miij.describe().loc['75%']
print(Rdes75)
print(Cdes75)
print(Wdes75)
print(Mdes75)


showLinkInfo = LinkInfo.iloc[:, 3:7]
boxLinkInfo = showLinkInfo.boxplot(sym = 'o',  # 异常点形状，参考marker
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
plt.vlines(Cdes75,0.1, 0.3, colors='k', label='Cdes75')
plt.hlines(Mdes75,0.0, 1, colors='k', label='Mdes75')
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

