#this file contains some classes that are to read text files
#coding=UTF-8
import codecs
import os,sys
import sxpTextEncode
import re
import pickle
def GetFilePathName(fname):
    pt = '[\\|/]'
    pat = re.compile(pt)
    fs = pat.split(fname)
    if len(fs)==1:
        return fname
    else:
        return (fs[0:-1],fs[-1])
def StoreSxptext(sxptxt, fname):
    f = open(fname,'wb')
    pickle.dump(sxptxt,f)
    f.close()
def LoadSxptext(fname):
    f = open(fname,'rb')
    sxptxt = pickle.load(f)
    f.close()
    return sxptxt
def cur_file_dir():
     #获取脚本路径
     path = sys.path[0]
     #判断为脚本文件还是py2exe编译后的文件，如果是脚本文件，则返回的是脚本的目录，如果是py2exe编译后的文件，则返回的是编译后的文件路径
     if os.path.isdir(path):
         return path
     elif os.path.isfile(path):
         return os.path.dirname(path)
rootdir = r'D:\pythonwork\code\axureui'
rootdir = cur_file_dir()
logfilename =rootdir + r'\weblog\log.txt'
indexpage = rootdir + r'\templates\index.html'
startuipage = rootdir + r'\templates\start.htm'
webfileroot = rootdir + r'\webfile'
webfilerootpattern = webfileroot.replace(u'\\',u'\\\\').lower()

def GetWebFilePathName(s):
    patstr =u'd:\\\\pythonwork\\\\code\\\\axureui\\\\webfile(.+)'
    patstr =webfilerootpattern + '(.+)'
    pattern_pos = []
    pattern = re.compile(patstr)
    match = pattern.search(s)
    pat_name = 'url'
    filesuffixpatstr = r''
    while match:
        tg = match.groups()
        tgtxt = match.group()
        posd = match.span()
        match = pattern.search(s,posd[1])
        pattern_pos.append([tgtxt,posd,tg,pat_name,1,0])
        return tg[0]
    print ''
def TraverseDir(filedir):
    if not os.path.exists(filedir):
        print 'no dir to be read'
        return []
  #  print 'visit--->:',filedir, os.path.getmtime(filedir)

    filelist = []
    subdirlist = []
    files = os.listdir(filedir)
    #now we first read each file in the txtPath
    for f in files:
      df = os.path.join(filedir, f)
#      print df, ' : ', os.path.isdir(df)
      if os.path.isdir(df):
         subdirlist.append(df)
         dirstack.append(df.lower())
      else:
         filelist.append(f)
    for eachf in filelist:
        if eachf == 'axQuery.std.js':
            breakpoint = 1
        ff =  os.path.join(filedir, eachf).lower()

        urlpath = GetWebFilePathName(ff)
        if urlpath is None:
            print 'none in', ff
        else:
            urttype = GetURLFileType(eachf)
            webfile_dic[urlpath] = [ff,urttype]
            dirfile_list.append([ff,eachf,urlpath])
    while len(dirstack) > 0:
        next_subdir = dirstack.pop()
        TraverseDir(next_subdir)
    return filelist, subdirlist

def GetDir(filedir):
    if not os.path.exists(filedir):
        print 'no dir to be read'
        return []
  #  print 'visit--->:',filedir, os.path.getmtime(filedir)

    filelist = []
    subdirlist = []
    files = os.listdir(filedir)
    #now we first read each file in the txtPath
    for f in files:
      df = os.path.join(filedir, f)
#      print df, ' : ', os.path.isdir(df)
      if os.path.isdir(df):
         subdirlist.append(f)
      else:
         filelist.append(f)

    return filelist, subdirlist
def WriteStrFile(filename,txtstr,encodetype='gbk'):
        ut = sxpTextEncode.GetUnicode(txtstr)
   #     ut = ut.encode('utf-8')
        f = codecs.open(filename,'w+',encodetype)
        f.write(ut)
        f.close();


def ReadTextUTF(fname):
       try:
           f=file(fname)
           f = codecs.open(fname,'r','utf-8')
           txt = f.read()
           f.close()
           return txt
       except IOError:
            print('wrong in open')
            return []
       return textcontent
def ReadTextContent(fpathname):
        try:
            file = open(fpathname,'r')
            textcontent = file.read()
            file.close()
            return textcontent
        except IOError:
            print('wrong in open')
            return []
        return textcontent

def ReadALL(fpathname):
        print(fpathname)
        try:
            file = open(fpathname,'r')
            lineset = [];
            while 1:
                lines = file.readlines(100000)
                if not lines:
                   break
                for line in lines:
                  print(line);
                lineset = lineset + lines;

            file.close()
            return lineset
        except IOError:
            print('wrong in open')
            file.close();
            return []
        return lines
def ReadTxtLines(fpathname):
        try:
            file = open(fpathname,'r')
            lineset = [];
            while 1:
                line = file.readline()
                if not line:
                   break
                if len(line.strip())==0:
                    continue;
                else:
                    lineset.append(line);
            file.close()
            return lineset
        except IOError:
            print('wrong in open')
            file.close();
            return []
        return lines


