#-------------------------------------------------------------------------------
# Name:        MyTFIDF
# Purpose:
#
# Author:      sunxp
#
# Created:     12/06/2016
# Copyright:   (c) sunxp 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------
from numpy import *
from sxpPackage import *
import re
import numpy as np
from numpy import *

class MyTFIDF:
    #1 means with stopwords
    #2 means without stopwords
    def __init__(self, pickle_path, choice=2, iteration_times=40):
        self.w_s = None
        self.s_p = None
        self.p_c = None
        self.c_c = None
        self.s_tk = None
        self.w_tk = None
        self.tk = []
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
        self.text = LoadSxptext(pickle_path)
        self.section2sentence_id_list = {}
        if choice == 1:
            self.get_parameters_with_stopwords()
        elif choice == 2:
            self.get_parameters_without_stopwords()
        #build title network**********
        self.BuildSentenceScore()
        self.rank_weight()
        self.ordered_sentence_id_set()
    def BuildTitleNetwork(self):
        section_list=self.text.section_list
##        print len(section_list)
##        print  self.c_c.shape
##        print self.w_s.shape
        i=0
        sec_title_word_set=[]
        for eachsec in section_list:
            print i, eachsec.title
            title_word_index = self.GetWordIndex(eachsec.title.lower())
            sec_title_word_set.append(title_word_index)
            i = i +1

        self.tk = matrix(random.rand(len(self.words))).T
        self.s_tk =  matrix(np.zeros(self.w_s.T.shape, dtype=np.float))
##        print 'self.tk.shape', self.tk.shape
##        print 'self.s_tk.shape', self.s_tk.shape
        for sent in self.text.sentenceset:
            wi = sec_title_word_set[sent.id_sec]
            self.s_tk[sent.id,wi] = 1
        self.w_tk = self.w_s*self.s_tk
      #  sw_tfidf = self.text.sentence_tfidf
##        print len(self.words)
     #   print self.words
    def GetWordIndex(self,sent):
        pat = '[\s|\:|,]'
        ws = re.split(pat,sent)
        index_list =[]
        for w in ws:
            if w in self.words:
                index_list.append(self.words.index(w))
            else:
                index_list.append(-1)
        return index_list
    def NormalizeWS(self):
        #print self.text.word_count
        #this function do not divid the all word count
#            s_w = self.w_s.T / self.text.word_count.T
        t = np.sum(self.text.word_count.T)
        #this function do not invovle the number of words in the paper
#            s_w = self.w_s.T / t
        s_w = np.multiply(self.w_s.T,self.text.word_count.T)/t
        self.w_s = s_w.T

    def OutputAllRankSentence(self,useabstr = 1,maxwords = -1):
        ranked_sentences = [self.text.sentenceset[self.idx_s[i, 0]]
                            for i in range(len(self.text.sentenceset))]
        sent_txt_set = []
        i = 0
        for sentence in ranked_sentences:
            sent_txt_set.append(sentence.sentence_text)
            i = i + 1
        return sent_txt_set

    def OutPutTopKSent(self, topk,useabstr = 1,maxwords = -1,strictmax=0):
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
    def OutPutTopKSentWeight(self, topk,useabstr = 1,maxwords = -1):
        ranked_sentences = [self.text.sentenceset[self.idx_s[i, 0]]
                            for i in range(len(self.text.sentenceset))]
        ranked_weight =  [self.s[self.idx_s[i, 0]]
                            for i in range(len(self.s))]
        sent_txt_set = []
        i = 0
        if useabstr == 1:
            abstractlen = len(self.text.abstract)
        if useabstr == 2:
            abstractlen = len(self.text.conclusion)
        wordlen = 0
        for sentence in ranked_sentences:

            if  wordlen>= abstractlen and maxwords == -1:
                break
            if len(sentence.sentence_text)<=1:
                continue
            if i >= topk  and maxwords == 0:
                break;
            wordlen = wordlen + len(sentence.sentence_text)
            sent_txt_set.append([sentence.sentence_text, ranked_weight[i],self.idx_s[i, 0]])
            i = i + 1
        return sent_txt_set
    def OutPutTopKWord(self, topk):
        ranked_word = [self.words[self.idx_w[i, 0]]
                            for i in range(len(self.words))]
        word_set = []
        i = 0
        for eachword in ranked_word:
            word_set.append(eachword)
            print eachword
        return word_set
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

    def get_parameters_with_stopwords(self):
        self.words = self.text.sentence_tfidf.word
        # import relation matrix
        self.w_s = matrix(self.text.s_k.toarray()).T
      #  self.w_s = matrix(self.text.sentence_tfidf.ct.toarray()).T #for version one
        self.s_p = matrix(self.text.p_s.toarray()).T
        self.p_c = matrix(self.text.c_p.toarray()).T
        self.c_c =matrix(self.text.c_c.toarray())

    def get_parameters_without_stopwords(self):
        self.get_parameters_with_stopwords()
        f = open('stopwords1.txt', 'r')
        lines = f.readlines()
        f.close()
        stopwords = [line.strip() for line in lines]
        idx = [i for i in range(len(self.words)) if self.words[i] not in stopwords
               and re.match(r'^[a-zA-Z\-]+$', self.words[i]) is not None]
        new_w_s = []
        for i in idx:
            new_w_s.append(array(self.w_s[i, :]).tolist())
        new_w_s = matrix(array(new_w_s))
        new_words = [self.words[i] for i in idx]
        self.words = new_words
        self.w_s = new_w_s
    def BuildSentenceScore(self):
        s = np.average(self.w_s,0).T
        p = self.s_p.T * s
        p = self.normalize(p)
        c = self.update_section_weight(p)
        c = self.normalize(c)

        w = self.w_s * s + self.w_s * self.s_p * p\
            + self.w_s * self.s_p * self.p_c * c
        w = self.normalize(w)

        self.w = w
        self.s = s
        self.p = p
        self.c = c

    def Buildwordcount(self):
        word_dict ={}
        nwd = 0
        print u'applications' in self.words
        for eachsent in self.text.sentenceset:
            wds = SplitSentence(eachsent.sentence_text.lower())
            for wd in wds:
                if wd not in self.words:
                    continue
                else:
                    if wd in word_dict:
                        word_dict[wd] +=1.0
                    else:
                        word_dict[wd] = 1.0
                        nwd = nwd + 1

        word_count=matrix(np.zeros((len(self.words),1),dtype=np.float))
        i = 0
        for wd in self.words:
            if wd in word_dict:
                word_count[i,0]=word_dict[wd]
            i = i + 1
        return word_count
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

    def update_word_weight(self, w, s, p, c):
        w = self.w_s * s + self.w_s * self.s_p * p\
            + self.w_s * self.s_p * self.p_c * c
        #w = self.w_s * self.s_p * self.p_c * c
        #w = self.w_s * s
       # w = self.w_s * s + self.w_s * self.s_p * p #this is the mostly used model
        w = self.normalize(w)
        return w

    def iteration(self, w):
        for i in range(self.times):
            s = self.update_sentence_weight(w)
#            print(s[59])
            tk = self.normalize(self.s_tk.T*s)

            p = self.update_paragraph_weight(s)

            c = self.update_section_weight(p)

            w1 = self.w_s * s + self.w_s * self.s_p * p\
                + self.w_s * self.s_p * self.p_c * c
            #w = self.w_s * self.s_p * self.p_c * c
            #w = self.w_s * s
           # w = self.w_s * s + self.w_s * self.s_p * p #this is the mostly used model
            w1 = self.normalize(w1)
            w2 = self.normalize(self.w_tk*tk)
            w = self.normalize(w1+w2)
        self.w = w
        self.s = s
        self.p = p
        self.c = c
def SplitSentence(sent_txt):
    pat =r'[\s,\(\)\[\]\:\?\"\'\/]'
    s =re.split(pat,sent_txt)
    return s
def TestPickle():
    pk = r'D:\pythonwork\code\paperparse\paper\papers\pickle\P14-1007.xhtml_2.pickle'
#    pk = r'D:\pythonwork\code\paperparse\paper\papers\pickle\P14-1011.xhtml_2.pickle'
    pk = r'D:\pythonwork\code\paperparse\paper\single\pk\testdimension_3.pk'
    pk = r'D:\pythonwork\code\paperparse\paper\papers\pickle\P14-2063.xhtml_2.pickle'
    model= MyTFIDF(pk)
    topksent = 10
    tops = model.OutPutTopKSentWeight(topksent,1,-1)
    i = 0
    for eachs in tops:
        print '----------------'
        print i, eachs
        i = i + 1
#    model.OutPutTopKWord(topksent)
    print model.words
    sent_id = 79
    s_w = model.w_s.T[sent_id,:]
    print s_w[s_w>0.0]
    print model.text.sentenceset[sent_id].sentence_text

    sent_id = 57
    s_w = model.w_s.T[sent_id,:]
    print s_w[s_w>0.0]

def TestText():
    fn = 'P14-2063.xhtml'
#    text=SentenceParseOnePaper(fn)
    pkdir = 'D:\pythonwork\code\paperparse\paper\papers\pickle'
    pkf = pkdir + '\\'+fn+'_2.pickle'
    text = LoadSxptext(pkf)
    i = 0
    for eachsent in text.sentenceset:
        print i, eachsent.sentence_text
        i = i + 1
    print text.sentence_tfidf.word
    print text.sentence_tfidf.tfidf[79,:]

if __name__ == '__main__':
    #TestNormalizeMatrixA()
    cmdstr ='testrank'
    if cmdstr=='testrank':
        TestPickle()
    if cmdstr == 'testtext':
        TestText()
  #  TestPageRankMatrix()

