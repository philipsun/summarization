#-------------------------------------------------------------------------------
# Name:        sxpParseXHMLPaper
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

class sxpText:
    fname = ''
    title = ''
    abstract = ''
    relatedwork = ''
    conclusion = ''
    reference = ''
    section_title_set =[]
    paraset = []
    whole_sectitle = ''
    whole_text = ''
    sxpprocess = None
class sxpSectionTitle:
    title = ''
    id_str = ''
    id_set = ''
    level = 0
class sxpPara:
    para_id = ''
    para_text = ''
    para_tuple = []
    para_tfidf =[]
    section_title=''

paperpath = r'D:\pythonwork\code\paperparse\paper\papers'
def FindStr(pattern,strsrc):
    p = re.compile(pattern)
    return p.match(strsrc)
def ParseOnePaper(fname):

    papersrc = sxpLoadWeb.LoadFile(fname)
   # print papersrc
    soup = BeautifulSoup(papersrc,from_encoding = 'utf-8')
   # titleitem = soup.findAll(attr={"class":"ltx_title ltx_title_document"})
    titleitem = soup.find_all(class_=re.compile("ltx_title"))
    sxptxt = sxpText()
    sxptxt.fname = fname;
    sectionset = []
    sectiontitle ={}
    whole_section_title =''
    section_title_set = []
    whole_text = ''
    for t in titleitem:
        sxpsec = sxpSectionTitle()
        tp = t.parent
        if tp.has_attr('id'):
            sid = tp['id'].lower()
        else:
            sid = 'top'
        cls = t['class']
        sxpsec.id_str = sid;
        sxpsec.id_set = ParseParaID(sid)
        sxpsec.title = t.text
        sxpsec.level = len(sxpsec.id_set)
        whole_section_title = whole_section_title + '\n' + t.text
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
        section_title_set.append(sxpsec)
##    for s in sectionset:
##        print s.parent_id, s.text

    sxptxt.section_title_set = section_title_set
    sxptxt.whole_sectitle = whole_section_title
#**************************************************************
    print 'begin to find all ltx_para'
    soup = BeautifulSoup(papersrc,from_encoding = 'utf-8')
    paraset = []
    ltx_paraset = soup.find_all(class_=re.compile("ltx_para"))
    #for each paragraph:
    for para in ltx_paraset:
        sxp_para = sxpPara()
        #here we find the whole text of a paragraph
        sxp_para.para_text = para.text
        whole_text = whole_text + '\n' + para.text
        if para.has_attr('id'):
##            print para['id'], para.text;
            pid = para['id'].lower()
            sxp_para.para_id = pid
            #here we find the section id of the paragraph
            sxp_para.para_tuple = ParseSectionIDStr(pid)
        else:
            if para.has_attr('class'):
                if isinstance(para['class'], list):
                    sxp_para.para_id = ' '.join(para['class']).lower()
                else:
                    sxp_para.para_id = para['class'].lower()
                sxp_para.para_tuple = [sxp_para.para_id,'']
        #here we find the section title of the para_graph
        #if we use dict to store section title, we will be more efficient here
        for sxpsec in section_title_set:
            if sxp_para.para_tuple is None:
                print sxp_para
            if sxp_para.para_tuple[0]== sxpsec.id_str:
                sxp_para.section_title = sxpsec.title;
                break;
            else:
                sxp_para.section_title = '';

        paraset.append(sxp_para)
    sxptxt.paraset = paraset
    sxptxt.whole_text = whole_text
#**************************************************************
#****************Now we try to extract the key counter of whole_text
    sxptxt.sxpprocess = sxpProcessParaText.ParseTextPara(whole_text)
    return sxptxt
#**************************************************************
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

def TestParseOnePaper():
    fname = paperpath + '\\' + 'P14-1010.xhtml'
    sxptxt = ParseOnePaper(fname)
##    sxpPPT.MakePPTFromTextA(sxptxt)
##    for sxpsec in sxptxt.section_title_set:
##        print sxpsec.t_type, sxpsec.id_str, sxpsec.title
##    for sxp_para in sxptxt.paraset:
##        print sxp_para.para_id,sxp_para.para_tuple,
##        print sxp_para.section_title
##        print sxp_para.para_text
    sentenceset = sxptxt.sxpprocess.sentenceset
    for ss in sentenceset:
        print ss.keylist

##    para_id = ''
##    para_text = ''
##    para_tuple = []
##    para_tfidf =[]
##    section_title=''
#    print sxptxt.whole_text
#    print sxptxt.title
#    print sxptxt.abstract
##    for sct in sxptxt.sectionset:
##        print sct
##    for para in sxptxt.paraset:
##        print para.para_id, para.para_tuple, para.para_text

def main():
    TestParseOnePaper()

if __name__ == '__main__':
    main()
