__author__ = 'a'
from sxpPackage import *
import networkx as nx
import numpy as np
from numpy import *


class GraphBased:
    def __init__(self, pickle_path,remove_stopwords=1):
        self.section2sentence_id_list = {}
        self.idx_s = []
        self.remove_stopwords = remove_stopwords
        self.text = LoadSxptext(pickle_path)
        self.page_rank(pickle_path)
        self.ordered_sentence_id_set()

    def page_rank(self, pickle_path):
        g = create_graph(pickle_path,self.remove_stopwords)
        pr = nx.pagerank(g)
       # self.idx_s = list(argsort(pr.values()))
        pr = array(pr.values())
        pr = pr.reshape((len(pr),1))
        self.idx_s = argsort(-pr, axis=0)
        print self.idx_s.shape
      #  self.idx_s.reverse()

    def ordered_sentence_id_set(self):
        #print len(self.idx_s)
        #print len(self.text.sentenceset)
        #print self.idx_s
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
    def OutputAllRankSentence(self,useabstr = 1,maxwords = -1):
        i = 0
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


# input : path, file_name
# output: matrix
def create_graph(pickle_path, remove_stopwords = 1):
    f = open('stopwords.txt', 'r')
    lines = f.readlines()
    f.close()
    if remove_stopwords == 1:
        stopwords = [line.strip() for line in lines]
    elif remove_stopwords == 0:
        stopwords = []

    text = LoadSxptext(pickle_path)
    sentences = text.sentenceset
    g = nx.Graph()
    for sent in sentences:
        g.add_node(sent.id)
    for i in range(len(sentences)):
        for j in range(i, len(sentences)):
##            sent_a = set(sentences[i].sentence_text.split())
##            sent_b = set(sentences[j].sentence_text.split())
            sent_a = set([w for w in sentences[i].sentence_text.split() if w not in stopwords])
            sent_b = set([w for w in sentences[j].sentence_text.split() if w not in stopwords])

            common_word = sent_a.intersection(sent_b)
            if not common_word:
                continue
            jaccard = len(common_word) / float(len(sent_a.union(sent_b)))
            g.add_edge(sentences[i].id, sentences[j].id, weight=jaccard)
            g.add_edge(sentences[j].id, sentences[i].id, weight=jaccard)
    return g

"""
def test_page_rank():
    path = r'C:\Users\a\PycharmProjects\extractInfo\papers'
    file_name = 'P14-1007.xhtml'
    pickle_path = path + '\\pickle\\' + file_name + '_1.pickle'
    page_rank(pickle_path)


def main():
    test_page_rank()

"""


def TestPickle():
    pk = r'E:\pythonworknew\code\paperparse\paper\papers\pickle\P14-1007.xhtml_2.pickle'
#    pk = r'D:\pythonwork\code\paperparse\paper\papers\pickle\P14-1011.xhtml_2.pickle'
    pk = r'D:\pythonworknew\code\paperparse\paper\single\pk\testdimension_3.pk'
    pk = r'E:\pythonworknew\code\paperparse\paper\single\pk\testdimension_3.pk'
    model= GraphBased(pk)
    topksent = 10
    useabstr = 0
    maxword = 100
    strictmax = 1
    tops = model.OutPutTopKSent(topksent,useabstr,maxword,strictmax)
    i = 0
    print len(tops)
    for eachs in tops:
        print '----------------'
        print i, eachs
        i = i + 1
if __name__ == '__main__':
    #TestNormalizeMatrixA()
    TestPickle()
  #  TestPageRankMatrix()