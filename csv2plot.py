## author : charlie
## date : 20220118

import matplotlib.pyplot as plt

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

plt.plot(time_list, rmsd_list)
plt.xlabel("Time (ns)")
plt.ylabel(yname)
plt.show()



print("Good day !")
