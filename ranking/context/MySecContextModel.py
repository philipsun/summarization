#-------------------------------------------------------------------------------
# Name:        sxpContextModel
# Purpose:
#
# Author:      sunxp
#
# Created:     26/10/2015
# Copyright:   (c) sunxp 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------
__author__ = 'sunxp'
from numpy import *
from sxpPackage import *
import re


class SecConTextModel:
    #1 means with stopwords
    #2 means without stopwords
    def __init__(self, pickle_path, remove_stopwords=1, iteration_times=20):
        self.w_s = None
        self.s_p = None
        self.p_c = None
        self.t_p = None
        self.s_t = None
        self.c_c = None
        self.w = []
        self.s = []
        self.p = []
        self.c = []
        self.t = [] #context
        self.idx_w = []
        self.idx_s = []
        self.idx_p = []
        self.idx_c = []
        self.idx_t = [] #sorted context
        self.times = iteration_times
        self.words = []
        self.text = LoadSxptext(pickle_path)
        self.section2sentence_id_list = {}
        if remove_stopwords == 0:
            self.get_parameters_with_stopwords()
        elif remove_stopwords == 1:
            self.get_parameters_without_stopwords()
        w = matrix(random.rand(len(self.words))).T
        self.iteration(w)
        self.rank_weight()
        self.ordered_sentence_id_set()
    def OutputAllRankSentence(self,useabstr = 1,maxwords = -1):
        ranked_sentences = [self.text.sentenceset[self.idx_s[i, 0]]
                            for i in range(len(self.text.sentenceset))]
        sent_txt_set = []
        i = 0
        for sentence in ranked_sentences:
            sent_txt_set.append(sentence.sentence_text)
            i = i + 1
        return sent_txt_set

    def OutPutTopKSent(self, topk,useabstr = 1,maxwords = -1,strictmax = 0):
        ranked_sentences = [self.text.sentenceset[self.idx_s[i, 0]]
                            for i in range(len(self.text.sentenceset))]
        sent_txt_set = []
        i = 0
        if useabstr == 0:
            if maxwords==-1:
                usetopk = True;
            else:
                usetopk = False
        if useabstr == 1:
            abstractlen = len(self.text.abstract.split(' '))
            maxwords = abstractlen
            usetopk = False

        if useabstr == 2:
            abstractlen = len(self.text.conclusion.split(' '))
            maxwords = abstractlen
            usetopk = False
        wordlen = 0
        print 'use topk', usetopk, 'maxword',maxwords
        for sentence in ranked_sentences:
            if len(sentence.sentence_text)<=1:
                 continue
            words = sentence.sentence_text.split(' ')
            wl = len(words)
            if usetopk:
                if i>=topk:
                    break
            else:
                if strictmax == 1:
                    if wordlen + wl > maxwords:
                        seglen = wordlen+wl -maxwords
                        if seglen<=0:
                            break
                        else:
                            wl = seglen
                            segsent = words[0:wl]
                            usesent = ' '.join(segsent)
                            sent_txt_set.append(usesent)
                            wordlen = wordlen + wl
                            break
                else:
                    if wordlen >= maxwords:
                        break
            wordlen = wordlen + wl#len(sentence.sentence_text)
            sent_txt_set.append(sentence.sentence_text)
            i = i + 1
        return sent_txt_set
    def ordered_sentence_id_set(self):
        ranked_sentences = [self.text.sentenceset[self.idx_s[i, 0]]
                            for i in range(len(self.text.sentenceset))]
        sec_titles = []
        for sec in self.text.section_list:
            self.section2sentence_id_list[sec.title] = []
            sec_titles.append(sec.title)
        for sentence in ranked_sentences:
            section_tag = self.text.paraset[sentence.id_para].section_title
            #section_id = text.paraset[sentence.id_para].id_sec
            if section_tag != '' and section_tag in sec_titles:
                self.section2sentence_id_list[section_tag].append(sentence.id)

    def rank_weight(self):
        self.idx_w = argsort(array(-self.w), axis=0)
        self.idx_s = argsort(array(-self.s), axis=0)
        self.idx_p = argsort(array(-self.p), axis=0)
        self.idx_c = argsort(array(-self.c), axis=0)
        self.idx_t = argsort(array(-self.t), axis=0)

    def get_parameters_with_stopwords(self):
        self.words = self.text.sentence_tfidf.word
        # import relation matrix
        self.w_s = matrix(self.text.s_k.toarray()).T
        #self.w_s = matrix(self.text.sentence_tfidf.ct.toarray()).T #for version one
        self.s_p = matrix(self.text.p_s.toarray()).T
        self.p_c = matrix(self.text.c_p.toarray()).T
        self.t_p = matrix(self.text.p_t.toarray()).T
        self.s_t = matrix(self.text.t_s.toarray()).T
        self.c_c = matrix(self.text.c_c.toarray())
    def get_parameters_without_stopwords(self):
        self.get_parameters_with_stopwords()
        f = open('stopwords.txt', 'r')
        lines = f.readlines()
        f.close()
        stopwords = [line.strip() for line in lines]
        idx = [i for i in range(len(self.words)) if self.words[i] not in stopwords
               and re.match(r'^[a-zA-Z]+$', self.words[i]) is not None]
        new_w_s = []
        for i in idx:
            new_w_s.append(array(self.w_s[i, :]).tolist())
        new_w_s = matrix(array(new_w_s))
        new_words = [self.words[i] for i in idx]
        self.words = new_words
        self.w_s = new_w_s

    @staticmethod
    def normalize(w):
        assert(sum(w) > 0)
        w = w / sum(w)
        return w

    def update_sentence_weight(self, w):
        s = self.w_s.T * w
        s = self.normalize(s)
        return s

    def update_paragraph_weight(self, s):
        p = self.s_p.T * s
        p = self.normalize(p)
        return p
    def update_context_weigth(self, s):
        t = self.s_t.T * s
        t = self.normalize(t)
        return t

    def update_paragraph_weight_bycontext(self, t):
        p = self.t_p.T * t
        p = self.normalize(p)
        return p

    def update_section_weight(self, p):
        sec = self.c_c * self.p_c.T * p
        sec = self.normalize(sec)
        return sec

    def update_word_weight(self, w, s, p, sec):
        #w = self.w_s * s + self.w_s * self.s_p * p\
           # + self.w_s * self.s_p * self.p_c * sec
        #w = self.w_s * self.s_p * self.p_c * sec
        #w = self.w_s * s
        w = self.w_s * s + self.w_s * self.s_p * p
        w = self.normalize(w)
        return w
    def update_word_weight_bycontext(self, w, s, t,p,sec):
        w = self.w_s * s + self.w_s*self.s_t*t + self.w_s * self.s_t * self.t_p * p\
             + self.w_s * self.s_t * self.t_p* self.p_c * sec

        w = self.normalize(w)
        return w


    def iteration(self, w):
        for i in range(self.times):
            s = self.update_sentence_weight(w)

            t = self.update_context_weigth(s)

            p = self.update_paragraph_weight_bycontext(t)

            c = self.update_section_weight(p)

            w = self.update_word_weight_bycontext(w, s, t, p,c)

        self.w = w
        self.s = s
        self.p = p
        self.c = c
        self.t = t


def TestPickle():
    pk = r'D:\pythonwork\code\paperparse\paper\papers\pickle\P14-1007.xhtml_2.pickle'
#    pk = r'D:\pythonwork\code\paperparse\paper\papers\pickle\P14-1011.xhtml_2.pickle'
    pk = r'D:\pythonwork\code\paperparse\paper\single\pk\testdimension_3.pk'
    model= SecConTextModel(pk)
    topksent = 10
    tops = model.OutPutTopKSent(topksent,1,-1)
    i = 0
    for eachs in tops:
        print '----------------'
        print i, eachs
        i = i + 1
if __name__ == '__main__':
    #TestNormalizeMatrixA()
    TestPickle()
  #  TestPageRankMatrix()
