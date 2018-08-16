__author__ = 'a'
import networkx as nk
from sxpPackage import *
from numpy import *
import re

class WordGraph:
    def __init__(self, pickle_path,remove_stopwords=0):
        self.section2sentence_id_list = {}
        self.idx_s = []
        self.idx_w = []
        self.words = []
        self.w = []
        self.remove_stopwords = remove_stopwords
        self.text = LoadSxptext(pickle_path)
        self.page_rank(pickle_path)
        #
        self.ordered_sentence_id_set()

    def page_rank(self, pickle_path):
        g = create_graph(pickle_path,self.remove_stopwords)
        pr = nk.pagerank(g)
        for elem in pr.items():
            #print elem
            self.words.append(elem[0])
            self.w.append(elem[1])
        #print self.words
        #print self.w
        sentence_weight = []
        for sent in self.text.sentenceset:
            words = sent.sentence_text.split()
            weight = 0
            for word in words:
                word = word.lower()
                if word not in pr.keys():
                    continue
                weight += pr[word]
            sentence_weight.append(weight)
    #    self.idx_s = argsort(-array(sentence_weight)).tolist()
        pr = array(sentence_weight)
        pr = pr.reshape((len(pr),1))
        self.idx_s = argsort(-pr, axis=0)
        print self.idx_s.shape

        self.idx_w = argsort(-array(self.w)).tolist()

    def ordered_sentence_id_set(self):
        #print len(self.idx_s)
        #print len(self.text.sentenceset)
        #print self.idx_s
        ranked_sentences = [self.text.sentenceset[self.idx_s[i,0]]
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
        ranked_sentences = [self.text.sentenceset[self.idx_s[i,0]]
                            for i in range(len(self.text.sentenceset))]
        sent_txt_set = []
        i = 0
        for sentence in ranked_sentences:
            sent_txt_set.append(sentence.sentence_text)
            i = i + 1
        return sent_txt_set

    def OutPutTopKSent(self, topk,useabstr = 1,maxwords = -1,strictmax=0):
        ranked_sentences = [self.text.sentenceset[self.idx_s[i,0]]
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


def create_graph(pickle_path, remove_stopwords=2, window=3):
    text = LoadSxptext(pickle_path)
    sentences = text.sentenceset
    g = nk.Graph()
    f = open('stopwords.txt', 'r')
    lines = f.readlines()
    f.close()
    if remove_stopwords==1:
        stopwords = [line.strip() for line in lines]
    elif remove_stopwords == 0:
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


def main():
    path = r'C:\Users\a\PycharmProjects\extractInfo\papers'
    file_name = 'P14-1007.xhtml'
    pickle_path = path + '\\pickle\\' + file_name + '_1.pickle'
    test_word_graph(pickle_path)


if __name__ == '__main__':
    main()
