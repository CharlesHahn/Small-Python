## author : charlie
## date : 20220121

import argparse
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import matplotlib.pylab as pylab

# params to control plot
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


def read_xvg(inputfile:str) -> tuple:
    """extract xaxis, yaxis, time_list, rmsd_list from xvg file """

    ## read xvg file
    with open(inputfile, "r") as fo:
        lines = fo.readlines()

    ## deal with content of rmsd.xvg
    xaxis, yaxis = "", ""
    time_list, rmsd_list = [], []

    ## remove empty line
    lines = [ line.strip() for line in lines if len(line) != 0 ]

    for line in lines:
        ## ignore all lines started with #
        if line[0] == "#":
            continue
        
        ## get the axis info
        if line[0] == "@":
            if "xaxis" in line:
                xaxis = line.strip('"').split('"')[-1]
            if "yaxis" in line:
                yaxis = line.strip('"').split('"')[-1]

        ## deal with data line
        if not line.startswith("@") and not line.startswith("#"):
            items = line.split()
            time_list.append(float(items[0]))
            rmsd_list.append(float(items[1]))

    ## check length of time_list and rmsd_list
    if len(time_list) != len(rmsd_list):
        print("Wrong in length of time_list and rmsd_list")
        print("time_list -> {} ; rmsd_list -> {}".format(
            len(time_list), len(rmsd_list)))
        exit()
    
    return xaxis, yaxis, time_list, rmsd_list


def read_csv(inputfile:str) -> tuple:
    """ read xaxis, yaxis, time_list, rmsd_list from csv file """

    ## read data
    with open(inputfile, 'r') as fo:
        lines = fo.readlines()
    
    ## get xaxis and yaxis
    items = lines[0].split(",")
    xaxis = items[0].strip()
    yaxis = items[1].strip()
    
    ## get data
    time_list, rmsd_list = [], []
    for line in lines[1:]:
        items = line.strip().split(",")
        time_list.append(float(items[0].strip()))
        rmsd_list.append(float(items[1].strip()))

    ## check length of time_list and rmsd_list
    if len(time_list) != len(rmsd_list):
        print("Wrong in length of time_list and rmsd_list")
        print("time_list -> {} ; rmsd_list -> {}".format(
            len(time_list), len(rmsd_list)))
        exit()

    return xaxis, yaxis, time_list, rmsd_list


def save_csv(xaxis:str, yaxis:str, time_list:list, rmsd_list:list,
             outputfile:str) -> None:
    """save xaxis, yaxis, time_list, rmsd_list into csv file """
    with open(outputfile, 'w') as fo:
        fo.write(xaxis + ", " + yaxis + "\n")
        for i in range(len(time_list)):
            fo.write("{}, {}\n".format(time_list[i], rmsd_list[i]))
    
    print("Save data to {} successfully !".format(outputfile))


def draw_rmsd(xaxis:str, yaxis:str, time_list:list, rmsd_list:list,
              outputfile:str) -> None:
    """ plot rmsd vs time """

    ## moving average
    # rmsd_ave = pd.Series(rmsd_list).rolling(50).mean().tolist()
    windowsize = 50
    mv_ave = [ np.nan for i in range(windowsize)]
    low = [ np.nan for i in range(windowsize)]
    high = [ np.nan for i in range(windowsize)]

    ## calculate mv_ave, low and high
    for i in range(windowsize, len(rmsd_list)):
        window_data = rmsd_list[i-windowsize:i]
        ave = np.mean(window_data)
        std = np.std(window_data)
        interval = stats.norm.interval(0.95, ave, std)
        mv_ave.append(ave)
        low.append(interval[0])
        high.append(interval[1])
    print(len(mv_ave), len(low), len(high))

    ## plot rsmd vs time
    # plt.plot(time_list, rmsd_list, alpha=0.5, label="origin rmsd")
    plt.plot(time_list, mv_ave, color="k", label="moving average")
    plt.fill_between(time_list, low, high, color="grey", alpha=0.5)
    plt.xlabel(xaxis)
    plt.ylabel(yaxis)
    plt.xlim(min(time_list)-1000, max(time_list)+1000)
    plt.legend()
    plt.savefig(outputfile)
    plt.show()


def get_argv() -> tuple:
    """ get command line argvs by argparse """

    ## parse command line argvs
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", required=True, help="input file")
    parser.add_argument("-o", required=True, help="output file")
    args = parser.parse_args()

    ## check filename
    inputfile = args.i 
    outputfile = args.o
    suffix = [".csv", ".png", ".xvg"]
    if inputfile[-4:] not in suffix:
        print("Wrong -> No support for your input file type !", 
              "please make sure its suffix is .csv, .xvg or .png")
        exit()
    if outputfile[-4:] not in suffix:
        print("Wrong -> No support for your output file type !", 
              "please make sure its suffix is .csv, .xvg or .png")
        exit()
    
    return inputfile, outputfile


def main():
    ## parse command line argvs
    inputfile, outputfile = get_argv()

    ## control flow by argvs
    if inputfile.split(".")[1] == "xvg":
        xaxis, yaxis, time_list, rmsd_list = read_xvg(inputfile)
        if outputfile.split(".")[1] == "csv":
            save_csv(xaxis, yaxis, time_list, rmsd_list, outputfile)
        elif outputfile.split(".")[1] == "png":
            draw_rmsd(xaxis, yaxis, time_list, rmsd_list, outputfile)
        else:
            print("Wrong -> the output file can only be csv file or png file")
            exit()
    
    elif inputfile.split(".")[1] == "csv":
        xaxis, yaxis, time_list, rmsd_list = read_csv(inputfile)
        if outputfile.split(".")[1] == "csv":
            save_csv(xaxis, yaxis, time_list, rmsd_list, outputfile)
        elif outputfile.split(".")[1] == "png":
            draw_rmsd(xaxis, yaxis, time_list, rmsd_list, outputfile)
        else:
            print("Wrong -> the output file can only be csv file or png file")
            exit()

    else:
        print("Wrong -> the input file can only be xvg file or csv file")
        exit()



if __name__ == "__main__":
    main()
