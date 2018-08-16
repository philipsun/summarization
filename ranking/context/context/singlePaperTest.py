__author__ = 'a'
#from Controller import *
from SinglePaperController import *
modeldir = r'D:\pythonwork\code\paperparse\paper\papers\model'
systemdir = r'D:\pythonwork\code\paperparse\paper\papers\system'
def sxpGetDirFileSubList(filedir):
    if not os.path.exists(filedir):
        print 'no dir to be read'
        return []
    filelist = []
    subdirlist = []
    try:
        files = os.listdir(filedir)
        #now we first read each file in the txtPath
        for f in files:
          df = os.path.join(filedir, f)
          if os.path.isdir(df):
             subdirlist.append(f)
          else:
             filelist.append(f)
    except Exception as e:
        msg = filedir + ':' + str(e)
        print msg
    return filelist, subdirlist
def GetSystemDir():
    subfile, subdir = sxpGetDirFileSubList(systemdir)
    systemsub_set = []
    for eachsub in subdir:
        subdirfull = systemdir + '\\' + eachsub
        systemsub_set.append(subdirfull)
    return systemsub_set
def TestDir():
    print modeldir
    print GetSystemDir()
def main():
    #path = r'C:\Users\a\PycharmProjects\extractInfo\papers'
    path = r'D:\pythonwork\code\paperparse\paper\papers'
    evaluate_all_forjava(path, 'context1',10,1,0)
    evaluate_all_forjava(path, 'mymodel',10,1,0)
    evaluate_all_forjava(path, 'tfidf',10,1,0)
    evaluate_all_forjava(path, 'graphb',10,1,0)
    evaluate_all_forjava(path, 'graphw',10,1,0)
def Evaluate_forpyroute():
    path = r'D:\pythonwork\code\paperparse\paper\papers'
    evaluate_all(path, 'context1',10,1,0)
    evaluate_all(path, 'mymodel',10,1,0)
    evaluate_all(path, 'tfidf',10,1,0)
    evaluate_all(path, 'graphb',10,1,0)
    evaluate_all(path, 'graphw',10,1,0)
def Evaluate_singlepaper():
    modelpath = r'D:\pythonwork\code\paperparse\paper\single\model'
    pkpath = r'D:\pythonwork\code\paperparse\paper\single\pk'
    systempath = r'D:\pythonwork\code\paperparse\paper\single\system'
    evaluate_singpaper(pkpath,modelpath,systempath, 'context1')
    evaluate_singpaper(pkpath,modelpath,systempath, 'mymodel')
    evaluate_singpaper(pkpath,modelpath,systempath, 'tfidf')
    evaluate_singpaper(pkpath,modelpath,systempath, 'graphb')
    evaluate_singpaper(pkpath,modelpath,systempath, 'graphw')
if __name__ == '__main__':
    #Evaluate_forpyroute()
    Evaluate_singlepaper()