## author : charlie
## date : 20220118

import matplotlib.pyplot as plt
from matplotlib import pylab as pylab

# 绘图控制参数
myparams = {
    'axes.labelsize'  : '14',
    'xtick.labelsize' : '14',
    'ytick.labelsize' : '14',
    'ytick.direction' : 'in', 
    # 'xtick.bottom'    : False,
    'xtick.bottom'    : True,
    'xtick.direction' : 'in',
    'lines.linewidth' : '2',
    'axes.linewidth'  : '1',
    'legend.fontsize' : '14',
    #'legend.loc'     : 'upper right',
    'legend.fancybox' : False,
    'legend.frameon'  : False,
    'font.family'     : 'Arial',
    # 'figure.dpi'      : 300,
    'savefig.dpi'     : 300,
}
pylab.rcParams.update(myparams)


## read csv file
with open("rmsd.csv", 'r') as fo:
    lines = fo.readlines()

## deal with data
xname, yname = lines[0].split(",")[0], lines[0].split(",")[1].strip()
time_list, rmsd_list = [], []
for line in lines[1:]:
    items = line.strip().split(",")
    time_list.append(float(items[0].strip()))
    rmsd_list.append(float(items[1].strip()))

time_list = [ t/1000 for t in time_list ]

## plot time vs rmsd

plt.plot(time_list, rmsd_list, label="test")
plt.xlabel("Time (ns)")
plt.ylabel(yname)
plt.legend()
plt.show()



print("Good day !")
