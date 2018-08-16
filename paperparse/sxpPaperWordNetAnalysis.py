#-------------------------------------------------------------------------------
# Name:        sxpPaperAnalysisA
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
import sxpParseSection
import sxpExtractText
import sxpJudgeCharacter
import pickle
import numpy as np
from scipy.sparse import csr_matrix
from scipy import *
import warnings
import os


class sxpText:
    fname = ''
    title = ''
    abstract = ''
    relatedwork = ''
    conclusion = ''
    reference = ''
    section_id_dict ={}
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
        self.section_id_dict ={}
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
    id_sec = 0
    def __init__(self):
        self.sentence_text = ''
        self.id = 0
        self.id_para = 0
paperpath = r'D:\pythonwork\code\paperparse\paper\papers'
def FindStr(pattern,strsrc):
    p = re.compile(pattern)
    return p.match(strsrc)
def TestParsSection():
    fn = 'P14-1007.xhtml'
    fname = paperpath + '\\' + fn
    papersrc = sxpLoadWeb.LoadFile(fname)
    papersrc = sxpJudgeCharacter.ReplaceNonEnglishCharacter(papersrc)
#    papersrc = repr(papersrc.decode('utf-8','ignore').encode('utf-8'))
#    papersrc = papersrc.replace(r'\n',' ')
   # print papersrc
    sec_set = sxpParseSection.ExtractSection(papersrc)
    section_id_dict ={}
    whole_section_title  = ''
    section_list  = []
    sec_id = 0
    for sec in sec_set:
        sxpsec = sxpSectionTitle()
        sxpsec.id = sec_id
        sxpsec.id_set = ParseParaID(sec.id_str)
        sxpsec.id_str = sec.id_str
        sxpsec.t_type = sec.title_type
        sxpsec.title = sec.title
        whole_section_title = whole_section_title + '\n' + sec.title
        if section_id_dict.has_key(sxpsec.id_str) == True:
            print sxpsec.id_str, sxpsec.title
           # section_list[os] = sxpsec
        else:
            section_id_dict[sxpsec.id_str]=sec_id
            sec_id = sec_id + 1
            section_list.append(sxpsec)
    if section_id_dict.has_key('top') == False:
        sxpdoc = sxpSectionTitle()
        sxpdoc.id = sec_id
        sxpdoc.title = 'doc'
        sxpdoc.id_str = 'top'
        sxpdoc.level = 0
        sxpdoc.t_type = 'doc'
        section_id_dict['top']=0
        section_list =[]
        section_list.append(sxpdoc)
    for sec in section_list:
        print sec.id, sec.id_str, sec.title
def ParseOnePaper(fname):
    print 'load file:', fname
    papersrc = sxpLoadWeb.LoadFile(fname)
    papersrc = sxpJudgeCharacter.ReplaceNonEnglishCharacter(papersrc)
#    papersrc = repr(papersrc.decode('utf-8','ignore').encode('utf-8'))
#    papersrc = papersrc.replace(r'\n',' ')
   # print papersrc
##    soup = BeautifulSoup(papersrc,from_encoding = 'utf-8')
##   # titleitem = soup.findAll(attr={"class":"ltx_title ltx_title_document"})
##    titleitem = soup.find_all("ltx_title ltx_title_section")
    sxptxt = sxpText()
    sxptxt.fname = fname;

    whole_text = ''
    print 'load section title'
##    for s in sectionset:
##        print s.parent_id, s.text
## Now first we extract section ti  ltes
    section_list = []
    whole_section_title =''
    section_id_dict = {}
    sec_set = sxpParseSection.ExtractSection(papersrc)
    sec_id = 0
    for sec in sec_set:
        sxpsec = sxpSectionTitle()
        sxpsec.id = sec_id
        sxpsec.id_set = ParseParaID(sec.id_str)
        sxpsec.id_str = sec.id_str.lower()
        sxpsec.t_type = sec.title_type
        sxpsec.title = sec.title
        whole_section_title = whole_section_title + '\n' + sec.title
        if section_id_dict.has_key(sxpsec.id_str) == True:
            print sxpsec.id_str, sxpsec.title
           # section_list[os] = sxpsec
        else:
            section_id_dict[sxpsec.id_str]=sec_id
            sec_id = sec_id + 1
            section_list.append(sxpsec)
    if section_id_dict.has_key('top') == False:
        sxpdoc = sxpSectionTitle()
        sxpdoc.id = sec_id
        sxpdoc.title = 'doc'
        sxpdoc.id_str = 'top'
        sxpdoc.level = 0
        sxpdoc.t_type = 'doc'
        section_id_dict['top']=0
        section_list =[]
        section_list.append(sxpdoc)

    sxptxt.section_id_dict = section_id_dict
    sxptxt.whole_sectitle = whole_section_title
##    for sec in section_list:
##        print sec.id

#**************************************************************
#*********First we add section title to paragraphs*************
    para_textset = []
    sentence_textset = []
    id_para = 0
    id_sent = 0
    for sec in section_list:
        sxp_para = sxpPara()
        sxp_para.para_text = sec.title
        sxp_para.id = id_para
        sxp_para.id_sec = sec.id
        sxp_para.para_id = sec.id_str
        para_textset.append(sxp_para.para_text)
        #add sentence
        sxpsent = sxpSent()
        sxpsent.sentence_text = sec.title
        sxpsent.id = id_sent
        id_sent = id_sent + 1
        sxpsent.id_para = id_para
        sxpsent.id_sec = -1
        sxptxt.sentenceset.append(sxpsent)
        sentence_textset.append(sec.title)
        whole_text = whole_text + '\n' + sec.title
        sxp_para.section_title = sxpsec.title;
        id_para = id_para + 1
        sxptxt.paraset.append(sxp_para)

#*********Following is to extract the paragraph and its section title
##    print 'begin to find all ltx_para'
##    soup = BeautifulSoup(papersrc,from_encoding = 'utf-8')
##    paraset = []
##    ltx_paraset = soup.find_all(class_=re.compile("ltx_para"))
    print 'parse para'

    ltx_paraset = sxpParseDivPara.ExtractParagraph(papersrc)
    #for each paragraph:
    current_sec = None
    for para in ltx_paraset:
        sxp_para = sxpPara()
        #here we find the whole text of a paragraph
        sxp_para.para_text = para[1]
        para_textset.append(para[1])
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
            current_sec = sxpsec
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
                    current_sec = sxpsec
                    break
                else:
                    uppersection = ParseUpperSection(uppersection)
            if len(uppersection) == 0:
                if current_sec is not None:
                    sxp_para.section_title = current_sec.title;
                    sxp_para.id_sec = current_sec.id
                else:
                    sxp_para.section_title = 'top';
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
        #for each paragraph, we extract its sentence
        sentenceset = sxpExtractText.MySentenceA(sxp_para.para_text)
        for sent in sentenceset:
            sxpsent = sxpSent()
            sxpsent.sentence_text = sent
            sxpsent.id = id_sent
            id_sent = id_sent + 1
            sxpsent.id_para = id_para
            sxpsent.id_sec = sxp_para.id_sec
            sxptxt.sentenceset.append(sxpsent)
            sentence_textset.append(sent)

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
    print 'building c_p matrix'
    sxptxt.c_p = csr_matrix((cs,ps), dtype=float64)
    print 'start'
    print sxptxt.c_p.shape
    for para in sxptxt.paraset:
        c = para.id_sec
        p = para.id
#        print c, p
        sxptxt.c_p[c, p] = 1.0


#        sxptxt.c_p[p, c] = 1.0
#third, building p-s matrixx
    print 'p_s matrix'
    sxptxt.p_s = csr_matrix((ps,ss), dtype=float64)
    for sent in sxptxt.sentenceset:
        p = sent.id_para
        s = sent.id
        sxptxt.p_s[p,s] = 1.0
#        sxptxt.p_s[p,s] = 1.0
#fourth, building s-k matrix
    print 's_k matrix'
    sxptxt.s_k =csr_matrix(sxptxt.sentence_tfidf.tfidf)

#fourth, building s-k matrix
    print 's_k matrix'
    sxptxt.s_k =csr_matrix(sxptxt.sentence_tfidf.tfidf)


#fifth, we will build k-k matrix which is the incident relationship of
    print 'k_k matrix'
    sxptxt.k_k =csr_matrix((ks,ks), dtype=float64)
    for sent in sxptxt.sentenceset:
        ws =sxpExtractText.ExtractEnglishWord(sent.sentence_text)
        kwpos= []
        if len(ws)>0:
           for w in ws:
              if w in sxptxt.sentence_tfidf.word:
                 kwpos.append(sxptxt.sentence_tfidf.word.index(w))
           n = len(kwpos)
           for i in range(n-1):
              sxptxt.k_k[kwpos[i],kwpos[i+1]] = 1
#return sxptxt
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
    #fn = 'P14-1008.xhtml'
    fname = paperpath + '\\' + fn
    sxptxt = ParseOnePaper(fname)
    fpname = paperpath + '\\pickle\\' + fn +  '.net_1.pickle'
    StoreSxptext(sxptxt, fpname)
    sxptxt = LoadSxptext(fpname)
##    sxpPPT.MakePPTFromTextA(sxptxt)


##    intro_id = FindIntroductionSection(sxptxt)
##    PrintAllPara(sxptxt)
##    PrintAllSentence(sxptxt)
##    PrintIntroductionSent(sxptxt,intro_id)
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
    fpname = paperpath + '\\pickle\\' + fn +  '_1.pickle'
    StoreSxptext(sxptxt, fpname)
    sxptxt = LoadSxptext(fpname)
    print sxptxt.d_c.shape
    print sxptxt.c_p.shape
    print sxptxt.p_s.shape
    print sxptxt.s_k.shape
def PrintAllSection(sxptxt):
    for sxpsec in sxptxt.section_list:
        print sxpsec.id, sxpsec.t_type, sxpsec.id_str, sxpsec.title
def PrintAllPara(sxptxt):
    for sxp_para in sxptxt.paraset:
        print sxp_para.id, sxp_para.id_sec, sxp_para.para_id,sxp_para.para_tuple,
        print sxp_para.section_title
        print sxp_para.para_text
def PrintAllSentence(sxptxt):
    sentenceset = sxptxt.sentenceset
    for sent in sentenceset:
##        if sent.id == 70:
##            print sent.sentence_text[0]==' ', sent.sentence_text[0].islower()
          print sent.id, sent.id_sec, sent.id_para, sent.sentence_text
def PrintIntroductionSent(sxptxt,intro_id):
    sentenceset = sxptxt.sentenceset
    for sent in sentenceset:
        if sent.id_sec == intro_id:
            print sent.id, sent.id_sec, sent.id_para, sent.sentence_text
def FindIntroductionSection(sxptxt):
    title_sect = 0
    abstract_sect = -1
    intro_sect = -1
    for sxpsec in sxptxt.section_list:
        print sxpsec.id, sxpsec.t_type, sxpsec.id_str, sxpsec.title
        idstr = sxpsec.id_str.lower()
        if idstr.find('abstract')>0:
            abstract_sect = sxpsec.id
        if idstr.find('instruction')>0:
            intro_sect = sxpsec.id
    if intro_sect == -1:
        if abstract_sect > -1:
            intro_sect = abstract_sect + 1
        else:
            abstract_sect = 1
            intro_sect = 2
    return intro_sect


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
        fset = fn.split('.')
        n = len(fset)
        if n <= 1:
            continue
        else:
            sf = fset[-1].lower()
            if sf == 'xhtml':
                SentenceParseOnePaper(fn)

def ListDir():
    flist = GetDirFileList(paperpath)
    print flist
def GetSXPTXTPicklName(fn):
    fpname = paperpath + '\\pickle\\' + fn +  '.net_1_1.pickle'
    return fpname
def MatchSentenceID(sentlabel_set):
    papernum = len(intro_sent)
    for i in range(papernum):
        paper = intro_sent[i]
        fn = paper[0]
        picklename = GetSXPTXTPicklName(fn)
        sxptxt = LoadSxptext(fpname)
        sentset = sxptxt.sentenceset
        labelnum = len(paper)
        j = 1
        while j < labelnum:
            labelsent = paper[i]
            labelid = FindSent(labelsent,sentset)
def FindSent(labelsent,sentset):
    ns = len(sentset)
    nl = []
    for i in ns:

        dist = MatchTwoSentence(labelsent,sentset[i])
        nl.append( dist)
def TestLoad():
    fn = 'P14-1007.xhtml'
    fname = paperpath + '\\pickle\\'  + fn +  '.net_1.pickle'
    sxptxt = LoadSxptext(fname)
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
    fn = 'P14-1014.xhtml'
    SentenceParseOnePaper(fn)
def TestParse():
    sectionid = 's1.sss1.p1'
    print ParseUpperSection(sectionid)
def main():
    #TestParsSection()
    #TestLoad()
    #TestFile()
    ProcessFilesInDir()
    #ListDir()
if __name__ == '__main__':
    main()
