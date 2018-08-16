#-------------------------------------------------------------------------------
# Name:        sxpFenci
# Purpose:     this package is to provide a Chinese text segmentation function
#               interface for others to use, it will use jieba to do it
# Author:      sunxp
#
# Created:     27/01/2015
# Copyright:   (c) sunxp 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------
# encoding=utf-8
import os
import jieba
import jieba.posseg as pseg
import sys
import re
import time
import string
import json
import codecs
import pickle
from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
#reload(sys)
#sys.setdefaultencoding('utf-8')
#reload(sys) will make output invisible, so you need to update sys.stdout=stdout
# by import sys  stdout = sys.stdout reload(sys) sys.stdout = stdout
def getFileList(path):
  filelist = []
  files = os.listdir(path)
  for f in files:
    if f[0] == '.':
      pass
    else:
      filelist.append(f)
  return filelist,path

def fenci(filename,path,segPath):
  f = open(path +"/" + filename,'r+')
  file_list = f.read()
  f.close()

   #保存分词结果

  if not os.path.exists(segPath):
    os.mkdir(segPath)

  #对文档进行分词处理
  seg_list = jieba.cut(file_list,cut_all=True)
  #对空格，换行符进行处理
  result = []
  for seg in seg_list:
    seg = ''.join(seg.split())
    seg = seg.strip();
    reg = 'w+'
    r = re.search(reg,seg)
    if seg !='' and seg != '\r' and seg != '\n' and seg != '\t' and seg != '=' and seg != '[' and seg != ']' and seg != '(' and seg != ')' and not r:
      result.append(seg.encode("UTF-8"))

  #将分词后的结果用空格隔开，保存至本地
  f = open(segPath+"/"+filename+"-seg.txt","w+")
  f.write(' '.join(result))#using space to join segmented words of text
  f.close()

#读取已经分词好的文档，进行TF-IDF计算
def Tfidf(filelist,sFilePath,path):
  corpus = []
  for ff in filelist:
    fname = path +"/" + ff
    f = open(fname+"-seg.txt",'r+')
    content = f.read()
    f.close()
    corpus.append(content)

  vectorizer = CountVectorizer()
  transformer = TfidfTransformer()
  tfidf = transformer.fit_transform(vectorizer.fit_transform(corpus))#tf-idf matrix
  word = vectorizer.get_feature_names()  #所有文本的关键字
  weight = tfidf.toarray()


  if not os.path.exists(sFilePath):
    os.mkdir(sFilePath)

  for i in range(len(weight)):
    print u'----------writing all the tf-idf in the ',i,u'file into ', sFilePath+'/' +string.zfill(i,5)+".txt"
    f = open(sFilePath+"/"+string.zfill(i,5)+".txt",'w+')
    for j in range(len(word)):
      f.write(word[j].encode("utf_8") + "  " + str(weight[i][j]) + " ")
    f.close()

def sxpFenci(txtPath,segPath):
    filelist = []
    files = os.listdir(txtPath)
#now we first read each file in the txtPath
    for f in files:
       if f[0] == '.':
          pass
       else:
          filelist.append(f)
#now we will fenci each file in the filelist
    if not os.path.exists(segPath):
            os.mkdir(segPath)
    tfidfPath =os.path.join(txtPath,'/tfidf');
    if not os.path.exists(tfidfPath):
            os.mkdir(tfidfPath)
    for filename in filelist:
          print "Using jieba on " + filename
          f = open(txtPath +"/" + filename,'r+')
          file_content = f.read()
          f.close()
          #use jieba to fenci the document
          #using cut_all = True, means that all possible combination of segs are extracted, which is better for search engine
          #using cut_all = False, meanst that only the most accurate one segment is produce, which is better for content process.
          seg_list = jieba.cut(file_content,cut_all=False)
          #to process spaces and newline characters if there is
          #对空格，换行符进行处理
          result = []
          for seg in seg_list:
            seg = ''.join(seg.split())
            seg = seg.strip();
            reg = 'w+'
            r = re.search(reg,seg)
            if seg !='' and seg != '\r' and seg != '\n' and seg != '\t' and seg != '=' and seg != '[' and seg != ']' and seg != '(' and seg != ')' and not r:
              result.append(seg.encode("UTF-8"))

          #save this segment results to the local directory
          fname = os.path.join(segPath,filename)+"-seg.txt"
          f = open(fname,"w+")
         # f = open(segPath+"/"+filename+"-seg.txt","w+")
          f.write(' '.join(result))#using space to join segmented words of text
          f.close()
def sxpMakeTFIDF(txtPath, segPath,tfidfPath):
    filelist = []
    files = os.listdir(txtPath)
#now we first read each file in the txtPath
    corpus = []
    for f in files:
      if f[0] == '.':
         pass
      else:
         filelist.append(f)
      fname = segPath +"/" + f
      f = open(fname+"-seg.txt",'r+')
      content = f.read()
      f.close()
      corpus.append(content)

    vectorizer = CountVectorizer()
    transformer = TfidfTransformer()
    tfidf = transformer.fit_transform(vectorizer.fit_transform(corpus))#tf-idf matrix
    word = vectorizer.get_feature_names()  #所有文本的关键字
    weight = tfidf.toarray()
    if not os.path.exists(tfidfPath):
       os.mkdir(tfidfPath)

    for i in range(len(weight)):
      print u'----------writing all the tf-idf in the ',i,u'file into ', tfidfPath+'/' +filelist[i]+".tfidf.txt"
      f = open(tfidfPath+"/"+filelist[i]+".tfidf.txt",'w+')
      for j in range(len(word)):
          f.write(word[j].encode("utf_8") + "  " + str(weight[i][j]) + "\n")
      f.close()
def sxFenciStr(str,encodingstr,cut_all):
    seg_list = jieba.cut(str,cut_all=False)
    result = []
    for seg in seg_list:
        seg = ''.join(seg.split())
        seg = seg.strip();
        reg = 'w+'
        r = re.search(reg,seg)
        if seg !='' and seg != '\r' and seg != '\n' and seg != '\t' and seg != '=' and seg != '[' and seg != ']' and seg != '(' and seg != ')' and not r:
           result.append(seg.encode("utf-8"))
    return result
def isMark(mstr):
    seg = mstr.decode('utf-8')
    if seg ==u'' or seg == u'\r' or seg == u'\n' or seg == u'\t' or seg == u'=' or seg == u'[' or seg == u']' or seg == u'(' or seg == u')':
        return True
    if seg ==u'*' or seg == u':' or seg == u'.' or seg == u',' or seg == u'!' or seg == u'{' or seg == u'}' or seg == u'<' or seg == u'>':
        return True
    if seg == u'~' or seg == u'@' or seg == u'#' or seg == u'$' or seg == u'%' or seg == u'^' or seg == u'&' or seg == u';' or seg == u'?':
        return True
    if seg == u'\'' or seg == u'\"' or seg == u'-' or seg == u'+' or seg == u'\\' or seg == u'/' or seg == u'|' or seg == u'`' :
        return True
    if seg == u'\'' or seg == u'\"' or seg == u'-' or seg == u'+' or seg == u'\\' or seg == u'/' or seg == u'|' or seg == u'`' :
        return True
    if seg == u'，' or seg == u'。' or seg == u'：' or seg == u'；' or seg == u'（' or seg == u'）' or seg == u'“' or seg == u'”' :
        return True
    if seg == u'【' or seg == u'】' or seg == u'——' or seg == u'？' or seg == u'！' or seg == u'‘' or seg == u'《' or seg == u'》' :
        return True
    if seg == u'…' or seg == u'、':
        return True
    return False
def sxpFenciStrSkipMarks(str,encodingstr,cut_all):
    seg_list = jieba.cut(str,cut_all=False)
    result = []
    for seg in seg_list:
        seg = ''.join(seg.split())
        seg = seg.strip();
        reg = 'w+'
        r = re.search(reg,seg)
        useg = seg.encode('utf-8')
        if not isMark(useg) and not r:
           result.append(seg.encode("utf-8"))
    return result

def sxpFenciTFIDFDirJsonFile(txtPath, segPath):
    filelist = []
    files = os.listdir(txtPath)
#now we first read each file in the txtPath
    for f in files:
       if f[0] == '.':
          pass
       else:
          filelist.append(f)
#now we will fenci each file in the filelist
    if not os.path.exists(segPath):
            os.mkdir(segPath)
    tfidfPath =os.path.join(txtPath,'/tfidf');
    if not os.path.exists(tfidfPath):
            os.mkdir(tfidfPath)
    for filename in filelist:
          print "Using jieba on " + filename
          f = codecs.open(txtPath +"/" + filename,'r+','gbk')
          js =json.load(f,encoding='gbk')

          file_content = js[u't'] + ' ' + js[u'm']
          f.close()
          #use jieba to fenci the document
          #using cut_all = True, means that all possible combination of segs are extracted, which is better for search engine
          #using cut_all = False, meanst that only the most accurate one segment is produce, which is better for content process.
          seg_list = jieba.cut(file_content,cut_all=False)
          #to process spaces and newline characters if there is
          #对空格，换行符进行处理
          result = []
          for seg in seg_list:
              seg = ''.join(seg.split())
              seg = seg.strip();
              reg = 'w+'
              r = re.search(reg,seg)
              useg = seg.encode('utf-8')
              if not isMark(useg) and not r:
                 result.append(seg.encode("utf-8"))
          #save this segment results to the local directory
          fname = os.path.join(segPath,filename)+"-seg.txt"
          f = open(fname,"w+")
         # f = open(segPath+"/"+filename+"-seg.txt","w+")
          f.write(' '.join(result))#using space to join segmented words of text
          f.close()

#in this version, we do not store each tf-idf of each file, instead we just store the whole weight list

def sxpMakeTFIDFStore(txtPath, segPath,tfidfPath,timestr):
    filelist = []
    files = os.listdir(txtPath)
#now we first read each file in the txtPath
    corpus = []
    print('load corpus for all documents')
    for f in files:
      if f[0] == '.':
         pass
      else:
         filelist.append(f)
      fname = segPath +"/" + f
      f = open(fname+"-seg.txt",'r+')
      content = f.read()
      f.close()
      corpus.append(content)

    print('make tf-idf')

    vectorizer = CountVectorizer()
    transformer = TfidfTransformer()
    tfidf = transformer.fit_transform(vectorizer.fit_transform(corpus))#tf-idf matrix
    word = vectorizer.get_feature_names()  #所有文本的关键字
 #   weight = tfidf.toarray()
    if not os.path.exists(tfidfPath):
       os.mkdir(tfidfPath)

    fname = tfidfPath+'\\'+timestr+'.tfidf'
    print('store tf-idf at:',fname)
    with open(fname, 'w') as f:            # open file with write-mode
        picklestring = pickle.dump(tfidf, f)   # serialize and save object
    f.close()
    print('finished tf-idf at:')

    fname = tfidfPath+'\\'+timestr+'.word'
    print('store tf-idf at:',fname)
    with open(fname, 'w') as f:            # open file with write-mode
        picklestring = pickle.dump(word, f)   # serialize and save object
    f.close()
    print('finished word at:')

#this has problem with weight, so we donot try to do it yet
##    fname = tfidfPath+'\\'+timestr+'.weight'
##    print('store weight at:',fname)
##    with open(fname, 'w') as f:            # open file with write-mode
##        picklestring = pickle.dump(weight, f)   # serialize and save object
##    f.close()
##    print('finished word at:')

#following codes are to store every tf-idf file for each document
##    if not os.path.exists(tfidfPath):
##       os.mkdir(tfidfPath)
##
##    for i in range(len(weight)):
##      print u'----------writing all the tf-idf in the ',i,u'file into ', tfidfPath+'/' +filelist[i]+".tfidf.txt"
##      f = open(tfidfPath+"/"+filelist[i]+".tfidf.txt",'w+')
##      for j in range(len(word)):
##          f.write(word[j].encode("utf_8") + "  " + str(weight[i][j]) + "\n")
##      f.close()

if __name__ == '__main__':
    txtPath = 'D:/pythonwork/data/sn163/txt'
    segPath = 'D:/pythonwork/data/sn163/seg'
    tfidfPath = 'D:/pythonwork/data/sn163/tfidf'
##    sxpFenciTFIDFDirJsonFile(txtPath,segPath)
##    sxpMakeTFIDF(txtPath, segPath,tfidfPath)
    timestr = '2015-01-01'
    tfidfPath = 'D:/pythonwork/data/sn163/alltfidf'
    sxpMakeTFIDFStore(txtPath, segPath,tfidfPath,timestr)
