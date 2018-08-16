#-------------------------------------------------------------------------------
# Name:        sxpPLot
# Purpose:
#
# Author:      sunxp
#
# Created:     23/04/2015
# Copyright:   (c) sunxp 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#coding: utf-8
import time
import random
import matplotlib.pyplot as plt
import numpy as np
def sxpPlotScatter(data,title,xlabel,ylabel):
    n = len(data)
    xtick = range(1,n+1)
    plt.figure()
    plt.plot(xtick,data,'bs')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.show()

def sxpPlotHist(data,title,xlabel,ylabel):

    plt.figure()
    n, bins,patches = plt.hist(data,50,normed=1,alpha=0.75,cumulative=1)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.show()
    time.sleep(1)
def sxpPlotHistBin(data,title, xlabel, ylabel):
    y = np.bincount(data)
    x = np.nonzero(y)[0]
    print x
    print y
    print(zip(x,y[x]))
    bs = zip(x,y[x])
    zipped= sorted(bs,reverse=True,key=lambda x:x[1])
    x,y = zip(*zipped)
    plt.bar(x,y)
##    plt.bar(*(zip(x,y[x]).sort()))
    plt.show()
def sxpPlotSortedHistBin(data,title, xlabel, ylabel):
    y = np.bincount(data)
    x = np.nonzero(y)[0]
    sy = sorted(y[x],reverse=True)
    x = range(1,len(sy)+1)

#    plt.bar(x,sy)
    plt.plot(x,sy,'bs')

##    plt.bar(*(zip(x,y[x]).sort()))
    plt.show()
def sxpPlotHistRange(data,title,xlabel,ylabel):
    plt.hist(data, bins=range(max(data)+2))
    plt.show()
def testshow():
    data = [random.randrange(1,10,1) for i in range(10)]
    title = 'random'
    xlabel = 'x'
    ylabel = 'y'
#    sxpPlotScatter(data,title,xlabel,ylabel)
#    sxpPlotHist(data,title,xlabel,ylabel)
#    sxpPlotHistBin(data,title,xlabel,ylabel)
#    sxpPlotHistRange(data,title,xlabel,ylabel)
    sxpPlotSortedHistBin(data,title,xlabel,ylabel)
def Test():
    a = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    print(zip(*a))
    print(map(list,zip(*a)))

    data =[random.randrange(1,10,1) for i in range(10)]
    y = np.bincount(data)
    x = np.nonzero(y)[0]
    print x
    print y
    print(zip(x,y[x]))
    bs = zip(x,y[x])
    print sorted(bs,key=lambda x:x[1])
    zipped= sorted(bs,reverse=True,key=lambda x:x[1])
    print zipped
    x,y = zip(*zipped)
    print x
    print y

def main():
    testshow()
    #Test()
if __name__ == '__main__':
    main()
