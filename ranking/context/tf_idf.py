__author__ = 'a'
from sxpPackage import *
from numpy import *
import re


class TfIdf:
    def __init__(self, pickle_path,remove_stopwords=1):
        self.section2sentence_id_list = {}
        self.text = LoadSxptext(pickle_path)
        self.words = self.text.sentence_tfidf.word
        self.count_words = []
        self.idx_s = []
        self.remove_stopwords = remove_stopwords
        self.get_sentence_weight()
        self.rank_sentences()
        self.section_to_sentences()

    def section_to_sentences(self):
        ranked_sentences = []
        for elem in self.idx_s:
            ranked_sentences.append(self.text.sentenceset[elem])
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
    def rank_sentences(self):
        # get rid of the stopwords
        f = open('stopwords.txt', 'r')
        lines = f.readlines()
        f.close()
        if self.remove_stopwords == 1:
            stopwords = [line.strip() for line in lines]
        elif self.remove_stopwords == 0:
            stopwords = []
        # get the non-stopwords indexes
        idx = [i for i in range(len(self.words)) if self.words[i] not in stopwords
                      and re.match(r'^[a-zA-Z]+$', self.words[i]) is not None]
        sentences2words = []
        w_s = matrix(self.text.s_k.toarray()).T
        for i in idx:
            sentences2words.append(array(w_s[i, :]).tolist())
        e = matrix(ones(len(sentences2words))).T
        sentence_weight = matrix(array(sentences2words)).T * e
        self.idx_s = argsort(array(-sentence_weight), axis=0)

    def get_sentence_weight(self):
        words_count = {}
        f = open('stopwords.txt', 'r')
        lines = f.readlines()
        f.close()
        if self.remove_stopwords == 1:
            stopwords = [line.strip() for line in lines]
        elif self.remove_stopwords == 0:
            stopwords = []

        sentences = self.text.sentenceset
        for sent in sentences:
            words = sent.sentence_text.split()
            words = [word.lower() for word in words]
            words = [word for word in words if word not in stopwords
                     and re.match(r'^[a-zA-Z]+$', word) is not None]
            for word in words:
                if word in words_count:
                    words_count[word] += 1;
                else:
                    words_count[word] = 1
        aux = [(words_count[k], k) for k in words_count.keys()]
        aux.sort()
        aux.reverse()
        self.count_words = aux


def test_tfidf():
    pk = r'D:\pythonwork\code\paperparse\paper\papers\pickle\P14-1007.xhtml_2.pickle'
#    pk = r'D:\pythonwork\code\paperparse\paper\papers\pickle\P14-1011.xhtml_2.pickle'
    pk = r'e:\pythonworknew\code\paperparse\paper\single\pk\testdimension_3.pk'
    model= TfIdf(pk,remove_stopwords=0)
    topksent = 10
    useabstr = 1
    maxword = -1
    tops = model.OutPutTopKSent(topksent,useabstr,maxword)
    i = 0
    print len(tops)
    for eachs in tops:
        print '----------------'
        print i, eachs
        i = i + 1
def main():
    test_tfidf()


if __name__=='__main__':
    main()



