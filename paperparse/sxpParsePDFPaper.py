#-------------------------------------------------------------------------------
# Name:        sxpParsePDFPaper
# Purpose:
#
# Author:      sunxp
#
# Created:     04/12/2015
# Copyright:   (c) sunxp 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------
# -*- coding=utf-8 -*-
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.layout import LAParams
from pdfminer.layout import LTTextBoxHorizontal
from pdfminer.converter import PDFPageAggregator

import numpy as np
from scipy.sparse import csr_matrix
from scipy import *

import re
import sxpLoadWeb
from sxpPackage import *
import sxpTextEncode
import sxpExtractText
import sxpContextMan
import sxpProcessParaText
import sxpFenciMakeTFIDF
import sxpReadFileMan
def Parse(fname):
    # Open a PDF file.
    fp = open(fname, 'rb')
    # Create a PDF parser object associated with the file object.
    parser = PDFParser(fp)
    # Create a PDF document object that stores the document structure.
    # Supply the password for initialization.
    password = ''
    document = PDFDocument(parser, password)
    # Check if the document allows text extraction. If not, abort.
    if not document.is_extractable:
        raise PDFTextExtractionNotAllowed
    # Create a PDF resource manager object that stores shared resources.
    rsrcmgr = PDFResourceManager()
    # Create a PDF device object.
    laparams = LAParams()
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    # Create a PDF interpreter object.
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    # Process each page contained in the document.
    i = 0
    para_list = []
    for page in PDFPage.create_pages(document):
        interpreter.process_page(page)
        # receive the LTPage object for the page.
        layout = device.get_result()
        for x in layout:
            if(isinstance(x, LTTextBoxHorizontal)):
                if(len(x.get_text()) > 1):
                    string_txt = x.get_text().replace('/n', ' ')
                    print string_txt
                    if (len(string_txt)>0):
                        print i, '-----'
                        i = i + 1
                        para_list.append(string_txt)
        print '/n/n/n/n'
    fp_pk = fname + '.pk'
    sxpPackage.StoreSxptext(para_list,fp_pk)
def ShowParse(fname):
    i = 0
    para_list = sxpPackage.LoadSxptext(fname)
    for eachp in para_list:
        txt = eachp.strip()
        if len(txt)>1:
            print i,'------'
            i = i + 1
            print txt

def ProcessParaTxt():
    fname = r'testdimension1.txt'
    papersrc = sxpLoadWeb.LoadFile(fname)
    patstr = r'\d+\s------'
    pat = re.compile(patstr)
    para_set = pat.split(papersrc)
    for eachpara in para_set:
        txtstr = eachpara.strip()
        txtword = txtstr.split(' ')
        if len(txtword)<=2:
            continue;
        else:
            print '------'
            print ReplaceDash(sxpTextEncode.GetUnicode(txtstr))

def is_relevant(sentences, s, t):
    max_dis = 0
    maintxt = ''
    for eachs in sentences:
        maintxt = maintxt + ' ' + eachs.sentence_text
    for eachs in sentences :
        sim = sxpContextMan.Similarity(eachs.sentence_text, s)
        if sim > max_dis:
            max_dis = sim
    if max_dis > t:
        return True
    return False
def is_relevantA(sentences, s, t):
    max_dis = 0
    maintxt = ''
    for eachs in sentences:
        maintxt = maintxt + ' ' + eachs.sentence_text
    max_dis = sxpContextMan.Similarity(maintxt, s)
    if max_dis > t:
        return True
    return False
def ProcessSectionPara(fname):
    sxptxt = sxpText()
    sxptxt.fname = fname

    papersrc = sxpLoadWeb.LoadFile(fname)
    patstr = r'------\n'
    pat = re.compile(patstr)
    para_set = pat.split(papersrc)
    sec_title_set = []
    sec_index_set = []
    cc= 1
    pp = 0
    for eachpara in para_set:
        txtstr = eachpara.strip()
        sect = DetectSection(txtstr)
        if sect:
            cc = cc + 1
        else:
            k = DetectKeyword(txtstr)
            if k is None:
               pp = pp + 1

    c_c = csr_matrix((cc+1,cc+1), dtype=float64)
    print c_c.shape
    c_c[0,1] = 1
    sec_root = 0
    sec_index = 0
    p_index = 0
    title = para_set[0]
    para_list = []
    sec_list =[[0,['0','0'],'doc',0]]
    keywords = []
    for eachpara in para_set:
        txtstr = eachpara.strip()
        if len(txtstr)==0:
            continue
        sect = DetectSection(txtstr)
        if sect:
            sec_index = sec_index + 1
            sec_id = sect[0]
            sec_title = sect[1]

            if len(sec_id[1]) >=  1:
                c_c[sec_root,sec_index] = 1.0
                print 'c_c:', sec_root,sec_index,sec_id,sec_title
                sec_list.append([sec_index,sec_id,sec_title,2])
            if len(sec_id[1]) == 0:
                c_c[0,sec_index] = 1.0
                sec_root = sec_index
                print 'c_c:', 0,sec_index,sec_id,sec_title
                sec_list.append([sec_index,sec_id,sec_title,1])
        else:
            k = DetectKeyword(txtstr)
            if k:
                keywords = k[0]
            else:
                print 'c_p:',sec_index,p_index
                para_list.append([sec_index,p_index,txtstr])
              #  c_p[sec_index,p_index] = 1.0
                p_index = p_index + 1
    i = 0
    section_list = []
    whole_section_title =''
    section_id_dict = {}
    for eachsec in sec_list:
        sxpsec = sxpSectionTitle()
        sxpsec.id = eachsec[0]
        sxpsec.id_str = eachsec[1][0] + '.' + eachsec[1][1]
        sxpsec.id_set = eachsec[1]
        sxpsec.title = eachsec[2]
        print sxpsec.id, sxpsec.id_str,sxpsec.title
        whole_section_title= whole_section_title + ' ' + sxpsec.title
        sxpsec.t_type = 'sec'
        sxpsec.level = eachsec[3]
        section_id_dict[sxpsec.id_str] = sxpsec.id
        section_list.append(sxpsec)
        i = i + 1
##    i = 0
##    for eachpara in para_list:
##        print i, eachpara
##        i = i + 1
    keyword_set = SplitKeywords(keywords)
    for eachk in keyword_set:
        print eachk
    para_textset = []
    sxp_para_set = []
    abstract_str = ''
    conclusion_str= ''
    i = 0
    for eachp in para_list:
        sec_id = eachp[0]
        sxpsec = section_list[sec_id]
        print sxpsec.title
        if ContainWord(sxpsec.title,'abstract'):
            abstract_str = abstract_str + ' ' + eachp[2]
            continue
        if ContainWord(sxpsec.title,'conclusion'):
            conclusion_str = conclusion_str + ' ' + eachp[2]
            continue
        para_id = eachp[1]
        para_txt = eachp[2]
        sxp_para = sxpPara()
        sxp_para.para_text = para_txt
        sxp_para.id = i
        sxp_para.id_sec = sec_id
        sxp_para.para_id = str(i)
        i = i + 1
        para_textset.append(sxp_para.para_text)
        sxp_para_set.append(sxp_para)
    pp = len(sxp_para_set)
    nc = len(section_list)
  #  c_p = csr_matrix((nc,pp), dtype=float64)
    id_sent= 0
    whole_text = ''
    sentence_textset= []
    context_id = 0
    for sxp_para in sxp_para_set:
       # c_p[sxp_para.id_sec,sxp_para.id] = 1.0
        sentenceset = sxpExtractText.MySentenceA(sxp_para.para_text)
        sxpsent_set = []
        id_para = sxp_para.id
        for sent in sentenceset:
            sxpsent = sxpSent()
            sxpsent.sentence_text = sent
            sxpsent.id = id_sent
            id_sent = id_sent + 1
            sxpsent.id_para = sxp_para.id
            sxpsent.id_sec = sxp_para.id_sec
            sxptxt.sentenceset.append(sxpsent)
            sentence_textset.append(sent)
            whole_text = whole_text +'' + sent
            sxpsent_set.append(sxpsent)
        context = []
        context_result = []
        i = 0
        for st in sxpsent_set:
            s = st.sentence_text
            if len(context) == 0:
                context.append(st)
            elif is_relevant(context, s, 0.06):
                context.append(st)
            else:
                para_context = sxpContext()
                para_context.id = context_id
                context_id = context_id + 1
                para_context.id_para = id_para
                para_context.id_sec = sxp_para.id_sec
                para_context.context_sent = context
                context_result.append(para_context)
                context = []
                context.append(st)
            i = i + 1
        if len(context)>0:
                para_context = sxpContext()
                para_context.id = context_id
                context_id = context_id + 1
                para_context.id_para = id_para
                para_context.id_sec = sxp_para.id_sec
                para_context.context_sent = context
                context_result.append(para_context)
                context = []

#for this para, we add the context result to the global storage
        sxp_para.context_set = context_result
        sxptxt.context_set.extend(context_result)
    sxptxt.keyword_set = keyword_set
    sxptxt.paraset = sxp_para_set

    sxptxt.section_id_dict = section_id_dict
    sxptxt.whole_sectitle = whole_section_title
    sxptxt.abstract = abstract_str
    sxptxt.conclusion = conclusion_str
    sxptxt.whole_text = whole_text
    sxptxt.section_list = section_list
    sxptxt.c_c = c_c
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
    ts = len(sxptxt.context_set)
    print cs, ps, ss, ks,ts
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

#now to build para_context matrix p_t
    print 'building p_t matrix and t_s matrix'
    sxptxt.p_t = csr_matrix((ps,ts), dtype=float64)
    sxptxt.t_s = csr_matrix((ts,ss), dtype=float64)
    print 'start'
    print sxptxt.p_t.shape
    print sxptxt.t_s.shape
    for para in sxptxt.paraset:
        p = para.id
        for cont in para.context_set:
            t = cont.id
            sxptxt.p_t[p, t] = 1.0
            for eachs in cont.context_sent:
                s = eachs.id
                sxptxt.t_s[t,s] = 1.0

#        print c, p

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
##
##
###fifth, we will build k-k matrix which is the incident relationship of
##    print 'k_k matrix'
##    sxptxt.k_k =csr_matrix((ks,ks), dtype=float64)
##    for sent in sxptxt.sentenceset:
##        ws =sxpExtractText.ExtractEnglishWord(sent.sentence_text)
##        kwpos= []
##        if len(ws)>0:
##           for w in ws:
##              if w in sxptxt.sentence_tfidf.word:
##                 kwpos.append(sxptxt.sentence_tfidf.word.index(w))
##           n = len(kwpos)
##           for i in range(n-1):
##              sxptxt.k_k[kwpos[i],kwpos[i+1]] = 1
#return sxptxt
    return sxptxt
def SplitKeywords(keystr):
    patstr = r'[\s|,]'
    pat = re.compile(patstr)
    r = pat.split(keystr)
    key_set = []
    for eachk in r:
        if len(eachk.strip())==0:
            continue
        else:
            key_set.append(eachk)
    return key_set
def DetectKeyword(txtstr):
    patstr = r'Keywords:(.+)'
    pat = re.compile(patstr)
    r = pat.match(txtstr)
    if r:
        return [r.group()]
    else:
        return None
def ContainWord(txtstr,wordstr):
    patstr = wordstr
    if txtstr.lower().find(wordstr)>=0:
        return True;
    else:
        return False
def DetectSection(txtstr):
    patstr = r'(\d\d?\.\d?)\s+(.+)'
    pat = re.compile(patstr)
    r = pat.match(txtstr)

    if r:
#        print r.group()
#        print r.groups()
        m = r.groups()
        idset = m[0].split('.')
        sec_title = m[1].strip().lower()
        return [idset, sec_title]
    else:
        return None
def TestParse():
  #  fname = 'testpdf.pdf'
    fname = 'Dimensionality on summarization.pdf'
    #Parse(fname)
    pname= fname + '.pk'
    ShowParse(pname)
def ReplaceDash(strtxt):
    patstr = r'(\w)-\n(\w)'
    pat = re.compile(patstr)
    ns = pat.sub(r'\1\2', strtxt)
    return ReplaceManySpace(ns)
def ReplaceManySpace(strtxt):
    patstr = r'\s{2,}'
    pat = re.compile(patstr)
    ns = pat.sub(r' ', strtxt)
    return ns
def TestSinglePaper():
    ContainWord('doc','abstract')
    fname = r'testdimension_2.txt'
    sxptxt = ProcessSectionPara(fname)
    pname = fname + '.pk'
    StoreSxptext(sxptxt,pname)
def MakeModelFromPk():
    modelpath = r'D:\pythonwork\code\paperparse\paper\single\model'
    pkpath = r'D:\pythonwork\code\paperparse\paper\single\pk'
    flist = sxpReadFileMan.GetDirFileList(pkpath)
    i = 1
    pyrouge = 1
    for fn in flist:
        fset = fn.split('.')
        n = len(fset)
        if n <= 1:
            continue
        else:
            sf = fset[-1].lower()
            if sf == 'pk':
                sxptxt =LoadSxptext(fn)
                i = i + 1
                absconf =modelpath  +'\\' + fn +'.C' + '.html'
                if pyrouge == 1:
                    absf = modelpath + '\\' + fn + '.A' + '.html'
                    conf =modelpath  +'\\' +  fn + '.B' + '.html'
                    abstract = MakeModel(sxptxt.abstract,fn + '.A' )
                    conclusion = MakeModel(sxptxt.conclusion,fn + '.B' )
                    sxpReadFileMan.WriteStrFile(absf,abstract, 'utf-8')
                    sxpReadFileMan.WriteStrFile(conf,conclusion, 'utf-8')
    #                sxpReadFileMan.WriteStrFile(absconf,sxptxt.abstract +  sxptxt.conclusion, 'utf-8')
                if pyrouge == 0:
                    absf = fset[0] + '_reference1'+ '.txt'
                    conf = fset[0] + '_reference2'+ '.txt'
                    abstract = MakeModel(sxptxt.abstract,absf, 0)
                    conclusion = MakeModel(sxptxt.conclusion,conf,0 )
                    sxpReadFileMan.WriteStrFile(modelpath  +'\\' +absf, abstract, 'utf-8')
                    sxpReadFileMan.WriteStrFile(modelpath  +'\\' +conf, conclusion, 'utf-8')
    #                sxpReadFileMan.WriteStrFile(absconf,sxptxt.abstract +  sxptxt.conclusion, 'utf-8')
def MakeModel(txt,fn, formatsent = 1):
        modeltxt  = '''
<html><head>
    <title>%s</title>
</head>
'''%(fn)
        sentenceset = re.split(r'\.',txt)
        i = 0
        abstract_str = ''
        for sent in sentenceset:
            rsent = RemoveUStrSpace(sent)
            if len(rsent)<=1:
                continue
            i = i + 1
            rsent = rsent + '.'
            if formatsent == 1:
                sentr ='''<a name="%d">[%d]</a> <a href="#%d" id=%d>%s</a>\n'''%(i,i,i,i,rsent)
                abstract_str = abstract_str +sentr
            if formatsent == 0:
                abstract_str = abstract_str +rsent + '\n'
        if formatsent == 1:
            bodytxt ='''
<body bgcolor="white">
%s
</body>
</html>
        '''%(abstract_str)
        if formatsent == 0:
            bodytxt = abstract_str
        if formatsent == 1:
            abstract_str = modeltxt + bodytxt
        if formatsent== 0:
            abstract_str = bodytxt

        return abstract_str

def RemoveUStr(strtxt):
    patstr = r"u'\\u\w\w\w\w'"
    pattern = re.compile(patstr)
    nstr = pattern.sub('',strtxt)
##    patstr = "\s"
##    pattern = re.compile(patstr)
##    nstr = pattern.sub(' ',nstr)
    return nstr
def RemoveUStrSpace(strtxt):
    patstr = r"u'\\u\w\w\w\w'"
    pattern = re.compile(patstr)
    nstr = pattern.sub('',strtxt)
    patstr = "\s+"
    pattern = re.compile(patstr)
    nstr = pattern.sub(' ',nstr)
    return nstr
def main():
    #TestSinglePaper()
    MakeModelFromPk()
if __name__ == '__main__':
    main()
