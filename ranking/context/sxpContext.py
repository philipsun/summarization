#-------------------------------------------------------------------------------
# Name:        sxpContext
# Purpose:
#
# Author:      sunxp
#
# Created:     26/10/2015
# Copyright:   (c) sunxp 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------

def Similarity(sentence, s):
    #if sentence is a tf-idf vector, then use cosine similarity
    #if sentence is a string, use jaccard similarity
    if re.match('.+', s):
        return jaccard_similarity(sentence, s)
    else:
        return cosine_similarity(sentence, s)


def jaccard_similarity(sentence, s):
    stopwords = open('stopwords.txt','r').readlines()
    word_list1 = []
    word_list2 = []
    for word in nltk.sent_tokenize(sentence):
        if word not in stopwords:
            word_list1.append(word)
    for word in nltk.sent_tokenize(s):
        if word not in stopwords:
            word_list2.append(word)
    return set(word_list2).intersection(set(word_list1))/set(word_list2).union(set(word_list1))



def cosine_similarity(sentence, s):
    x = np.array(sentence)
    y = np.array(s)
    Lx = np.sqrt(x.dot(x))
    Ly = np.sqrt(y.dot(y))
    cos_angle = x.dot(y)/(Lx * Ly)
    return cos_angle
def main():
    pass

if __name__ == '__main__':
    main()
