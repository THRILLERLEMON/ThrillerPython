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