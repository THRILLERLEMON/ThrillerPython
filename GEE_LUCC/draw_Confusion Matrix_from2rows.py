# -*-coding:utf-8-*-
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
import numpy as np
import os
import sys


# 输出print内容
class Logger(object):
    def __init__(self, filename="Default.log"):
        self.terminal = sys.stdout
        self.log = open(filename, "a")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        pass


printpath = os.path.abspath(os.path.dirname(__file__))
type = sys.getfilesystemencoding()
sys.stdout = Logger('OutLog_ALL.txt')
print(printpath)

# labels表示你不同类别的代号
labels = [
    'DBF',
    'ENF',
    'MF',
    'Shrub',
    'Lgrass',
    'Mgrass',
    'Hgrass',
    'Crop',
    'Orchard',
    'Builtup',
    'Water',
    'Wet',
    'Snow',
    'Desert',
    'Barren']

# y_true代表真实的label值 y_pred代表预测得到的lavel值
y_true = np.loadtxt('C:/Users/thril/Desktop/True_ALL.txt')
y_pred = np.loadtxt('C:/Users/thril/Desktop/Pred_ALL.txt')

fontInfo = {'family': 'Times New Roman', 'size': 14}

tick_marks = np.array(range(len(labels))) + 0.5


def plot_confusion_matrix(cm, title='Confusion Matrix', cmap=plt.cm.YlGn):
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    cb = plt.colorbar()
    cb.set_ticks([0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
    cb.set_ticklabels([0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
    for l in cb.ax.yaxis.get_ticklabels():
        l.set_family('Times New Roman')
        l.set_size(12)
    xlocations = np.array(range(len(labels)))
    plt.xticks(xlocations, labels, rotation=90, fontproperties='Times New Roman', size=12)
    plt.yticks(xlocations, labels, fontproperties='Times New Roman', size=12)
    plt.ylabel('Reference', fontdict=fontInfo)
    plt.xlabel('Prediction', fontdict=fontInfo)


cm = confusion_matrix(y_true, y_pred)
print(cm)
print(accuracy_score(y_true, y_pred))
print(classification_report(y_true, y_pred, target_names=labels))
np.set_printoptions(precision=2)
cm_normalized = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
# print(cm_normalized)
plt.figure(figsize=(12, 8), dpi=400)

ind_array = np.arange(len(labels))
x, y = np.meshgrid(ind_array, ind_array)

for x_val, y_val in zip(x.flatten(), y.flatten()):
    c = cm_normalized[y_val][x_val]
    if c >= 0.01:
        thresholdColor = 'w'
        if c <= 0.5:
            thresholdColor = 'k'
        plt.text(x_val, y_val, "%0.2f" % (c,), color=thresholdColor, family='Times New Roman',
                 fontsize=10, va='center', ha='center')
# offset the tick
plt.gca().set_xticks(tick_marks, minor=True)
plt.gca().set_yticks(tick_marks, minor=True)
plt.gca().xaxis.set_ticks_position('none')
plt.gca().yaxis.set_ticks_position('none')
plt.grid(True, which='minor', linestyle='-', linewidth=1)
plt.gcf().subplots_adjust(bottom=0.15)

plot_confusion_matrix(cm_normalized, title='Normalized Confusion Matrix')
# show confusion matrix
plt.savefig(
    'C:/Users/thril/Desktop/confusion_matrix_ALL.png', format='png')
# plt.show()
