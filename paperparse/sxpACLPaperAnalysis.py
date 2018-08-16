#-------------------------------------------------------------------------------
# Name:        sxpPaperAnalysisA4
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
import sxpReadFileMan
import sxpContextMan
from sxpPackage import *
import sxpParseSectionNetwork

paperpath = r'.\paper\papers'
pickle_dir= paperpath + '\\' + 'pickle'
txt_dir = paperpath + '\\' + 'txt'
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
def SegSent(s):
    patstr = u',|\.|\:|\?|，|。|：|？|！|；'
    pattern = re.compile(patstr)
    ss = pattern.split(s)
    return ss
def SearchSentProcess(patstr, s, pat_name,pi):
    sent_list = SegSent(s)
    sent_pos_list = []
    i = 0;
    for eachs in sent_list:
        sent_pos = SearchProcess(patstr, eachs,'n', pat_name,pi)
        for eachsubpos in sent_pos:
            eachsubpos.extend([i])
            sent_pos_list.append(eachsubpos)
        i  = i + 1
    return sent_pos_list
def SearchProcess(patstr, s, sent='y', pat_name='',pi=0):
    if sent == 'y':
        return SearchSentProcess(patstr,s, pat_name,pi)
    pattern = re.compile(patstr)
    match =pattern.search(s)
    pattern_pos = []
    while match:
        tg = match.groups()
        tgtxt = match.group()
        posd = match.span()
        match = pattern.search(s,posd[1])
        pattern_pos.append([tgtxt,posd,tg,pat_name,pi,0])
    return pattern_pos
def IsAbstractConclusion(strtitle):
    patstr = u'abstract|conclusion'
    findpos = SearchProcess(patstr, strtitle.lower())
    if len(findpos)>0:
        return 1
    else:
        return 0
def IsConclusion(strtitle):
    patstr = u'conclusion'
    findpos = SearchProcess(patstr, strtitle.lower())
    if len(findpos)>0:
        return 1
    else:
        return 0
def IsAbstract(strtitle):
    patstr = u'abstract'
    findpos = SearchProcess(patstr, strtitle.lower())
    if len(findpos)>0:
        return 1
    else:
        return 0
def TestIsAbstractConclusion():
    s = 'Abbstract'
    print IsAbstractConclusion(s)
    s = 'Conclusions'
    print IsAbstractConclusion(s)
def ParseOnePaper(fname,include_absconc = True):
    print 'load file:', fname
    papersrc = sxpLoadWeb.LoadFile(fname)
    papersrc = sxpJudgeCharacter.ReplaceNonEnglishCharacter(papersrc)
#    papersrc = repr(papersrc.decode('utf-8','ignore').encode('utf-8'))
#    papersrc = papersrc.replace(r'\n',' ')
   # print papersrc
##    soup = BeautifulSoup(papersrc,from_encoding = 'utf-8')
##   # titleitem = soup.findAll(attr={"class":"ltx_title ltx_title_document"})
##    titleitem = soup.find_all("ltx_title ltx_title_section")
    shortfname = fname.split('\\')[-1]
    sxptxt = sxpText()
    sxptxt.fname = fname;
    abstract_str = ''
    conclusion_str = ''
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
    unknown_sec_id = 0
    if section_id_dict.has_key('unknown') == False:
        sxpdoc = sxpSectionTitle()
        sxpdoc.id = sec_id
        sxpdoc.title = 'unknown'
        sxpdoc.id_str = 'unknown'
        sxpdoc.level = 0
        sxpdoc.t_type = 'unknown'
        section_id_dict['unknown']=sec_id
        unknown_sec_id = sec_id
        section_list.append(sxpdoc)
        sec_id = sec_id + 1

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
    add_sec_title_to_para  = 0
    if add_sec_title_to_para == 1:
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
            sxpsent.id_sec = sec.id
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
    context_id = 0
    abstract_str = ''
    conclusion_str = ''
    for para in ltx_paraset:
        sxp_para = sxpPara()
        #here we find the whole text of a paragraph
        sxp_para.para_text = para[1]
        pid = para[0].lower()
        sxp_para.para_id = pid
        #here we find the section id of the paragraph
        sxp_para.para_tuple = ParseSectionIDStr(pid)
        #here we find the section title of the para_graph
        #if we use dict to store section title, we will be more efficient here
        if section_id_dict.has_key(sxp_para.para_tuple[0]):
            sxpsec_id = section_id_dict[sxp_para.para_tuple[0]]
          #  print sxpsec_id
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
                    sxp_para.section_title = 'unknown';
                    sxp_para.id_sec = unknown_sec_id

##        for sxpsec in section_id_dict:
##            if sxp_para.para_tuple is None:
##                print sxp_para
##            if sxp_para.para_tuple[0]== sxpsec.id_str:
##                sxp_para.section_title = sxpsec.title;
##                break;
##            else:
##                sxp_para.section_title = '';

        if IsAbstract(sxp_para.section_title) == 1:
            sentenceset = sxpExtractText.MySentenceA(sxp_para.para_text)
            for sent in sentenceset:
                rsent = RemoveUStrSpace(sent) + '.'
                abstract_str = abstract_str +rsent + '**.\n'
            if include_absconc == False:
                continue

        if IsConclusion(sxp_para.section_title) == 1:
            sentenceset = sxpExtractText.MySentenceA(sxp_para.para_text)
            for sent in sentenceset:
                rsent = RemoveUStrSpace(sent) + '.'
                conclusion_str = conclusion_str +rsent + '**.\n'
            if include_absconc == False:
                continue

        #for each paragraph, we extract its sentence
        sentenceset = sxpExtractText.MySentenceA(sxp_para.para_text)
        sxpsent_set = []
        for sent in sentenceset:
            sxpsent = sxpSent()
            sxpsent.sentence_text = sent
            sxpsent.id = id_sent
            id_sent = id_sent + 1
            sxpsent.id_para = id_para
            sxpsent.id_sec = sxp_para.id_sec
            sxptxt.sentenceset.append(sxpsent)
            sentence_textset.append(sent)
            sxpsent_set.append(sxpsent)
#*******for each paragraph, we parse a context set from it by iterating its sentences

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

#********for each paragraph, we add them to global storate variables
        para_textset.append(para[1])
        whole_text = whole_text + '\n' + para[1]
        sxp_para.id = id_para
        id_para = id_para + 1
        sxptxt.paraset.append(sxp_para)
    sxptxt.abstract = abstract_str
    sxptxt.conclusion = conclusion_str
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
    include_absconc = False;
    sxptxt = ParseOnePaper(fname,include_absconc)
    #3_.pickle is for inclusiong of abstract and conclusion
    #2_.pickle is for exclusion of abstract and conclusion
    if include_absconc == False:
        fpname = paperpath + '\\pickle\\' + fn +  '_3.pickle'
    if include_absconc == True:
        fpname = paperpath + '\\pickle\\' + fn +  '_2.pickle'
    sxptxt.c_c = sxpParseSectionNetwork.ParseSectionNetwork(sxptxt)
    StoreSxptext(sxptxt, fpname)
    sxptxt = LoadSxptext(fpname)
##    sxpPPT.MakePPTFromTextA(sxptxt)


##    intro_id = FindIntroductionSection(sxptxt)
##    PrintAllPara(sxptxt)
##    PrintAllSentence(sxptxt)
##    PrintIntroductionSent(sxptxt,intro_id)
    tfid = sxptxt.sentence_tfidf
    print sxptxt.d_c.shape
    print sxptxt.c_p.shape
    print sxptxt.p_s.shape
    print sxptxt.s_k.shape
    print sxptxt.p_t.shape
    print sxptxt.t_s.shape
    return sxptxt
##    print sxptxt.abstract
##    print sxptxt.conclusion
##def SentenceParseOnePaperFile(fn):
##    #fn = 'P14-1007.xhtml'
##    print 'process', fn
##    fname = paperpath + '\\' + fn
##    sxptxt = ParseOnePaper(fname)
##    fpname = paperpath + '\\pickle\\' + fn +  '_2.pickle'
##    StoreSxptext(sxptxt, fpname)
##    sxptxt = LoadSxptext(fpname)
##    print sxptxt.d_c.shape
##    print sxptxt.c_p.shape
##    print sxptxt.p_s.shape
##    print sxptxt.s_k.shape
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
def ProcessFileModelFromPickl():
    paperpath = r'.\paper\papers'
    modelpath = r'.\paper\papers\model_html'
    flist = GetDirFileList(paperpath)
    i = 1
    pyrouge = 1
    for fn in flist:
        fset = fn.split('.')
        n = len(fset)
        if n <= 1:
            continue
        else:
            sf = fset[-1].lower()
            if sf == 'xhtml':
                fname = paperpath + '\\' + fn
                fpname = paperpath + '\\pickle\\' + fn +  '_2.pickle'
                print i, fn
                sxptxt = LoadSxptext(fpname)
                i = i + 1
                absconf =modelpath  +'\\' + fn +'.C' + '.html'
                if pyrouge == 1:
                    absf = modelpath + '\\' + fn + '.A' + '.html'
                    conf =modelpath  +'\\' +  fn + '.B' + '.html'
                    abstract = MakeModel(sxptxt.abstract,fn + '.A')
                    conclusion = MakeModel(sxptxt.conclusion,fn + '.B')
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

def ProcessFilesModel():
    modelpath = r'.\paper\papers\model_html'
    flist = GetDirFileList(paperpath)
    i = 1
    pyrouge = 1
    for fn in flist:
        fset = fn.split('.')
        n = len(fset)
        if n <= 1:
            continue
        else:
            sf = fset[-1].lower()
            if sf == 'xhtml':
                sxptxt = SentenceParseOnePaper(fn)
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
        modeltxt  = '<html>\n<head>\n<title>%s</title>\n</head>\n'%(fn)
        sentenceset = re.split(r'\*\*\.',txt)
        i = 0
        abstract_str = ''
        for sent in sentenceset:
            rsent = RemoveUStrSpace(sent)
            if len(rsent)<=1:
                continue
            i = i + 1
            if formatsent == 1:
                sentr ='''<a name="%d">[%d]</a> <a href="#%d" id=%d>%s.</a>\n'''%(i,i,i,i,rsent)
                abstract_str = abstract_str +sentr
            if formatsent == 0:
                abstract_str = abstract_str +rsent + '\n'
        if formatsent == 1:
            bodytxt ='<body bgcolor="white">\n%s</body>\n</html>'%(abstract_str)
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

def TestRemoveUStr():
    strtxt = r'''
Dependency-based Compositional Semantics (DCS) is a framework of natural language semantics with easy-to-process structures as well as strict semantics.
In this paper, we equip the DCS framework with logical inference, by defining abstract denotations as an abstraction of the computing process of denotations in original DCS.
An inference engine is built to achieve inference on abstract denotations.
Furthermore, we propose a way to generate on-the-fly knowledge in logical inference, by combining our framework with the idea of tree transformation.
Experiments on FraCaS and PASCAL RTE datasets show promising results.
Abstract denotations are formulas constructed from a minimal set of relational algebra [] operators, which is already able to formulate the database queries defined by DCS trees.
For example, the semantics of u'\u201c' students read books u'\u201d' is given by the abstract denotation.
where read , student and book denote sets represented by these words respectively, and w r represents the set w considered as the domain of the semantic role r (e.g., u'\ud835' u'\udc1b' u'\ud835' u'\udc28' u'\ud835' u'\udc28' u'\ud835' u'\udc24' u'\ud835' u'\ude7e' u'\ud835' u'\ude71' u'\ud835' u'\ude79' is the set of books considered as objects.
The operators u'\u2229' and × represent intersection and Cartesian product respectively, both borrowed from relational algebra.
It is not hard to see the abstract denotation denotes the intersection of the u'\u201c' reading u'\u201d' set (as illustrated by the u'\u201c' read u'\u201d' table in Table 1 ) with the product of u'\u201c' student u'\u201d' set and u'\u201c' book u'\u201d' set, which results in the same denotation as computed by the DCS tree in Figure 1 , i.e., { John reads Ulysses , u'\u2026' }.
However, the point is that F 1 itself is an algebraic formula that does not depend on any concrete databases.
Formally, we introduce the following constants.
W a universal set containing all entities.
Content words a content word (e.g., read ) defines a set representing the word (e.g., u'\ud835' u'\udc2b' u'\ud835' u'\udc1e' u'\ud835' u'\udc1a' u'\ud835' u'\udc1d' = { ( x , y u'\u2005' r u'\u2062' e u'\u2062' a u'\u2062' d u'\u2062' ( x , y ) }.
In addition we introduce following functions.
× the Cartesian product of two sets.
u'\u2229' the intersection of two sets.
u'\u03a0' r projection onto domain of semantic role r (e.g., u'\u03a0' u'\ud835' u'\ude7e' u'\ud835' u'\ude71' u'\ud835' u'\ude79' u'\u2062' ( u'\ud835' u'\udc2b' u'\ud835' u'\udc1e' u'\ud835' u'\udc1a' u'\ud835' u'\udc1d' ) = { y u'\u2005' u'\u2203' x ; r u'\u2062' e u'\u2062' a u'\u2062' d u'\u2062' ( x , y ) }.
Generally we admit projections onto multiple semantics roles, denoted by u'\u03a0' R where R is a set of semantic roles.
u'\u0399' r relabeling (e.g., u'\u0399' u'\ud835' u'\ude7e' u'\ud835' u'\ude71' u'\ud835' u'\ude79' u'\u2062' ( u'\ud835' u'\udc1b' u'\ud835' u'\udc28' u'\ud835' u'\udc28' u'\ud835' u'\udc24' ) = u'\ud835' u'\udc1b' u'\ud835' u'\udc28' u'\ud835' u'\udc28' u'\ud835' u'\udc24' u'\ud835' u'\ude7e' u'\ud835' u'\ude71' u'\ud835' u'\ude79'.
q u'\u2282' r the division operator, where q u'\u2282' r u'\u2062' ( A , B ) is defined as the largest set X which satisfies B r × X u'\u2282' A.
2 2 If A and B has the same dimension, q u'\u2282' u'\u2062' ( A , B ) is either u'\u2205' or { * } ( 0 -dimension point set), depending on if A u'\u2282' B.
This is used to formulate universal quantifiers, such as u'\u201c' Mary loves every dog u'\u201d' and u'\u201c' books read by all students u'\u201d'.
An abstract denotation is then defined as finite applications of functions on either constants or other abstract denotations.
We have presented a method of deriving abstract denotation from DCS trees, which enables logical inference on DCS, and we developed a textual inference system based on the framework.
Experimental results have shown the power of the representation that allows both strict inference as on FraCaS data and robust reasoning as on RTE data.
Exploration of an appropriate meaning representation for querying and reasoning on knowledge bases has a long history.
Description logic, being less expressive than FOL but featuring more efficient reasoning, is used as a theory base for Semantic Web [].
Ideas similar to our framework, including the use of sets in a representation that benefits efficient reasoning, are also found in description logic and knowledge representation community [].
To our knowledge, however, their applications to logical inference beyond the use for database querying have not been much explored in the context of NLP.
The pursue of a logic more suitable for natural language inference is not new.
For instance, has implemented a model of natural logic [].
While being computationally efficient, various inference patterns are out of the scope of their system.
Much work has been done in mapping natural language into database queries [].
Among these, the ( u'\u039b' -)DCS [] framework defines algorithms that transparently map a labeled tree to a database querying procedure.
Essentially, this is because DCS trees restrict the querying process to a very limited subset of possible operations.
Our main contribution, the abstract denotation of DCS trees, can thus be considered as an attempt to characterize a fragment of FOL that is suited for both natural language inference and transparent syntax-semantics mapping, through the choice of operations and relations on sets.
We have demonstrated the utility of logical inference on DCS through the RTE task.
A wide variety of strategies tackling the RTE task have been investigated [] , including the comparison of surface strings [] , syntactic and semantic structures [] , semantic vectors [] and logical representations [].
Acquisition of basic knowledge for RTE is also a huge stream of research [].
These previous works include various techniques for acquiring and incorporating different kinds of linguistic and world knowledge, and further fight against the knowledge bottleneck problem, e.g., by back-off to shallower representations.
Logic-based RTE systems employ various approaches to bridge knowledge gaps proposes features from a model builder; proposes an abduction process; shows handcrafted rules could drastically improve the performance of a logic-based RTE system.
As such, our current RTE system is at a proof-of-concept stage, in that many of the above techniques are yet to be implemented.
Nonetheless, we would like to emphasize that it already shows performance competitive to state-of-the-art systems on one data set (RTE5.
Other directions of our future work include further exploitation of the new semantic representation.
For example, since abstract denotations are readily suited for data querying, they can be used to verify newly generated assumptions by fact search in a database.
This may open a way towards a hybrid approach to RTE wherein logical inference is intermingled with large scale database querying.
This research was supported by the Todai Robot Project at National Institute of Informatics.
    '''
    print RemoveUStrSpace(strtxt)
def StorePaperAbsCon():
    flist = GetDirFileList(paperpath)
    i = 0
    for fn in flist:
        fset = fn.split('.')
        n = len(fset)
        if n <= 1:
            continue
        else:
            sf = fset[-1].lower()
            if sf == 'xhtml':
                pickle_path = pickle_dir + '\\' +fn + '_1.pickle'
                sxptext = LoadSxptext(pickle_path)
                absf = txt_dir + '\\' + fn + '.t%s.abs.txt'%(str(i))
                conf =txt_dir + '\\' + fn + '.t%s.conf.txt'%(str(i))
                sxpReadFileMan.WriteStrFile(absf,sxptext.abstract, 'utf-8')
                sxpReadFileMan.WriteStrFile(conf,sxptext.conclusion, 'utf-8')
                i = i + 1
                print i, absf, conf

def ListDir():
    flist = GetDirFileList(paperpath)
    print flist
def GetSXPTXTPicklName(fn):
    fpname = paperpath + '\\pickle\\' + fn +  '_1.pickle'
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
    fn = 'P14-1019.xhtml'
    fname = paperpath + '\\pickle\\'  + fn +  '_1.pickle'
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
def TestPrintAllSentence():
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

def TestFile():
    fn = 'P14-2063.xhtml'
#    text=SentenceParseOnePaper(fn)
    pkdir = '.\paper\papers\pickle'
    pkf = pkdir + '\\'+fn+'_2.pickle'
    text = LoadSxptext(pkf)
    i = 0
    for eachsent in text.sentenceset:
        print i, eachsent.sentence_text
        i = i + 1
    print text.sentence_tfidf.word
    print text.sentence_tfidf.tfidf[59,:]
def TestParse():
    sectionid = 's1.sss1.p1'
    print ParseUpperSection(sectionid)

def main():
    #TestParsSection()
    #TestLoad()
    #TestIsAbstractConclusion()
   #  TestFile()
   cmdstr = 'parsesingle'
   if cmdstr =='parsesingle':
        TestFile()
   if cmdstr=='processdir':
        ProcessFilesInDir() #This is to produce pickle containing graphs of paper
   # ProcessFilesModel()
   if cmdstr=='makemodel':
        ProcessFileModelFromPickl() #this is to make model file for paper's
   # TestRemoveUStr()
   #  StorePaperAbsCon()
   # TestPrintAllSentence()
    #ListDir()
if __name__ == '__main__':
    main()
