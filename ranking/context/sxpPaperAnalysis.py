#-------------------------------------------------------------------------------
# Name:        sxpPaperAnalysis
# Purpose:
#
# Author:      sunxp
#
# Created:     30/03/2015
# Copyright:   (c) sunxp 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#coding: utf-8
import sxpLoadWeb
import re
from bs4 import BeautifulSoup
import sxpLatexHTMLParse
import urlparse
import sxpPPT
import sxpProcessParaText
import sxpFenciMakeTFIDF
import sxpParseDivPara
import sxpExtractText
import sxpJudgeCharacter
import pickle
import numpy as np
from scipy.sparse import csr_matrix
from scipy import *
import warnings
import os


##class sxpTFIDF:
##    ct = None #vectorizer.fit_transform(corpus)#ct crs_matrix
##    tfidf = None #transformer.fit_transform(ct)#tf-idf matrix crs_matrix
##    word = None #vectorizer.get_feature_names()  #所有文本的关键字 list
##    weight = None #tfidf.toarray()
##    def GetKeywordCount(self):
##        return len(self.word)
##
##    def GetWeightArray(self):
##        return self.tfidf.toarray()
##    def GetKeyword(self, i):
##        return self.word[i]
##    def GetXY(self, x,y):
##        [r,c] = self.ct.shape
##        if x>= c or y >= r:
##            return None
##        else:
##            return [self.ct[x,y],self.tfidf[x,y]]
##    def GetCTRow(self, i):
##        [r,c] = self.ct.shape
##        if i>= r:
##            return None
##        else:
##            return self.ct.getrow(i).toarray()#numpy.ndarray
####        c = np.ndarray()
####        c = np.ndarray()
##
##    def GetCTCol(self, i):
##        [r,c] = self.ct.shape
##        if i>= c:
##            return None
##        else:
##            return self.ct.getcol(i).toarray()#numpy.ndarray
##    def GetWeightRow(self, i):
##        [r,c] = self.tfidf.shape
##        if i>= r:
##            return None
##        else:
##            return self.tfidf.getrow(i).toarray()#numpy.ndarray
##    def GetWeightCol(self, i):
##        [r,c] = self.tfidf.shape
##        if i>= c:
##            return None
##        else:
##            return self.tfidf.getcol(i).toarray()#numpy.ndarray


class sxpText:
    fname = ''
    title = ''
    abstract = ''
    relatedwork = ''
    conclusion = ''
    reference = ''
    section_id_dict =[]
    section_list = []
    paraset = []
    whole_sectitle = ''
    whole_text = ''
    keycount = None
    para_tfidf = None
    sentence_tfidf = None
    sentenceset = []
    d_c = None
    c_p = None
    p_s = None
    s_k = None
    def __init__(self):
        self.fname = ''
        self.title = ''
        self.abstract = ''
        self.relatedwork = ''
        self.conclusion = ''
        self.reference = ''
        self.section_id_dict =[]
        self.section_list = []
        self.paraset = []
        self.whole_sectitle = ''
        self.whole_text = ''
        self.keycount = None
        self.para_tfidf = None
        self.sentence_tfidf = None
        self.sentenceset = []
        self.d_c = None
        self.c_p = None
        self.p_s = None
        self.s_k = None


class sxpSectionTitle:
    title = ''
    id_str = ''
    id_set = ''
    level = 0
    id = 0
    t_type = ''
    def __init__(self):
        self.title = ''
        self.id_str = ''
        self.id_set = ''
        self.level = 0
        self.id = 0
        self.t_type = ''

class sxpPara:
    para_id = ''
    para_text = ''
    para_tuple = []
    para_tfidf =[]
    section_title=''
    sentenceset = []
    id = 0
    id_sec = 0
    def __init__(self):
        self.para_id = ''
        self.para_text = ''
        self.para_tuple = []
        self.para_tfidf =[]
        self.section_title=''
        self.sentenceset = []
        self.id = 0
        self.id_sec = 0
class sxpSent:
    sentence_text = ''
    id = 0
    id_para = 0
    def __init__(self):
        self.sentence_text = ''
        self.id = 0
        self.id_para = 0
paperpath = r'D:\pythonwork\code\paperparse\paper\papers'
def FindStr(pattern,strsrc):
    p = re.compile(pattern)
    return p.match(strsrc)
def ParseOnePaper(fname):
    print 'load file'
    papersrc = sxpLoadWeb.LoadFile(fname)
    papersrc = sxpJudgeCharacter.ReplaceNonEnglishCharacter(papersrc)
#    papersrc = repr(papersrc.decode('utf-8','ignore').encode('utf-8'))
#    papersrc = papersrc.replace(r'\n',' ')
   # print papersrc
    soup = BeautifulSoup(papersrc,from_encoding = 'utf-8')
   # titleitem = soup.findAll(attr={"class":"ltx_title ltx_title_document"})
    titleitem = soup.find_all(class_=re.compile("ltx_title"))
    sxptxt = sxpText()
    sxptxt.fname = fname;
    sectionset = []
    sectiontitle ={}
    whole_section_title =''
    section_id_dict = {}
    whole_text = ''
    print 'load section title'
    sxpdoc = sxpSectionTitle()
    sxpdoc.id = 0
    sxpdoc.title = 'doc'
    sxpdoc.id_str = 'top'
    sxpdoc.level = 0
    sxpdoc.t_type = 'doc'
    section_id_dict['root']=0
    section_list =[]
    section_list.append(sxpdoc)
    sec_id = 1
    for t in titleitem:
        sxpsec = sxpSectionTitle()
        tp = t.parent
        if tp.has_attr('id'):
            sid = tp['id'].lower()
        elif tp.has_attr('class'):
            if tp['class'][0]=='ltx_abstract':
                sid = 'abstract'
            else:
                sid = 'top'
        else:
            sid = 'top'
        cls = t['class']
        sxpsec.id_str = sid;
        sxpsec.id_set = ParseParaID(sid)
        sxpsec.title = t.text
        sxpsec.level = len(sxpsec.id_set)
        whole_section_title = whole_section_title + '\n' + t.text
        if len(cls)>=1:
            t_type = cls[0]
        else:
            t_type = 'none'
        if len(cls) == 2:
            t_type = cls[1]
            if t_type == 'ltx_title_document':
               sxptxt.title = t.text
            elif t_type == 'ltx_title_abstract':
                sxptxt.abstract = t.text
                whole_text = whole_text + t.text
            elif t_type == 'ltx_title_bibliography':
                sxptxt.reference = t.text
        if len(cls) == 1:
            t_type = cls[0]

        sxpsec.t_type =t_type
        sxpsec.id = sec_id
        ##section_id_dict.append(sxpsec)
        if section_id_dict.has_key(sxpsec.id_str) == True:
            print sxpsec.id_str, sxpsec.title
            os = section_id_dict[sxpsec.id_str]
           # section_list[os] = sxpsec
        else:
            section_id_dict[sxpsec.id_str]=sec_id
            sec_id = sec_id + 1
            section_list.append(sxpsec)
##    for s in sectionset:
##        print s.parent_id, s.text
    print sec_id
    sxptxt.section_id_dict = section_id_dict
    sxptxt.whole_sectitle = whole_section_title
##    for sec in section_list:
##        print sec.id
#*******************matrix to be built***********

#**************************************************************
#*********Following is to extract the paragraph and its section title
##    print 'begin to find all ltx_para'
##    soup = BeautifulSoup(papersrc,from_encoding = 'utf-8')
##    paraset = []
##    ltx_paraset = soup.find_all(class_=re.compile("ltx_para"))
    print 'parse para'

    para_textset = []
    ltx_paraset = sxpParseDivPara.ExtractParagraph(papersrc)
    #for each paragraph:
    id_para = 0
    id_sent = 0
    sentence_textset = []
    for para in ltx_paraset:
        sxp_para = sxpPara()
        #here we find the whole text of a paragraph
        sxp_para.para_text = para[1]
        para_textset.append(para[1])
        #for each paragraph, we extract its sentence
        sentenceset = sxpExtractText.MySentence(sxp_para.para_text)
        for sent in sentenceset:
            sxpsent = sxpSent()
            sxpsent.sentence_text = sent
            sxpsent.id = id_sent
            id_sent = id_sent + 1
            sxpsent.id_para = id_para
            sxptxt.sentenceset.append(sxpsent)
            sentence_textset.append(sent)
        whole_text = whole_text + '\n' + para[1]
##            print para['id'], para.text;
        pid = para[0].lower()
        sxp_para.para_id = pid
        #here we find the section id of the paragraph
        sxp_para.para_tuple = ParseSectionIDStr(pid)
        #here we find the section title of the para_graph
        #if we use dict to store section title, we will be more efficient here
        if section_id_dict.has_key(sxp_para.para_tuple[0]):
            sxpsec_id = section_id_dict[sxp_para.para_tuple[0]]
            sxpsec = section_list[sxpsec_id]
            sxp_para.section_title = sxpsec.title;
            sxp_para.id_sec = sxpsec.id
        else:
            uppersection = ParseUpperSection(sxp_para.para_tuple[0])
            while(len(uppersection) >0 ):
                if section_id_dict.has_key(uppersection):
                    sec_id = section_id_dict[uppersection]
                    sxpsec = section_list[sec_id]
                    sxp_para.section_title = sxpsec.title;
                    sxp_para.id_sec = sxpsec.id
                    break
                else:
                    uppersection = ParseUpperSection(uppersection)
            if len(uppersection) == 0:
                sxp_para.section_title = '';
                sxp_para.id_sec = 0
##        for sxpsec in section_id_dict:
##            if sxp_para.para_tuple is None:
##                print sxp_para
##            if sxp_para.para_tuple[0]== sxpsec.id_str:
##                sxp_para.section_title = sxpsec.title;
##                break;
##            else:
##                sxp_para.section_title = '';
        sxp_para.id = id_para
        if id_para == 46:
            br  = 1;
        id_para = id_para + 1
        sxptxt.paraset.append(sxp_para)

    sxptxt.whole_text = whole_text
    sxptxt.section_list = section_list
    print 'extract keycount'

#**************************************************************
#****************Now we try to extract the key counter of whole_text
    sxptxt.keycount = sxpProcessParaText.ExtractKeyCount(whole_text)

#**************************************************************
    print 'make tfidf'

#**************************************************************
#****************Now we try to extract the sentence from the whole_text
##    sxptxt.sentenceset = sxpExtractText.MySentence(whole_text)
##    return sxptxt
#**************************************************************

    sxptxt.para_tfidf = sxpFenciMakeTFIDF.MakeTFIDFForCorpus(para_textset)

    sxptxt.sentence_tfidf = sxpFenciMakeTFIDF.MakeTFIDFForCorpus(sentence_textset)

#***************************************************************
#****************Now we try to build several matrix for graphs can be
#               extracted from sxptxt
#***************************************************************
    print 'we begin to build matrix'
    cs = len(sxptxt.section_id_dict) #because we have 0 as the global doc and 1 as the section from the
    ps = len(sxptxt.paraset)
    ss = len(sxptxt.sentenceset)
    ks = len(sxptxt.sentence_tfidf.word)
    print cs, ps, ss, ks
#first we build d-c matrix, which is actually a row vector
    print 'd_c matrix'
    sxptxt.d_c = csr_matrix(np.ones((1,cs), dtype=np.float))
#then building c-p matrix
    print 'c_p matrix'
    sxptxt.c_p = csr_matrix((cs,ps), dtype=float)
    print 'start'
    print sxptxt.c_p.shape
    for para in sxptxt.paraset:
        c = para.id_sec
        p = para.id
##        print c, p
        sxptxt.c_p[c, p] = 1.0


#        sxptxt.c_p[p, c] = 1.0
#third, building p-s matrixx
    print 'p_s matrix'
    sxptxt.p_s = csr_matrix((ps, ss), dtype=float64)
    for sent in sxptxt.sentenceset:
        p = sent.id_para
        s = sent.id
        sxptxt.p_s[p,s] = 1.0
#        sxptxt.p_s[p,s] = 1.0
#fourth, building s-k matrix
    print 's_k matrix'
    sxptxt.s_k = csr_matrix(sxptxt.sentence_tfidf.tfidf)


    return sxptxt


def Parseltx_title(papersrc):
    print 'begin to parse paragraph'
    soup = BeautifulSoup(papersrc,from_encoding = 'utf-8')
   # titleitem = soup.findAll(attr={"class":"ltx_title ltx_title_document"})
    paraitemset = soup.find_all('p')
    i = 1
    paraset =[]
    for para in paraitemset:

        pp = para.parent#get parent id so that it can access the section id and name
        if pp.has_attr('id'):
            para_id = pp['id']
        elif pp.has_attr('class'):
            para_id = pp['class']
        else:
            para_id = 'no_id'
##        print i, ':',para_id, type(para_id),'*****'
        ptxt = sxpLatexHTMLParse.ParseHTMLContentStr(para.text)
#        print ptxt
        i = i + 1
        sxp_para = sxpPara()
        sxp_para.para_idset = ParseParaID(para_id)
        sxp_para.para_id = para_id
        sxp_para.para_tuple = ParseParaIDSetStr(para_id)
        sxp_para.para_text = ptxt;
        paraset.append(sxp_para)


#**************************************************************
    return paraset
def ParseUpperSection(sectionid):
    para_seg = sectionid.split('.')
    n = len(para_seg)
    upper = para_seg[0:n-1]
    if len(upper) == 0:
        return ''
    i = 0
    s = ''
    for u in upper:
        if i == 0:
            s = s+ u
        else:
            s = s + '.' + u
        i = i + 1
    return s
def ParseSectionIDStr(para_id):
    if isinstance(para_id,list):
        paraid_str = para_id[0]
    else:
        paraid_str = para_id
    para_seg = paraid_str.split('.')
    p = '^(s+)x*\d+'
    pp = '^(p+)x*\d+'
    sectstr= ''
    parastr = ''
    for seg in para_seg:
        g = re.match(p,seg,0)
        if g is not None:
            if len(sectstr)==0:
                sectstr = sectstr+seg
            else:
                sectstr = sectstr+'.'+seg
        g = re.match(pp,seg,0)
        if g is not None:
            if len(parastr)==0:
                parastr = parastr+seg
            else:
                parastr = parastr+'.'+seg
    if len(sectstr)==0:
        sectstr = paraid_str
    if len(parastr)==0:
        parastr = paraid_str
    return [sectstr, parastr]
def ParseParaIDSetStr(para_id):
    if isinstance(para_id,list):
        paraid_str = para_id[0]
    else:
        paraid_str = para_id
    if  paraid_str is not None:
        p = '(.+)\\.p(\d+)$'
        g = re.match(p,paraid_str,0)
        if g is not None:
            return g.groups()
        else:
            return [paraid_str,'0'];
    else:
        return['noid','0']
def ParseParaID(paraid_str):
    if isinstance(paraid_str,list):
        paraid_str = paraid_str[0]
    sec = paraid_str.split('.')
    pa = r'(\D+)(\d+)'
    seclevel = len(sec)
    if  sec is not None:
        secpara = []
        i = 0
        for secstr in sec:
            g = re.match(pa,secstr,0)
            if g is not None:
                secpara.append(g.groups())
            else:
                t = [secstr,'{0}'.format(i)]
                secpara.append(t)
            i = i + 1
        return secpara;
    else:
        return[]
def ValidateEmail(email):
    if len(email) > 0:
        if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email) != None:
            return 1
    return 0
def TestParsePaperPara():
    fname = paperpath + '\\' + 'P14-1010.xhtml'
    sxptxt = ParseOnePaper(fname)
def StoreSxptext(sxptxt, fname):
    f = open(fname,'wb')
    pickle.dump(sxptxt,f)
    f.close()
def LoadSxptext(fname):
    f = open(fname,'rb')
    sxptxt = pickle.load(f)
    f.close()
    return sxptxt

def SentenceParseOnePaper(fn):
    #fn = 'P14-1007.xhtml'
    fname = paperpath + '\\' + fn
    sxptxt = ParseOnePaper(fname)
    fpname = paperpath + '\\pickle\\' + fn +  '.pickle'
    StoreSxptext(sxptxt, fpname)
    sxptxt = LoadSxptext(fpname)
##    sxpPPT.MakePPTFromTextA(sxptxt)
    para_textset = []
    for sxpsec in sxptxt.section_list:
        print sxpsec.id, sxpsec.t_type, sxpsec.id_str, sxpsec.title
    for sxp_para in sxptxt.paraset:
        print sxp_para.id, sxp_para.id_sec, sxp_para.para_id,sxp_para.para_tuple,
        print sxp_para.section_title
        print sxp_para.para_text
        para_textset.append(sxp_para.para_text)

    sentenceset = sxptxt.sentenceset
    sentence_textset = []
    for sent in sentenceset:
        print sent.id, sent.id_para, sent.sentence_text
    tfid = sxptxt.sentence_tfidf
    print tfid.tfidf[1,1]
    print sxptxt.d_c.shape
    print sxptxt.c_p.shape
    print sxptxt.p_s.shape
    print sxptxt.s_k.shape
def SentenceParseOnePaperFile(fn):
    #fn = 'P14-1007.xhtml'
    print 'process', fn
    fname = paperpath + '\\' + fn
    sxptxt = ParseOnePaper(fname)
    fpname = paperpath + '\\pickle\\' + fn +  '.pickle'
    StoreSxptext(sxptxt, fpname)
    sxptxt = LoadSxptext(fpname)
    print sxptxt.d_c.shape
    print sxptxt.c_p.shape
    print sxptxt.p_s.shape
    print sxptxt.s_k.shape
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
def GetDirFileListA(filedir):
    if not os.path.exists(filedir):
        print 'no dir to be read'
        return []

    filelist = []
    files = os.listdir(filedir)
    for f in files:
       if f[0] == '.':
         pass
       else:
         filelist.append(f)
    return filelist,filedir
def ProcessFilesInDir():
    flist = GetDirFileList(paperpath)
    for fn in flist:
        SentenceParseOnePaperFile(fn)
def ListDir():
    flist = GetDirFileList(paperpath)
    print flist
def TestLoad():
    fn = 'P14-1007.xhtml'
    fname = paperpath + '\\' + fn
    sxptxt = LoadSxptext(fpname)
    tfid = sxptxt.sentence_tfidf
    print type(tfid.tfidf)
    r = tfid.GetCTRow(1)[0]
    print type(r)
    print np.nonzero(r)
    print sxptxt.d_c.shape
    print sxptxt.c_p.shape
    print sxptxt.p_s.shape
    print sxptxt.s_k.shape
def TestFile():
    fn = 'P14-1008.xhtml'
    SentenceParseOnePaper(fn)
def TestParse():
    sectionid = 's1.sss1.p1'
    print ParseUpperSection(sectionid)
def main():
    #TestFile()
    #TestLoad()
    ProcessFilesInDir()
    #ListDir()
if __name__ == '__main__':
    main()
