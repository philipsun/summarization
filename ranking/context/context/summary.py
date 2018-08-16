__author__ = 'jane'
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import numpy as np
from sklearn.decomposition import PCA
from context import cosine_similarity
from preprocess.sxpPackage import LoadSxptext
from model.tjModel import MyModel
import sys


data_dir = r'C:\Users\jane\Documents\context-based text summarization\data\processed\papers'



def max_idx(a):
    print type(a)
    '''
    :param a: dict
    :return idx : int
    '''
    mx = -1
    idx = -1
    for k, v in a.items():
        if v > mx:
            mx = v
            idx = k
    return idx




def MMR(text, w, limit=10, lam=0.5, thredhold=0.2):
    #print 'type(w) ',type(w)
    #print 'type(idx_w) ',type(idx_w)

    summary = []
    visited = []
    dd_max = {}
    mmr_max = {}
    for i in range(len(w)):
        mmr_max[i] = w[i]
        dd_max[i] = 0

    vectorizer = CountVectorizer(min_df=1, stop_words='english',token_pattern='\w+')
    X = vectorizer.fit_transform(text).toarray()
    #print np.shape(X)
    transformer = TfidfTransformer()
    tfidf = transformer.fit_transform(X)
    pca = PCA(n_components=50)
    X_r = pca.fit(tfidf.toarray()).transform(tfidf.toarray())
    print w
    while len(visited) <= limit:
        print 'type(mmr_max) ', type(mmr_max)

        idx = max_idx(mmr_max)
        print idx
        mmr_max.pop(idx)
        dd_max.pop(idx)

        ## update the max weight dict
        for k, v in dd_max.items():
            sim = cosine_similarity(X_r[idx], X_r[k])
            if sim > v:
                dd_max[k] = sim
        #print idx
        visited.append(idx)
        for k in mmr_max.keys():
            mmr_max[k] = lam * w[k] - (1 - lam) * dd_max[k]

    for i in visited:
        summary.append(text[i])
    return summary


def test_MMR(filename):
    path = data_dir + '\\' + filename + '_1.pickle'
    text = []

    model = MyModel(path)
    for s in model.text.sentenceset:
        text.append(s.sentence_text)
    #print 'in the summary...'
    #print 'type(model.idx_w) ', model.idx_w
    #print 'type(model.w) ', model.w

    summary = MMR(text,model.s)
    for s in summary:
        print s


def main():
    sys.path.append(r"C:\Users\jane\Documents\context-based text summarization\text-summarization-system\preprocess")
    sys.path.append(r"C:\Users\jane\Documents\context-based text summarization\text-summarization-system\model")
    sys.path.append(r"C:\Users\jane\Documents\context-based text summarization\text-summarization-system\evaluate")

    filename = r'P14-1008.xhtml'
    test_MMR(filename)


if __name__ == '__main__':
    main()