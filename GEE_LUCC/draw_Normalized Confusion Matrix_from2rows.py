# -*-coding:utf-8-*-
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import numpy as np

# labels表示你不同类别的代号
labels = [
    'ENF',
    'DBF',
    'MF',
    'Cshrub',
    'Oshrub',
    'Grass',
    'Wet',
    'Crop',
    'Buildup',
    'Crop&Tree',
    'Snow',
    'Barren',
    'Water']

# y_true代表真实的label值 y_pred代表预测得到的lavel值
y_true = np.loadtxt('C:/Users/thril/Desktop/Modisls.txt')
y_pred = np.loadtxt('C:/Users/thril/Desktop/ls_landcover.txt')

tick_marks = np.array(range(len(labels))) + 0.5


def plot_confusion_matrix(cm, title='Confusion Matrix', cmap=plt.cm.binary):
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    xlocations = np.array(range(len(labels)))
    plt.xticks(xlocations, labels, rotation=90)
    plt.yticks(xlocations, labels)
    plt.ylabel('YR_90m_Class')
    plt.xlabel('Modis_Class')


cm = confusion_matrix(y_true, y_pred)
np.set_printoptions(precision=2)
cm_normalized = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
print(cm_normalized)
plt.figure(figsize=(12, 8), dpi=120)

ind_array = np.arange(len(labels))
x, y = np.meshgrid(ind_array, ind_array)

for x_val, y_val in zip(x.flatten(), y.flatten()):
    c = cm_normalized[y_val][x_val]
    if c > 0.01:
        plt.text(x_val, y_val, "%0.2f" % (c,), color='red',
                 fontsize=7, va='center', ha='center')
# offset the tick
plt.gca().set_xticks(tick_marks, minor=True)
plt.gca().set_yticks(tick_marks, minor=True)
plt.gca().xaxis.set_ticks_position('none')
plt.gca().yaxis.set_ticks_position('none')
plt.grid(True, which='minor', linestyle='-')
plt.gcf().subplots_adjust(bottom=0.15)

plot_confusion_matrix(cm_normalized, title='Normalized Confusion Matrix')
# show confusion matrix
plt.savefig('C:/Users/thril/Desktop/confusion_matrix2016.png', format='png')
plt.show()
