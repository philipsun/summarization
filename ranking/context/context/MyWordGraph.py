__author__ = 'sxp'
import networkx as nk
from sxpPackage import *
import numpy as np
from numpy import *
import re
import sxpReadFileMan
class MyWordGraph:
    def __init__(self, pickle_path,remove_stopwords=1):
        self.section2sentence_id_list = {}
        self.idx_s = []
        self.idx_w = []
        self.words = []
        self.w = []
        self.sent_len =[]
        self.pr=[]
        self.ranked_sentences = []
        self.sentence_weight=[]
        self.remove_stopwords = remove_stopwords
        print pickle_path
        self.text = LoadSxptext(pickle_path)
        self.page_rank(pickle_path)
        self.ComputRank()
       #    self.ComputHybridRank()
        #
        self.ordered_sentence_id_set()

    def page_rank(self, pickle_path):
        g = create_graph(pickle_path,self.remove_stopwords)
        self.pr = nk.pagerank(g)
        for elem in self.pr.items():
#            print elem
            self.words.append(elem[0])
            self.w.append(elem[1])
    def ComputeSentWeight(self,word_wegith_set):
        md = 'sum'
        wt = array(word_wegith_set)
        if md =='sum':
            return np.sum(wt)
        if md == 'max':
            if len(word_wegith_set)==0:
                return 0
            else:
                return np.max(wt)
        if md == 'maxavg':
            if len(word_wegith_set)==0:
                return 0
            else:
                av = np.mean(wt)
                mx = np.max(wt)
                sd = np.std(wt)
                #return av*mx/sd #this function is not so ok
                return av*mx #this function used in ComputRank is interesting.

    def ComputRank(self):
        #print self.words
        #print self.w
        self.sentence_weight = []
        for sent in self.text.sentenceset:
            words = sent.sentence_text.split()
            weight = 0
            weight_set = []
            for word in words:
                word = word.lower()
                if word not in self.pr.keys():
                    continue
                weight += self.pr[word]
                weight_set.append(self.pr[word])
            self.sentence_weight.append(self.ComputeSentWeight(weight_set))
        self.idx_s = argsort(-array(self.sentence_weight)).reshape((len(self.sentence_weight),1))
        self.idx_w = argsort(-array(self.w)).tolist()
        sorted_word = [[self.words[self.idx_w[i]],self.w[self.idx_w[i]]]
                            for i in range(len(self.words))]
##        for word in sorted_word:
##            print word
##        for key, value in sorted(self.pr.items(), key=lambda (k,v): (v,k), reverse = True):
##            print "%s: %s" % (key, value)

    def ComputHybridRank(self):
        #print self.words
        #print self.w
        self.sentence_weight = []
        self.sentence_len =[]
        i = 0
        for sent in self.text.sentenceset:
            words = sent.sentence_text.split()
            weight_set = []
            for word in words:
                word = word.lower()
                if word not in self.pr.keys():
                    continue
                weight_set.append(self.pr[word])
            if len(weight_set)==0:
                weight = 0
            else:
                weight = self.ComputeSentWeight(weight_set)#max(weight_set)
            self.sentence_len.append(len(words))
            self.sentence_weight.append(weight)
            i = i + 1
        maxlen = max(self.sentence_len)*1.0
        self.sentence_len = array(self.sentence_len) / maxlen
        ws=array(self.sentence_weight)
        ws=normalize(ws)
        ls=normalize(self.sentence_len)
        self.sentence_weight = ws*ls#in this way, the longer sentence will have a larger weight, and will be randerd higher rank in extraction
   #     self.sentence_weight = ws*(1-ls) #the shorter sentence will have a larger weight

        self.idx_s = argsort(-array(self.sentence_weight)).reshape((len(self.sentence_weight),1))
        self.idx_w = argsort(-array(self.w)).tolist()
        sorted_word = [[self.words[self.idx_w[i]],self.w[self.idx_w[i]]]
                            for i in range(len(self.words))]
##        for word in sorted_word:
##            print word
##        for key, value in sorted(self.pr.items(), key=lambda (k,v): (v,k), reverse = True):
##            print "%s: %s" % (key, value)

    def ordered_sentence_id_set(self):
        #print len(self.idx_s)
        #print len(self.text.sentenceset)
        #print self.idx_s
        self.ranked_sentences = [self.text.sentenceset[self.idx_s[i,0]]
                            for i in range(len(self.text.sentenceset))]
        sec_titles = []
        for sec in self.text.section_list:
            self.section2sentence_id_list[sec.title] = []
            sec_titles.append(sec.title)
        for sentence in self.ranked_sentences :
            section_tag = self.text.paraset[sentence.id_para].section_title
            #section_id = text.paraset[sentence.id_para].id_sec
            if section_tag != '' and section_tag in sec_titles:
                self.section2sentence_id_list[section_tag].append(sentence.id)
    def ComputeSentenceLen(self):
        self.sent_len = []
        for eachsent in self.ranked_sentences:
            self.sent_len.append(len(eachsent.sentence_text))
        return self.sent_len
    def OutputAllRankSentence(self,useabstr = 1,maxwords = -1):
        self.ranked_sentences = [self.text.sentenceset[self.idx_s[i,0]]
                            for i in range(len(self.text.sentenceset))]
        sent_txt_set = []
        i = 0
        for sentence in self.ranked_sentences:
            sent_txt_set.append(sentence.sentence_text)
            i = i + 1
        return sent_txt_set

    def OutPutTopKSent(self, topk,useabstr = 1,maxwords = -1,strictmax=0):
##        self.ranked_sentences = [self.text.sentenceset[self.idx_s[i]]
##                            for i in range(len(self.text.sentenceset))]

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
        for sentence in self.ranked_sentences:
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
        ranked_sentences = [self.text.sentenceset[self.idx_s[i,0]]
                            for i in range(len(self.text.sentenceset))]
        ranked_sentences_weight =  [self.sentence_weight[self.idx_s[i,0]]
                            for i in range(len(self.text.sentenceset))]
        sent_txt_set = []
        i = 0
        if useabstr == 0:
            if maxwords <=0:
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
        print 'useabst', useabstr,'use topk', usetopk, 'maxword',maxwords
        for sentence in ranked_sentences:
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
            sent_txt_set.append(sentence.sentence_text)
            i = i + 1
        return sent_txt_set,ranked_sentences_weight[:i]

def normalize(v):
    norm=np.linalg.norm(v)
    if norm==0:
       return v
    return v/norm
def create_graph(pickle_path, remove_stopwords=1, window=3):
    text = LoadSxptext(pickle_path)
    sentences = text.sentenceset
    g = nk.Graph()
    f = open('stopwords.txt', 'r')
    lines = f.readlines()
    f.close()

    if remove_stopwords == 1:
        stopwords = [line.strip() for line in lines]
    elif remove_stopwords ==0:
        stopwords = []
    for sent in sentences:
        words = sent.sentence_text.split()
        for i in range(len(words)):
            if words[i].lower() in stopwords or re.match(r'^[a-zA-Z]+$', words[i]) is None:
                continue
            for j in range(i + 1, i + window):
                if j < 0 or j >= len(words):
                    continue
                if words[j].lower() in stopwords or re.match(r'^[a-zA-Z]+$', words[j]) is None:
                    continue
                g.add_edge(words[i].lower(), words[j].lower())
    return g

def test_word_graph(pickle_path):
    wg = WordGraph(pickle_path)
    print wg.idx_s
def BuildWordGraph(sxptxt):
    print sxptxt.sentence_tfidf.word

def Testread():
    path = r'D:\pythonwork\code\paperparse\paper\papers\pickle'
    file_name = 'P14-1007.xhtml'
    pickle_path = path + '\\' + file_name + '_2.pickle'
    sxptxt = sxpReadFileMan.LoadSxptext(pickle_path)
    BuildWordGraph(sxptxt)

def TestPickle():
    pk = r'D:\pythonwork\code\paperparse\paper\papers\pickle\P14-1011.xhtml_2.pickle'
    pk = r'D:\pythonwork\code\paperparse\paper\papers\pickle\P14-2063.xhtml_2.pickle'
    pk = r'D:\pythonwork\code\paperparse\paper\single\pk\testdimension_4.pk'
    pk = r'D:\pythonwork\code\paperparse\paper\papers\pickle\P14-2008.xhtml_2.pickle'
    pk = r'D:\pythonwork\code\paperparse\paper\papers\pickle\P14-1007.xhtml_2.pickle'
#    pk = r'D:\pythonwork\code\paperparse\paper\papers\duc\txt\pickle\AP880512-0157'
    model= MyWordGraph(pk)
    topksent = 5
    useabstr= 0
    maxword = 0
    tops,weights = model.OutPutTopKSentWeight(topksent,useabstr,maxword)
    print len(tops)
    i = 0
    for eachs in tops:
        print '-----------------'
        print i, weights[i],eachs
        i = i + 1
def main():
    TestPickle()
if __name__ == '__main__':
    #TestNormalizeMatrixA()
    main()

