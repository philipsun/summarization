#coding: utf-8


import numpy as np
from numpy import *
import pickle
import sxpFenciMakeTFIDF
import sxpProcessParaText
#Version one is a very raw idea
# In this model, I did not consider the influence of neighborhood
# This model is strictly based on the tree structure of the document

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
        self.section_id_dict ={} #section_id_dict['abstract'] = 2
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

        def normalize(w):
            assert(sum(w) > 0)
            w = w / sum(w)
            return w


def update_sentence_weight(w_s, w):
    s = w_s.T * w
    s = normalize(s)
    return s


def update_paragraph_weight(s_p, s):
    p = s_p.T * s
    p = normalize(p)
    return p


def update_section_weight(p_c, p):
    sec =p_c.T * p
    sec = normalize(sec)
    return sec


def update_word_weight(w, w_s, s, s_p, p,p_c, sec):
    w = w_s * s + w_s * s_p * p + w_s * s_p *p_c * sec
    w = normalize(w)
    return w


def iteration(w, w_s, s_p, p_c, times):
    for i in range(times):
        s = update_sentence_weight(w_s, w)

        p = update_paragraph_weight(s_p, s)

        sec = update_section_weight(p_c, p)

        w = update_word_weight(w, w_s, s, s_p, p,p_c, sec)

    return w, s, p, sec

paperpath = r'C:\Users\a\PycharmProjects\extractInfo\papers'
def LoadSxptext(fname):
    f = open(fname,'rb')
    sxptxt = pickle.load(f)
    f.close()
    return sxptxt
def TestsxpLoadPickle():
    fn = 'P14-1007.xhtml'
    fname = paperpath + '\\' + fn
    fpname = paperpath + '\\pickle\\' + fn +  '.pickle'
    sxptxt = LoadSxptext(fpname)
    print sxptxt.section_id_dict
    for sxpsec in sxptxt.section_list:
        print sxpsec.id, sxpsec.t_type, sxpsec.id_str, sxpsec.title
    for sxp_para in sxptxt.paraset:
        print sxp_para.id, sxp_para.id_sec, sxp_para.para_id,sxp_para.para_tuple,
        print sxp_para.section_title
        print sxp_para.para_text

    sentenceset = sxptxt.sentenceset
    for sent in sentenceset:
        print sent.id, sent.id_para, sent.sentence_text
    tfid = sxptxt.sentence_tfidf
    print tfid.tfidf[1,1]
    print sxptxt.d_c.shape
    print sxptxt.c_p.shape
    print sxptxt.p_s.shape
    print sxptxt.s_k.shape
    print len(sxptxt.sentence_tfidf.word)
    print sxptxt.sentence_tfidf.word

#*************Now begin to rank word, sent, para, and sect
    w_s = matrix(sxptxt.s_k.toarray()).T
    s_p = matrix(sxptxt.p_s.toarray()).T
    p_c = matrix(sxptxt.c_p.toarray()).T
    w = matrix(np.random.rand(len(sxptxt.sentence_tfidf.word))).T
    print w_s.shape
    print s_p.shape
    print p_c.shape
    print w.shape
    #w_s = np.mat('1,0,0,0,1;1,1,0,1,0;0,1,1,0,1;1,0,1,1,0')
    #s_p = np.mat('1,0;1,0;0,1;0,1;0,1')
    #p_c = np.mat('1;1')
    w, s, p, c = iteration(w, w_s, s_p, p_c, 20)
    idx_w = argsort(array(-w), axis=0)
    new_w = w[idx_w]
    #print type(idx_w)
    #words = sxptxt.sentence_tfidf.word[idx_w]
    print [sxptxt.sentence_tfidf.word[idx_w[i, 0]] for i in range(100)]
    #print type(sxptxt.sentence_tfidf.word)
    idx_s = argsort(array(-s), axis=0)
    new_s = [sentenceset[i] for i in idx_s[:, 0].tolist()]
    i = 1
    for t in new_s[1:50]:
        print i, sxptxt.paraset[t.id_para].section_title, sxptxt.paraset[t.id_para].id_sec, t.sentence_text
        i = i + 1
    idx_c = argsort(array(-c),axis=0)
    sections = [sxptxt.section_list[i] for i in idx_c[:,0].tolist()]
    for sxpsec in sections:
        print sxpsec.id, sxpsec.t_type, sxpsec.id_str, sxpsec.title
    #print 'word weight distribution is ', w
    #print 'sentence weight distribution is ', s
    #print 'paragraph weight distribution is ', p
    #print 'section weight is ', c


def TestSimple():
    w = np.mat('0;0;0.5;0.5')
    w_s = np.mat('1,0,0,0,1;1,1,0,1,0;0,1,1,0,1;1,0,1,1,0')
    s_p = np.mat('1,0;1,0;0,1;0,1;0,1')
    p_c = np.mat('1;1')
    w, s, p, c = iteration(w, w_s, s_p, p_c, 10)
    idx_w = argsort(array(-w), axis=0)
    new_w = w[idx_w]
    print new_w
    print 'word weight distribution is ', w
    print 'sentence weight distribution is ', s
    print 'paragraph weight distribution is ', p
    print 'section weight is ', c

def main():
    #TestSimple()
    TestsxpLoadPickle()
pass


if __name__ == '__main__':
    main()


