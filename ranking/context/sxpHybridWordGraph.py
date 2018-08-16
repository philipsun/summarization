__author__ = 'a'
from sxpPackage import *
import networkx as nx
import numpy as np
from numpy import *
import re
from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer

class HybridWordGraph:
    def __init__(self, pickle_path, choice=2, iteration_times=20):
        self.w_s = None
        self.s_p = None
        self.p_c = None
        self.t_p = None
        self.s_t = None
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
        self.s_s = []
        self.section2sentence_id_list = {}
        self.idx_s = []
        self.text = LoadSxptext(pickle_path)
        choice = 2
        if choice == 1:
            self.get_parameters_with_stopwords()
        elif choice == 2:
            self.get_parameters_without_stopwords()

        w = matrix(random.rand(len(self.words))).T
        s = matrix(random.rand(len(self.text.sentenceset))).T
        self.voc_dict ={}
        self.MakeVocabularyDict()
        self.MakeSentSentMatrix()
        self.MakeWordWordMatrix()
    #this function is still in work, because we want to incoporate word-to-word matrix
    #but this hasn't been implemented because MakeWordWordMatrix is still not finished
    #so here iterationhybrid is just the same as in sxpHybridGraph.py
     #   self.s =self.RankSentenceNX()
     #   self.s = self.RankSentenceMyMat()
     #   print self.s
    #    self.iteration(w, s)
        self.iterationws(w,s)
     #   self.iterationhybrid(w,s)
        self.rank_weight()

     #   self.ordered_sentence_id_set()
    def MakeVocabularyDict(self):
        self.voc_dict ={}
        i = 0
        for w in self.words:
            self.voc_dict[w]=i
            i = i + 1

    def page_rank(self, pickle_path):
        g = create_graph(pickle_path)
        pr = nx.pagerank(g)
        self.idx_s = list(argsort(pr.values()))
        self.idx_s.reverse()
    def get_parameters_with_stopwords(self):
        self.words = self.text.sentence_tfidf.word
        # import relation matrix
        self.w_s = matrix(self.text.s_k.toarray()).T
        #self.w_s = matrix(self.text.sentence_tfidf.ct.toarray()).T #for version one
        self.s_p = matrix(self.text.p_s.toarray()).T
        self.p_c = matrix(self.text.c_p.toarray()).T
        self.t_p = matrix(self.text.p_t.toarray()).T
        self.s_t = matrix(self.text.t_s.toarray()).T
        nw,ns = self.w_s.shape
        ns,n_p = self.s_p.shape
        n_p,nc = self.p_c.shape
        nt,n_p = self.t_p.shape
        ns,nt = self.s_t.shape
        print 'nw',nw,'ns',ns,'np',n_p,'nt',nt,'nc',nc
        self.w = matrix(np.zeros((1,nw),dtype=np.float))
        self.s = matrix(np.zeros((1,ns),dtype=np.float))
        self.p = matrix(np.zeros((1,n_p),dtype=np.float))
        self.c = matrix(np.zeros((1,nc),dtype=np.float))
        self.t = matrix(np.zeros((1,nt),dtype=np.float))

#build graph between sentences
    def TestRankSentence(self):
        sentences = self.text.sentenceset
        ns = len(sentences)
        m = np.zeros((ns,ns), dtype=np.float)
        for i in range(len(sentences)):
            for j in range(i, len(sentences)):
                sent_a = set(sentences[i].sentence_text.split())
                sent_b = set(sentences[j].sentence_text.split())
                common_word = sent_a.intersection(sent_b)
                if not common_word:
                    continue
                jaccard = len(common_word) / float(len(sent_a.union(sent_b)))
                m[i,j]=jaccard
                m[j,i]=jaccard
        self.s_s = matrix(m)

        sentences = self.text.sentenceset
        g = nx.Graph()
        i = 0
        for sent in sentences:
            g.add_node(sent.id)
##            print i, sent.id, sentences[i].id
            i = i + 1
        for i in range(len(sentences)):
            for j in range(i, len(sentences)):
                sent_a = set(sentences[i].sentence_text.split())
                sent_b = set(sentences[j].sentence_text.split())
                common_word = sent_a.intersection(sent_b)
                if not common_word:
                    continue
                jaccard = len(common_word) / float(len(sent_a.union(sent_b)))
                g.add_edge(sentences[i].id, sentences[j].id, weight=jaccard)
                g.add_edge(sentences[j].id, sentences[i].id, weight=jaccard)

        nr,nc = self.s_s.shape
        gc = len(g)
        print nr,nc,gc
        gm = matrix(np.zeros((nr,nr),dtype=np.float))
        for i in range(nr):
            for j in g[i]:
                gij= g[i][j]
                gm[i,j] = gij['weight']

               # print gij['weight']
                if self.s_s[i,j] != gij['weight']:
                    print i,j, self.s_s[i,j],gij['weight']
        for i in range(nr):
            for j in range(nr):
                if gm[i,j] !=  self.s_s[i,j]:
                    if j in g[i]:
                        gij= g[i][j]
                        print i,j, self.s_s[i,j],gm[i,j],gij['weight']
                    else:
                        print j, 'not in g[i]', i, 'but', self.s_s[i,j], 'and m[i,j] is ', m[i,j]

        pr,W = nx.pagerank(g)

        self.idx_s = list(argsort(pr.values()))
        self.idx_s.reverse()
        print self.idx_s

        r,W1 = MyPageRankMatT(self.s_s,alreadysym=False)
        self.idx_s = argsort(r.flatten()).tolist()[0]
        self.idx_s.reverse()
        print self.idx_s
        print np.sum(W1,1)
        nw = matrix(np.zeros((nr,nr),dtype=np.float))
        for i in range(nr):
            for j in W[i]:
                wij= W[i][j]
               # print gij['weight']
                nw[i,j]= wij['weight']
##                if nw[i,j] != W1[i,j]:
##                    print i,j,nw[i,j],W1[i,j]
        print np.sum(nw,1)
        print np.sum(nw[0,:]), nw[0,:]
        print np.sum(W1[0,:]), W1[0,:]
    def MakeSentSentMatrix(self):
        sentences = self.text.sentenceset
        ns = len(sentences)
        m = np.zeros((ns,ns), dtype=np.float)
        for i in range(len(sentences)):
            for j in range(i, len(sentences)):
                sent_a = set(sentences[i].sentence_text.split())
                sent_b = set(sentences[j].sentence_text.split())
                common_word = sent_a.intersection(sent_b)
                if not common_word:
                    continue
                jaccard = len(common_word) / float(len(sent_a.union(sent_b)))
                m[i,j]=jaccard
                m[j,i]=jaccard
        self.s_s = matrix(m)
    def MakeWordWordMatrix(self):
        sentences = self.text.sentenceset
        ws = len(self.words )
        m = np.zeros((ws,ws), dtype=np.float)
        print m.shape
        for i in range(len(sentences)):
                sent_a = sentences[i].sentence_text.split()
             #   print sent_a
                idx = [self.voc_dict[w] for w in sent_a if w in self.voc_dict]
             #   print idx
                for j in range(len(idx)-1):
                    m[idx[j],idx[j+1]]=m[idx[j],idx[j+1]]+1
             #       print self.words[idx[j]],self.words[idx[j+1]]
        self.wf_wf = matrix(m)
        self.wf_wf =NormalizeMatrix(self.wf_wf)
    def RankSentenceMyMat(self):
        sentences = self.text.sentenceset
        ns = len(sentences)
        m = np.zeros((ns,ns), dtype=np.float)
        for i in range(len(sentences)):
            for j in range(i, len(sentences)):
                sent_a = set(sentences[i].sentence_text.split())
                sent_b = set(sentences[j].sentence_text.split())
                common_word = sent_a.intersection(sent_b)
                if not common_word:
                    continue
                jaccard = len(common_word) / float(len(sent_a.union(sent_b)))
                m[i,j]=jaccard
                m[j,i]=jaccard
        self.s_s = matrix(m)
        r,W1 = MyPageRankMatT(self.s_s,alreadysym=False)
       # idx_s = argsort(r.flatten()).tolist()[0]
       # idx_s.reverse()
        return r.T
    def RankSentenceNX(self):
        sentences = self.text.sentenceset
        g = nx.Graph()
        i = 0
        for sent in sentences:
            g.add_node(sent.id)
##            print i, sent.id, sentences[i].id
            i = i + 1
        for i in range(len(sentences)):
            for j in range(i, len(sentences)):
                sent_a = set(sentences[i].sentence_text.split())
                sent_b = set(sentences[j].sentence_text.split())
                common_word = sent_a.intersection(sent_b)
                if not common_word:
                    continue
                jaccard = len(common_word) / float(len(sent_a.union(sent_b)))
                g.add_edge(sentences[i].id, sentences[j].id, weight=jaccard)
                g.add_edge(sentences[j].id, sentences[i].id, weight=jaccard)

        pr = nx.pagerank(g)
        #self.idx_s = list(argsort(pr.values()))
        #self.idx_s.reverse()
        return matrix(pr.values()).T
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
        print len(self.words)
    def rank_weight(self):
        self.idx_w = argsort(array(-self.w), axis=0)
#        print self.s
        self.idx_s = argsort(array(-self.s), axis=0)
#        print self.idx_s
        self.idx_p = argsort(array(-self.p), axis=0)
        self.idx_c = argsort(array(-self.c), axis=0)
        self.idx_t = argsort(array(-self.t), axis=0)

    def ordered_sentence_id_set(self):
        #print len(self.idx_s)
        #print len(self.text.sentenceset)
        #print self.idx_s
       # print self.idx_s
        ranked_sentences = [self.text.sentenceset[self.idx_s[i]]
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
    def OutPutTopKSent(self, topk,useabstr = 1,maxwords = -1,strictmax=0):
        ranked_sentences = [self.text.sentenceset[self.idx_s[i]]
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
    def OutPutTopKSentWeight(self, topk,useabstr = 1,maxwords = -1,strictmax=0):
        ranked_sentences = [self.text.sentenceset[self.idx_s[i]]
                            for i in range(len(self.text.sentenceset))]
        ranked_sentences_weight = [self.s[self.idx_s[i]]
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
        print 'use topk', usetopk, 'maxword',maxwords
        i =0
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
                            sent_txt_set.append([usesent,ranked_sentences_weight[i]])
                            wordlen = wordlen + wl
                            break
                else:
                    if wordlen >= maxwords:
                        break
            wordlen = wordlen + wl#len(sentence.sentence_text)
            sent_txt_set.append([sentence.sentence_text,ranked_sentences_weight[i]])
            i = i + 1
        return sent_txt_set
    def OutPutTopKWords(self, topk=10):
        ranked_words = [self.words[self.idx_w[i]]
                            for i in range(len(self.words))]
        ranked_word_weights =  [self.w[self.idx_w[i]]
                            for i in range(len(self.w))]
        i = 0
        rw =[]
        for wd in ranked_words:
            if i>=topk:
                break
            rw.append([wd,ranked_word_weights[i]])
            i = i + 1
        return rw
    @staticmethod
    def normalize(w):
        assert(sum(w) > 0)
        w = w / sum(w)
        return w
    def update_sentence_weight_w_s(self, w,s):
        pass
    def update_sentence_weight(self, w, s):
        s = self.w_s.T * w + self.s_s*s
     #   s = self.s_s*s
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
        sec = self.p_c.T * p
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
    def update_word_weight_bycontext(self, w, s, t,p):
#        w = self.w_s * s + self.w_s * self.s_t * self.t_p * p #this is the mostly used one in previous experiments
        w = self.wf_wf * w + self.w_s * s + self.w_s*self.s_t*t + self.w_s * self.s_t * self.t_p * p #this is the latest one that incorporate context

        w = self.normalize(w)
        return w
    def update_word_weight_bywf(self,w):
        w = self.wf_wf * w
        w = self.normalize(w)
        return w
    def update_word_weight_bywfs(self,w,s):
        w = self.w_s * s
        w = self.normalize(w)
        return w

    def iterationhybrid(self,w,s):
        M = self.s_s
        N = M.shape[0]
        alpha,max_iter,S_S,x,per,dangling_weights,is_dangling=PreparePageRankMatrix(M,alpha=0.85,max_iter=100, p=None, alreadysym=True)
        i = 0
        tol=1.0e-6

        for _ in range(max_iter):
            xlast = x.copy()
            sw = sum(xlast.T[is_dangling])
            x = alpha * xlast*S_S + alpha * sw * dangling_weights + (1 - alpha) * per
            s =self.w_s.T * w
            x = x+s.T
            s=x.T
            t = self.s_t.T * s
            t = self.normalize(t)
            p = self.t_p.T * t
            p = self.normalize(p)
            sec = self.p_c.T * p
            sec = self.normalize(sec)
            w = self.w_s * s + self.w_s*self.s_t*t + self.w_s * self.s_t * self.t_p * p #this is the latest one that incorporate context
            w = self.normalize(w)
            i = i + 1
    #        x = alpha * M*x  + (1 - alpha) * p
            err = sum(abs(x-xlast))
            if err < N*tol:
                break
        self.s = x.T

    def iterationws(self,w,s):
        M = self.s_s
        N = M.shape[0]
        alpha,max_iter,self.s_s,x_s_s,pers_s,dangling_weights_s_s,is_dangling_s_s=PreparePageRankMatrix(self.s_s,alpha=0.85,max_iter=100, p=None, alreadysym=True)
        alpha,max_iter,self.wf_wf,x_wf_wf,per_wf_wf,dangling_weights_wf_wf,is_dangling_wf_wf=PreparePageRankMatrix(self.wf_wf,alpha=0.85,max_iter=100, p=None, alreadysym=True)

        i = 0
        tol=1.0e-6

        for i in range(self.times):
            #**********page rank style iteration********
            xlast_s_s = x_s_s.copy()
            sw = sum(xlast_s_s.T[is_dangling_s_s])
            x_s_s = alpha * xlast_s_s*self.s_s + alpha * sw * dangling_weights_s_s + (1 - alpha) * pers_s
            #*******************************************
            s =self.w_s.T * w # this is to compute the sentence weight from its word weight vector
            x_s_s = 0.5*x_s_s+0.5*s.T #this is to combine the sentence-sentence weight with its word weight
            s=x_s_s.T


##            #**********page rank style iteration********
            xlast_wf_wf =x_wf_wf.copy()
            sw = sum(xlast_wf_wf.T[is_dangling_wf_wf])
            x_wf_wf = alpha * xlast_wf_wf * self.wf_wf + alpha * sw * dangling_weights_wf_wf + (1 - alpha) * per_wf_wf
##            #*******************************************

            w1 = self.wf_wf*w
            w2 = self.w_s * s  #this is the latest one that incorporate context
            w = self.normalize(w1+w2)
            i = i + 1
    #        x = alpha * M*x  + (1 - alpha) * p
            err = sum(abs(x_s_s-xlast_s_s))
            print err
            if err < N*tol:
                break
        self.s = x_s_s.T
        self.w = w
        self.s = s

    def iteration(self, w, s):
        for i in range(self.times):
            s = self.update_sentence_weight(w, s)

            t = self.update_context_weigth(s)

            p = self.update_paragraph_weight_bycontext(t)

            c = self.update_section_weight(p)

            w = self.update_word_weight_bycontext(w, s, t, p)

          #  w = self.update_word_weight_bywf(w)
        self.w = w
        self.s = s
        self.p = p
        self.c = c
        self.t = t

# input : path, file_name
# output: matrix
def create_graph(text):
#    text = LoadSxptext(pickle_path)
    sentences = text.sentenceset
    g = nx.Graph()
    for sent in sentences:
        g.add_node(sent.id)
    for i in range(len(sentences)):
        for j in range(i, len(sentences)):
            sent_a = set(sentences[i].sentence_text.split())
            sent_b = set(sentences[j].sentence_text.split())
            common_word = sent_a.intersection(sent_b)
            if not common_word:
                continue
            jaccard = len(common_word) / float(len(sent_a.union(sent_b)))
            g.add_edge(sentences[i].id, sentences[j].id, weight=jaccard)
            g.add_edge(sentences[j].id, sentences[i].id, weight=jaccard)
    return g
def FindDanglingNodes(M,axis_id = 1):
    S = M.sum(axis=1)
    sel = np.where(S==0)
    return sel[0]
def NormalizeArrayMatrix(M,axis_id=1):
    S = np.sum(M,axis = axis_id)
    S[S != 0] = 1.0 / S[S != 0]
    Q = np.diag(S)
    M = np.dot(M,Q)
    return M
def NormalizeMatrix(M, axis_id = 1):
    S = M.sum(axis=1)
    sel = np.where(S==0)
    S[sel] = 1
    rown = M.shape[0]
    nm = M.copy()
    for r in range(rown):
        nm[r,:] = nm[r,:]/S[r]
    return nm
def MakeSymmetricMatrix(M,mode='half'):
    if mode == 'half':
        s = (M+M.T)/2
    if mode == 'merg':
        s = M.T.copy()
        nr = s.shape
        for index,x in np.ndenumerate(s):
            if s[index] ==0:
                s[index] = M[index]
            elif M[index] == 0:
                s[index] = s[index]
            else:
                s[index] = (s[index] + M[index])/2.0


    return s
def NormalizeMatrixFalse(M, axis_id=1):
    S = matrix(np.sum(M,axis = axis_id))
    sel = np.where(S!=0)
    S[sel] = 1.0 / S[sel]
    Q = np.diagflat(S.T)
    M = M*Q
    return M

def UpdateNormalizeDanglingMat(M):
    C = matrix(M)
    axis_id=1
    S = matrix(np.sum(C,axis = axis_id))
    colnum = C.shape[1]
    danglenodes = np.where(S == 0.0)
    nd = danglenodes[1].shape[1]
    if nd is None:
        return C
    st = matrix(np.ones((nd,colnum), dtype=np.float)*1.0/colnum)
    C[danglenodes[0],:] = st
    return C

def TestPageRankMatrix():
    M = matrix([[1.0,1.0,0.0,1.0],
         [1.0,0.0,0.0,0.0],
         [0.0,0.0,0.0,0.0],
         [1.0,1.0,0.0,1.0]])
    M = matrix(np.random.rand(10,10))
    print 'matrix m', M
    print 'transposed m',M.T
    M = MakeSymmetricMatrix(M,mode='merg')
    print 'symmetrized', M
    nM = NormalizeMatrix(M)
    print 'normalized matrix',nM
    g = MakeGraphObjectFromMatrix(M)
##    for i in range(M.shape[0]):
##        print i,g[i]
    nr,nc = M.shape
    gc = len(g)
    print nr,nc,gc

    for i in range(nr):
        for j in g[i]:
            gij= g[i][j]
           # print gij['weight']
            if M[i,j] != gij['weight']:
                print i,j, M[i,j],gij['weight']

    v = nx.pagerank(g)
    print 'vpagerank',v.values()
    v = MyPageRankMatT(M) #this will be the equal implementation of nx.pagerank because it treat M as an
    print('vmypagerank',v)


def MyPageRank(M,alpha=0.9,max_iter=20, p=None):
    #note M is a matrix object, and row is out degree
    N = M.shape[0]
    M=NormalizeMatrix(M,1)
    if p is None:
        p = matrix(np.repeat(1.0 / N, N)).T
    dangling_weights = matrix(np.repeat(1.0 / N, N)).T
    axis_id = 1
    S = matrix(np.sum(M,axis = axis_id))


    x = matrix(np.random.rand(N,1))
    is_dangling = np.where(S == 0)[0]
    sw = sum(x[is_dangling])
#    max_iter = 20
    for _ in range(max_iter):
        sw = sum(x[is_dangling])
        x = alpha * ( M*x + sw * dangling_weights) + (1 - alpha) * p
    return x
def MyPageRankMat(M,alpha=0.85,max_iter=100, p=None):
    #note M is a matrix object, and row is out degree
    N = M.shape[0]
    M=NormalizeMatrix(M,1)
#    M=UpdateNormalizeDanglingMat(M)
    if p is None:
        p = matrix(np.repeat(1.0 / N, N)).T
    dangling_weights = matrix(np.repeat(1.0 / N, N)).T
    axis_id = 1
    S = matrix(np.sum(M,axis = axis_id))


    x = matrix(np.ones((N,1),dtype = np.float)*1.0/N)
    is_dangling = np.where(S == 0)[0]
    is_dangling = []
    sw = sum(x[is_dangling])

#    max_iter = 20
    for _ in range(max_iter):
        sw = sum(x[is_dangling])
        x = alpha * M*x + sw * dangling_weights + (1 - alpha) * p
#        x = alpha * M*x  + (1 - alpha) * p
    return x
def MakeGraphObjectFromMatrix(M,makebidirect=False):
    nr,nc=M.shape
    print M
    g = nx.Graph()
    for i in range(nr):
        g.add_node(i)
    for i in range(nr):
        for j in range(nc):
            jaccard = M[i,j]
          #  print 'i,j',i,j,jaccard
            g.add_edge(i, j, weight=jaccard)
          #  g.add_edge(j, i, weight=jaccard)
    return g

def MakeAdjecentMatrix(M):
    dm= M.copy()
    sel = np.where(dm>0.0)
    dm[sel] = 1
    return dm
def PreparePageRankMatrix(M,alpha=0.85,max_iter=100, p=None, alreadysym=True):
        #note M is a matrix object, and row is out degree
  #  M = MakeSymmetricMatrix(M+M.T) #make it undirected so that it can be used to rank sentence like nx.pagerank
    if alreadysym == False:
        M = MakeSymmetricMatrix(M,mode='merg')
    N = M.shape[0]
    W=NormalizeMatrix(M,1)
#    M=UpdateNormalizeDanglingMat(M)
    if p is None:
        p = matrix(np.repeat(1.0 / N, N)).T
    dangling_weights = matrix(np.repeat(1.0 / N, N)).T
    axis_id = 1
    S = matrix(np.sum(W,axis = axis_id))


    x = matrix(np.ones((N,1),dtype = np.float)*1.0/N)
    is_dangling = np.where(S == 0.0)[0]
    sw = sum(x[is_dangling])
    x = x.T
    dangling_weights = dangling_weights.T
    p= p.T
#    max_iter = 20
    tol=1.0e-6
    i = 0
    return alpha,max_iter,W,x,p,dangling_weights,is_dangling
def MyPageRankMatT(M,alpha=0.85,max_iter=100, p=None, alreadysym=True):
    #note M is a matrix object, and row is out degree
  #  M = MakeSymmetricMatrix(M+M.T) #make it undirected so that it can be used to rank sentence like nx.pagerank
    if alreadysym == False:
        M = MakeSymmetricMatrix(M,mode='merg')
    N = M.shape[0]
    W=NormalizeMatrix(M,1)
#    M=UpdateNormalizeDanglingMat(M)
    if p is None:
        p = matrix(np.repeat(1.0 / N, N)).T
    dangling_weights = matrix(np.repeat(1.0 / N, N)).T
    axis_id = 1
    S = matrix(np.sum(W,axis = axis_id))


    x = matrix(np.ones((N,1),dtype = np.float)*1.0/N)
    is_dangling = np.where(S == 0.0)[0]
    sw = sum(x[is_dangling])
    x = x.T
    dangling_weights = dangling_weights.T
    p= p.T
#    max_iter = 20
    tol=1.0e-6
    i = 0
    for _ in range(max_iter):
        xlast = x.copy()
        sw = sum(xlast.T[is_dangling])
        x = alpha * xlast*W + alpha * sw * dangling_weights + (1 - alpha) * p
##        if i == 0:
##            print sw
##            print alpha
##
##            print x
        i = i + 1
#        x = alpha * M*x  + (1 - alpha) * p
        err = sum(abs(x-xlast))
        if err < N*tol:
            return x,W
    return x,W

def TestPickle():
    pk = r'D:\pythonwork\code\paperparse\paper\papers\pickle\P14-1007.xhtml_2.pickle'
#    pk = r'D:\pythonwork\code\paperparse\paper\papers\pickle\P14-1011.xhtml_2.pickle'
    pk = r'D:\pythonwork\code\paperparse\paper\single\pk\testdimension_3.pk'
    model= HybridWordGraph(pk)
    topksent = 10
    useabstr = 0
    maxwords = -1
    strictmax=0
    tops = model.OutPutTopKSentWeight(topksent,useabstr,maxwords,strictmax)
    i = 0
    for eachs in tops:
        print '----------------'
        print i, eachs
        i = i + 1
    tpwd =100
    i=0
    rw=model.OutPutTopKWords(tpwd)
    for wd in rw:
        print '----------------'
        print i, wd[0],wd[1]
        i = i + 1
if __name__ == '__main__':
    #TestNormalizeMatrixA()
    TestPickle()
  #  TestPageRankMatrix()
"""
def test_page_rank():
    path = r'C:\Users\a\PycharmProjects\extractInfo\papers'
    file_name = 'P14-1007.xhtml'
    pickle_path = path + '\\pickle\\' + file_name + '_1.pickle'
    page_rank(pickle_path)


def main():
    test_page_rank()

"""