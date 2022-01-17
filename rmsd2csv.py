## author : charlie
## date : 20220116

## read rmsd.xvg
with open("rmsd.xvg", "r") as fo:
    lines = fo.readlines()

## deal with content of file
xaxis, yaxis = "", ""
time_list, rmsd_list = [], []

## remove empty line
lines = [ line for line in lines if len(line) != 0]

for line in lines:
    ## ignore all # line
    if line[0] == "#":
        continue

    ## get the axis info
    if line[0] == "@":
        if "xaxis" in line:
            xaxis = line.strip().strip('"').split('"')[-1]
        if "yaxis" in line:
            yaxis = line.strip().strip('"').split('"')[-1]

    ## deal with data line
    if not line.startswith("@") and not line.startswith("#"):
        items = line.strip().split()
        time_list.append(float(items[0]))
        rmsd_list.append(float(items[1]))

## check length of time_list, rmsd_list
if len(time_list) != len(rmsd_list):
    print("Wrong in length of time_list and rmsd_list")
    exit()
## print(len(time_list), len(rmsd_list))

## save date csv file
with open("rmsd.csv", 'w') as fo:
    fo.write(xaxis+", "+yaxis+"\n")
    for i in range(len(time_list)):
        fo.write("{}, {}\n".format(time_list[i], rmsd_list[i]))

print("Good day !")

