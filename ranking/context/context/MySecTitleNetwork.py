# -------------------------------------------------------------------------------
# Name:        MySecTitleNetwork
# Purpose:     In order to increase the weight of words in the section title
#
# Author:      sunxp
#
# Created:     12/06/2016
# Copyright:   (c) sunxp 2016
# Licence:     <your licence>
# -------------------------------------------------------------------------------

# -*- coding: UTF-8 -*-

### Notification:
### The difference between MySecTitleNetwork and MySecModel lies in:
###   The original thought that words in section title may be more important,
### so we add a weight vector tk and two belongingness matrix s_tk, w_tk and
### rewrite the word_weight_update function to increase weight of words in
### section title.
### 1. tk: (length of token list from main body)*1 vector, the word weight for words in section title
### 2. s_tk: (number of sentences)*(length of token list from main body) matrix, for each sentence set its section title words as 1, other words as 0
### 3. w_tk: (length of token list from main body)*(length of token list from main body) matrix = w_s * s_tk, only set words appearing in section title as 1
### 4. update_section_title_weight: update tk = normalize(s_tk.T * s)
### 5. update_word_weight:
###      w1 = word weight update as same as MySecModel
###      w2 = w_tk*tk
###      w = normalize(w1+w2)
### 6. word_count: a vector stores word count number for token list from main body

#######################################################################################
# ---------------------------------- Global variable -------------------------------- #
#######################################################################################
##import sys
##sys.path.append("..")
from sxpPackage import *
from scipy import *
import numpy as np
import os
import re
#######################################################################################
# ------------------------------------- Classes ------------------------------------- #
#######################################################################################
class MySecTitleModel:
    # choice: 1 means with stopwords; 2 means without stopwords
    def __init__(self, pickle_path, remove_stopwords=2, iteration_times=40):
        self.w_s = None
        self.s_p = None
        self.p_c = None
        self.c_c = None
        self.s_tk = None  # sentence_section-title-words matrix
        self.w_tk = None  # words_section-title-words matrix
        self.tk = []  # initial section title words weight vector
        self.w = []
        self.s = []
        self.p = []
        self.c = []
        self.idx_w = []
        self.idx_s = []
        self.idx_p = []
        self.idx_c = []
        self.times = iteration_times
        self.words = []
        self.word_count = []
        self.sec_title_word_set = []
        self.ranked_sentences = []
        self.text = LoadSxptext(pickle_path)
        self.section2sentence_id_list = {}
        if remove_stopwords == 0:
            self.get_parameters_with_stopwords()
        elif remove_stopwords == 1:
            self.get_parameters_without_stopwords()
        self.BuildTitleNetwork()  # build title network
        # self.word_count = self.Buildwordcount()  # add a new attribute named as "word_count" to sxpText object
        # self.NormalizeWS()
        w = matrix(random.rand(len(self.words))).T  # initial
        self.iteration(w)
        self.rank_weight()
        self.ordered_sentence_id_set()

    def get_parameters_with_stopwords(self):
        self.words = self.text.sentence_tfidf.word
        self.word_count = self.text.sentence_tfidf.ct.sum(axis=0).T
        self.w_s = matrix(self.text.s_k.toarray()).T
        self.s_p = matrix(self.text.p_s.toarray()).T
        self.p_c = matrix(self.text.c_p.toarray()).T
        self.c_c = matrix(self.text.c_c.toarray())

    def get_parameters_without_stopwords(self):
        # -- assign values to words, w_s, s_p, p_c
        self.get_parameters_with_stopwords()
        # -- get stopwords list
        f = open(os.path.join('stopwords.txt'), 'r')
        lines = f.readlines()
        f.close()
        stopwords = [line.strip() for line in lines]
        # -- strip stopwords out from self.words and self.w_s
        idx = [i for i in range(len(self.words)) if self.words[i] not in stopwords
               and re.match(r'^[a-zA-Z\-]+$', self.words[i]) is not None]
        new_w_s = []
        new_word_count = []
        for i in idx:
            new_w_s.append(array(self.w_s[i, :]).tolist())
            new_word_count.append(self.word_count[(i,0)])
        new_words = [self.words[i] for i in idx]
        new_w_s = matrix(array(new_w_s))
        new_word_count = matrix(array(new_word_count)).T
        self.words = new_words
        self.w_s = new_w_s
        self.word_count = new_word_count

    def BuildTitleNetwork(self):
        section_list = self.text.section_list
        self.sec_title_word_set = []
        for i, eachsec in enumerate(section_list):
##            print i, eachsec.title
            title_word_index = self.GetWordIndex(eachsec.title.lower())
##            print title_word_index
            self.sec_title_word_set.append(title_word_index)

        self.tk = matrix(random.rand(len(self.words))).T
        self.s_tk = matrix(np.zeros(self.w_s.T.shape, dtype=np.float))
##        print self.sec_title_word_set
        #note that since title words can be no where in the article, the matrix s_tk can be a zero
        #matrix, so, please be sure that normalization can handle zero vector
        #and Another thing is that we believe all sentences are related to the title or the zero
        #so we can add this relationship to the networks
        linktotitle = 1
        for sent in self.text.sentenceset:
##            print sent.id_sec
            wi = self.sec_title_word_set[sent.id_sec]
            self.s_tk[sent.id, wi] = 1
            if linktotitle==1:
                wi = self.sec_title_word_set[0]
                self.s_tk[sent.id, wi] = 1
##            print sent.id,wi
        self.w_tk = self.w_s*self.s_tk

    def GetWordIndex(self, sent):
        pat = '[\s|\:|,]'
        ws = re.split(pat, sent)
        ws = [w for w in ws if len(w) > 0]
        index_list = []
        for w in ws:
            if w in self.words:
                index_list.append(self.words.index(w))
            # else:
            #     index_list.append(-1)  # 这里不合理，为什么没有该词时要加-1? 导致BuildTitleNetwork建words list中最后一个与该section所有句子的链接
        return index_list

    # 这个函数不对, 直接从sentence split得到的word 和 self.words中的tokens是不同的，不如直接都用sentence_tfidf.ct相加得到， 这样tokens是一样的
    # def Buildwordcount(self):
    #     word_dict = {}  # record words and their appearance time in all sentences
    #     nwd = 0
    #     # print u'applications' in self.words
    #     for eachsent in self.text.sentenceset:
    #         wds = SplitSentence(eachsent.sentence_text.lower())
    #         for wd in wds:
    #             if wd not in self.words:   # ignore words that are not in token list
    #                 continue
    #             else:
    #                 if wd in word_dict:
    #                     word_dict[wd] += 1.0
    #                 else:
    #                     word_dict[wd] = 1.0
    #                     nwd += 1
    #
    #     word_count = matrix(np.zeros((len(self.words), 1), dtype=np.float))
    #     for i, wd in enumerate(self.words):
    #         if wd in word_dict:
    #             word_count[i, 0] = word_dict[wd]
    #     return word_count

    def rank_weight(self):
        self.idx_w = argsort(array(-self.w), axis=0)
        self.idx_s = argsort(array(-self.s), axis=0)
        self.idx_p = argsort(array(-self.p), axis=0)
        self.idx_c = argsort(array(-self.c), axis=0)

    def ordered_sentence_id_set(self):
        self.ranked_sentences = [self.text.sentenceset[self.idx_s[(i,0)]] for i in range(len(self.text.sentenceset))]
        sec_titles = []
        for sec in self.text.section_list:
            self.section2sentence_id_list[sec.title] = []
            sec_titles.append(sec.title)
        for sentence in self.ranked_sentences:
            section_tag = self.text.paraset[sentence.id_para].section_title
            if section_tag != '' and section_tag in sec_titles:
                self.section2sentence_id_list[section_tag].append(sentence.id)

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

    def update_section_weight(self, p):
        sec = self.c_c * self.p_c.T * p
        sec = self.normalize(sec)
        return sec

    def update_section_title_weight(self, s):
        tk = self.s_tk.T * s
        tk = self.normalize(tk)
        return tk

    def update_word_weight(self, w, s, p, c):
        w = self.w_s * s + self.w_s * self.s_p * p\
            + self.w_s * self.s_p * self.p_c * c
        # w = self.w_s * s + self.w_s * self.s_p * p  #this is the mostly used model
        w = self.normalize(w)
        return w

    def iteration(self, w):
        for i in range(self.times):
            s = self.update_sentence_weight(w)

            tk = self.update_section_title_weight(s)

            p = self.update_paragraph_weight(s)

            c = self.update_section_weight(p)

            w1 = self.update_word_weight(w, s, p, c)
            w2 = self.normalize(self.w_tk*tk)
            w = self.normalize(w1+w2)
        self.w = w
        self.s = s
        self.p = p
        self.c = c

    # this function do not involve the number of words in the paper
    # i.e. this function do not divide the all word count
    def NormalizeWS(self):
        # s_w = self.w_s.T / self.text.word_count.T
        t = np.sum(self.word_count)
        # s_w = self.w_s.T / t
        self.w_s = np.multiply(self.w_s, self.word_count)/t

    def OutputAllRankSentence(self,useabstr = 1,maxwords = -1):
        sent_txt_set = []
        for sentence in self.ranked_sentences:
            sent_txt_set.append(sentence.sentence_text)
        return sent_txt_set

    # ---- return top k sentence_text ----
    def OutPutTopKSent(self, topk, useabstr = 1, maxwords = -1,strictmax=0):
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

    def OutPutTopKSentWeight(self, topk, useabstr = 1, maxwords = -1):
        ranked_weight = [self.s[self.idx_s[(i, 0)]]
                         for i in range(len(self.s))]
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
        for sentence in self.ranked_sentences:
            if len(sentence.sentence_text)<=1:
                 continue
            if usetopk:
                if i>=topk:
                    break
            else:
                if wordlen >= maxwords:
                    break
            wl = len(sentence.sentence_text.split(' '))
            wordlen = wordlen + wl#len(sentence.sentence_text)
            sent_txt_set.append([sentence.sentence_text, ranked_weight[i], self.idx_s[(i, 0)]])
            wordlen += len(sentence.sentence_text)
            i += 1
        return sent_txt_set

    def OutPutTopKWord(self, topk):
        ranked_word = [self.words[self.idx_w[i, 0]] for i in range(len(self.words))]
        word_set = []
        for i, eachword in enumerate(ranked_word):
            if i >= topk:
                break
            word_set.append(eachword)
            print eachword
        return word_set

#######################################################################################
# -------------------------------- Some tool functions ------------------------------ #
#######################################################################################
def SplitSentence(sent_txt):
    pat = r'[\s,\(\)\[\]\:\?\"\'\/]'
    s = re.split(pat, sent_txt)
    return s

#######################################################################################
# -------------------------------- Some test functions ------------------------------ #
#######################################################################################
def TestPickle():
    pk = r'D:\pythonwork\code\paperparse\paper\papers\pickle\P14-2045.xhtml_3.pickle'
    model = MySecTitleModel(pk)
    topksent = 10
    useabs = 0
    maxwords = -1
    tops = model.OutPutTopKSentWeight(topksent, useabs, maxwords)
    for i, eachs in enumerate(tops):
        print '----------------'
        print i, eachs

    # model.OutPutTopKWord(20)
    # sent_id = 79
    # s_w = model.w_s.T[sent_id, :]
    # print s_w[s_w > 0.0]
    # print model.text.sentenceset[sent_id].sentence_text
    #
    # sent_id = 57
    # s_w = model.w_s.T[sent_id, :]
    # print s_w[s_w > 0.0]
    #
    sections = model.text.section_list
    for sec in sections:
        print sec.title.lower()
        for idx in model.sec_title_word_set[sec.id]:
            print model.words[idx],

def TestText():
    pk = r'D:\pythonwork\code\paperparse\paper\papers\pickle\P14-2138.xhtml_2.pickle'
    text = LoadSxptext(pk)
    for i, eachsent in enumerate(text.sentenceset):
        print i, eachsent.sentence_text
    print text.sentence_tfidf.word
    print text.sentence_tfidf.tfidf[79, :]

#######################################################################################
# --------------------------------- Main function  ---------------------------------- #
#######################################################################################
if __name__ == '__main__':
    cmdstr = 'testrank'
    if cmdstr == 'testrank':
        TestPickle()
    if cmdstr == 'testtext':
        TestText()

