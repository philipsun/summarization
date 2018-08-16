#this file contains some classes that are to read text files
#coding=UTF-8
import codecs
import os
import sxpTextEncode
import pickle
def CheckDir(dirstr):
    if os.path.exists(dirstr) == False:
        os.path.os.mkdir(dirstr)
        print 'ok, we make dir',dirstr
    print 'ok',dirstr
def StoreSxptext(sxptxt, fname):
    f = open(fname,'wb')
    pickle.dump(sxptxt,f)
    f.close()
def LoadSxptext(fname):
    f = open(fname,'rb')
    sxptxt = pickle.load(f)
    f.close()
    return sxptxt
def IsType(fname,typename):
    fs = fname.split('.')
    if fs[-1] == typename:
        return True;
    else:
        return False
def GetDirFileList(filedir):
    if not os.path.exists(filedir):
        print 'no dir to be read'
        return []
    filelist = []
    files = os.listdir(filedir)
    #now we first read each file in the txtPath
    for f in files:
      if os.path.isdir(os.path.join(filedir, f)):
         pass
      else:
         filelist.append(f)
    return filelist
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


