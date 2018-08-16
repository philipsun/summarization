﻿#-------------------------------------------------------------------------------
# Name:        sxpFenciMakeTFIDF
# Purpose:
#
# Author:      sunxp
#
# Created:     07-04-2015
# Copyright:   (c) sunxp 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import jieba
import jieba.posseg as pseg
import re
import pickle
from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
from scipy.sparse import csr_matrix


class sxpTFIDF:
    ct = None #vectorizer.fit_transform(corpus)#ct crs_matrix
    tfidf = None #transformer.fit_transform(ct)#tf-idf matrix crs_matrix
    word = None #vectorizer.get_feature_names()  #所有文本的关键字 list
    weight = None #tfidf.toarray()
    def GetKeywordCount(self):
        return len(self.word)

    def GetWeightArray(self):
        return self.tfidf.toarray()
    def GetKeyword(self, i):
        return self.word[i]
    def GetXY(self, x,y):
        [r,c] = self.ct.shape
        if x>= c or y >= r:
            return None
        else:
            return [self.ct[x,y],self.tfidf[x,y]]
    def GetCTRow(self, i):
        [r,c] = self.ct.shape
        if i>= r:
            return None
        else:
            return self.ct.getrow(i).toarray()#numpy.ndarray
##        c = np.ndarray()
##        c = np.ndarray()

    def GetCTCol(self, i):
        [r,c] = self.ct.shape
        if i>= c:
            return None
        else:
            return self.ct.getcol(i).toarray()#numpy.ndarray
    def GetWeightRow(self, i):
        [r,c] = self.tfidf.shape
        if i>= r:
            return None
        else:
            return self.tfidf.getrow(i).toarray()#numpy.ndarray
    def GetWeightCol(self, i):
        [r,c] = self.tfidf.shape
        if i>= c:
            return None
        else:
            return self.tfidf.getcol(i).toarray()#numpy.ndarray

## ctnzero = ct.nonzero()
##        r = ctnzero[0]
##        c = ctnzero[1]
##        for i in range(len(r)):
##            x= r[i] #document index
##            y=c[i]  #keyword index
##            count= ct[x,y]
##            weight=tfidf[x,y]
##            w = word[y]
def SaveSxpTFIDF(fname, sxptfidf):
        print('store sxptfidf at:',fname)
        with open(fname, 'w') as f:            # open file with write-mode
            picklestring = pickle.dump(sxptfidf, f)   # serialize and save object
        f.close()
        print('finishedsxptfidf at:')
def LoadSxpTFIDF(fname):
        print('load sxptfidf at:',fname)
        with open(fname, 'w') as f:            # open file with write-mode
##            picklestring = pickle.dump(sxptfidf, f)   # serialize and save object
            sxptfidf = pickle.load(f)
        f.close()
        print('finishedsxptfidf at:')
        return sxptfidf

def SegStrSet(strcontent):
    seg_list = jieba.cut(strcontent,cut_all=False)
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
def SegStrComplex(strcontent):
    seg_list = jieba.cut(strcontent,cut_all=False)
    result = []
    strspace= ' '
    for seg in seg_list:
        useg = seg.encode('utf-8')
        strspace = strspace + useg
    if isinstance(strspace,unicode):
        strspace = strspace.decode('utf-8')
    return strspace

def SegStr(strcontent):
    seg_list = jieba.cut(strcontent,cut_all=False)
    result = []
    for seg in seg_list:
        useg = seg.encode('utf-8')
        if not isMark(useg):
           result.append(seg.encode("utf-8"))
    segstr = ' '.join(result)
    if isinstance(segstr,unicode):
        segstr = segstr.decode('utf-8')
    return segstr
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
def MakeTFIDFForCorpus(docset):
    print 'begin to load and fenci file',len(docset)
    corpus = []
    sxptfidf = sxpTFIDF()
    for docstr in docset:
    #****************Fenci*****************
       segcontent = SegStrComplex(docstr)
      # print segcontent
    #**************************************
       corpus.append(segcontent)
    #****************MakeTFIDF*****************
    print 'begin to make tfidf',len(corpus)
 #   vectorizer = CountVectorizer(stop_words=None)
    vectorizer = CountVectorizer(analyzer = "word",   \
                             tokenizer = None,    \
                             preprocessor = None, \
                             token_pattern = u'(?u)\\b\S+\\b',\
                             stop_words = None)
    transformer = TfidfTransformer()
    sxptfidf.ct =vectorizer.fit_transform(corpus)#ct

    sxptfidf.tfidf = transformer.fit_transform(sxptfidf.ct)#tf-idf matrix
    sxptfidf.word = vectorizer.get_feature_names()  #所有文本的关键字
##    for w in sxptfidf.word:
##        print w
##    sxptfidf.weight = sxptfidf.tfidf.toarray()
    print 'finished'
    return sxptfidf
def TestTFIDF():
    docset = [u'hello this is a U.S. test, and we are 你好 going to  let the test 100 run', u'we can make a simple analysis in this work']
    seg = SegStrComplex(docset[0])
    print seg
    sxptfidf = MakeTFIDFForCorpus(docset)
    kn = sxptfidf.GetKeywordCount()
    for i in range(kn):
        print sxptfidf.GetKeyword(i)
        #print type(sxptfidf.GetCTCol(i))
def TestNumpyMatrix():

    a = np.eye(5, 5)
    a[0,3]=2
    a[3,0]=2
    a[4,2]=2
    a[3,2]=2

    a = csr_matrix(a)
    print a
    dense = np.asarray(a.todense())
    column = np.asarray(a.getcol(2).todense()).reshape(-1)


    print "dense"
    # operations on full dense matrix
    print "1"
    print csr_matrix( np.vstack([ line for line in dense if line[2] == 1 ]) )
    print "2"
    print csr_matrix( np.vstack([ line for line in dense if line[2] == 0 ]) )

    print "sparse"
    # Operations on sparse matrix
    result1 = []
    result2 = []
    for irow in range(a.shape[0]):
        if column[irow] == 1:
            [ result1.append( (irow,indice) ) for indice in a[irow].indices   ]
        else :
            [ result2.append( (irow,indice) ) for indice in a[irow].indices   ]

    print result1,result2

    result3 =[]
    print 'my sparse visit'
    for irow in range(a.shape[0]):
    ##    if column[irow] == 1:
    ##        [ result1.append( (irow,indice) ) for indice in a[irow].indices   ]
    ##    else :
    ##        [ result2.append( (irow,indice) ) for indice in a[irow].indices   ]
    ##
        [ result3.append( (irow,indice) ) for indice in a[irow].indices ]
    print result3
    print 'my sparse visit 1'
    a = np.matrix('1 2; 3 4 ; 5 6')
    a = csr_matrix(a)
    print a
    b = a.getrow(1)
    b = a.getcol(1)
    nzero = b.nonzero()
        #print ct
    r = nzero[0]
    c = nzero[1]
    print r
    print c

    for i in range(len(r)):
        x= r[i]
        y=c[i]
        print a[x,y]
def main():
    TestTFIDF()
if __name__ == '__main__':
    main()