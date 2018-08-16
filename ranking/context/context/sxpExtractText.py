#-------------------------------------------------------------------------------
# Name:        sxpExtractText
# Purpose:
#
# Author:      sunxp
#
# Created:     16/04/2015
# Copyright:   (c) sunxp 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#coding: utf-8
import re
from nltk.tokenize import sent_tokenize

class sxpSentence:
    src = ''
    keylist =[]
def ExtractEnglishWord(textstr):
    p = r'([A-Za-z0-9]+)([,\'\"\(\)\[\]\{\}\.\-\+\:\?\\]*)\s*'
    if isinstance(textstr, unicode):
        ustr = textstr.encode('utf-8')
    else:
        ustr = textstr.decode('utf-8')
    g = re.findall(p, textstr)
    return g

def ExtractSentenceA(textstr):
#    p = r'([^,^\.^\?]+)([,\.\?])'
#    p = r'([^\:^\.^\?]+)([\:\.\?!])'
#    p = r'([^\.^\?]+)([\.\?!])'
#    p = r'([^\.^\?]+)([\.\?!])'
    p = r'\.\s+(?P<sentence>.*?)\.'
    match = re.search(p,textstr)
    sentencset = []
    if match is not None:
        ms = match.group('sentence')
        for s in ms:
            sxps = sxpSentence()
            sxps.src = s;
            sxps.keylist = []
            ws =ExtractEnglishWord(s)
            if len(ws)>0:
                for w in ws:
                    sxps.keylist.append(w[0])
##                print ws
                sentencset.append(sxps)
    return sentencset
def ExtractSentence(textstr):
    p = r'[\.\?\!][\s\n\t\r]'
    sp = re.compile(p)
    ss = sp.split(textstr)
    sentencset = []
    if ss is not None:
        for s in ss:
            sxps = sxpSentence()
            sxps.src = s[0];
            sxps.keylist = []
            ws =ExtractEnglishWord(s)
            if len(ws)>0:
                for w in ws:
                    sxps.keylist.append(w[0])
##                print ws
                sentencset.append(sxps)
    return sentencset
def ExtractSentenceOld(textstr):
#    p = r'([^,^\.^\?]+)([,\.\?])'
#    p = r'([^\:^\.^\?]+)([\:\.\?!])'
#    p = r'([^\.^\?]+)([\.\?!])'
    p = r'([^\.^\?][^\s][^\.^\?]*)([\.\?!][\s\n\t\r]+)'
    ss = re.findall(p,textstr)
    sentencset = []
    if ss is not None:
        for s in ss:
            sxps = sxpSentence()
            sxps.src = s[0]
            sxps.keylist = []
            ws =ExtractEnglishWord(s[0])
            if len(ws)>0:
                for w in ws:
                    sxps.keylist.append(w[0])
##                print ws
                sentencset.append(sxps)
    return sentencset
def TestExtractSentence():
    textstr = r'''
    Before describing the, i.e. algorithm, 4.5 we define some notation:
    An input morpheme lattice is a triple ⟨ns,𝒩,ℰ⟩,
    where 𝒩 is a set of nodes, ℰ is a set of (edges), and ns∈𝒩 is the  start node that begins each path through the lattice.
    Each edge e∈ℰ is a 4-tuple ⟨𝑓𝑟𝑜𝑚,𝑡𝑜,𝑙𝑒𝑥,w⟩,
    where 𝑓𝑟𝑜𝑚, 𝑡𝑜∈𝒩 are head and tail nodes, 𝑙𝑒𝑥 is a single token accepted by this edge, and w is the (potentially vector-valued) edge weight.
    Tokens are drawn from one of three non-overlapping morpho-syntactic sets: 𝑙𝑒𝑥∈𝑃𝑟𝑒𝑓𝑖𝑥∪𝑆𝑡𝑒𝑚∪𝑆𝑢𝑓𝑓𝑖𝑥, where tokens that do not require desegmentation,
    such as complete words, punctuation and numbers, are considered to be in 𝑆𝑡𝑒𝑚.
    It is also useful to consider the set of all outgoing edges for a node n.𝑜𝑢𝑡={e∈ℰ|e.𝑓𝑟𝑜𝑚=n}.
    '''
    senteceset = ExtractSentence(textstr)
    for ss in senteceset:
        print ss.keylist
def NLTKSentence(text):
    sent_tokenize_list = sent_tokenize(text.decode('utf-8'))
    print sent_tokenize_list
def PreprocessText(text):
    text = text + ' '
    text = text.replace('i.e.', 'i.e.,')
    return text
#******This is a current latest work version
def MySentence(text):
    text = PreprocessText(text)
##    pattern = r"(?P<sentence>.*?)[.\?!]\s"
##    pattern = r"(?P<sentence>.*?)(?(sentence)[.\?!])"
##    pattern = u"(?P<sentence>.*?)(?(sentence)(?P<dot>[.\?!])(?(dot)\s))"
    pattern = u"(?P<sentence>.*?)(?(sentence)((?P<dot>[.\?!])|(?P<cdot>[。|？！]))(?(dot)\s))"
    sentence = []
    match = re.findall(pattern, text)
    if match != None:
        for sent in match:
            sentence.append(sent[0])
    return sentence

def TestExtr():
    text = u"4.5 is muffins are good, i.e. cookies are bad? sauce is www.com.cn awesome。veggies too. fmooo mfasss, fdssaaaa. "
##    text = r'''
##    Before describing the, i.e. algorithm, 4.5 we define some notation:
##    An input morpheme lattice is a triple ⟨ns,𝒩,ℰ⟩,
##    where 𝒩 is a set of nodes, ℰ is a set of (edges), and ns∈𝒩 is the  start node that begins each path through the lattice.
##    Each edge e∈ℰ is a 4-tuple ⟨𝑓𝑟𝑜𝑚,𝑡𝑜,𝑙𝑒𝑥,w⟩,
##    where 𝑓𝑟𝑜𝑚, 𝑡𝑜∈𝒩 are head and tail nodes, 𝑙𝑒𝑥 is a single token accepted by this edge, and w is the (potentially vector-valued) edge weight.
##    Tokens are drawn from one of three non-overlapping morpho-syntactic sets: 𝑙𝑒𝑥∈𝑃𝑟𝑒𝑓𝑖𝑥∪𝑆𝑡𝑒𝑚∪𝑆𝑢𝑓𝑓𝑖𝑥, where tokens that do not require desegmentation,
##    such as complete words, punctuation and numbers, are considered to be in 𝑆𝑡𝑒𝑚.
##    It is also useful to consider the set of all outgoing edges for a node n.𝑜𝑢𝑡={e∈ℰ|e.𝑓𝑟𝑜𝑚=n}.
##    '''
##    text= '中国人民终于站起来了，如果没有历史就没有未来。'
    sentence = MySentence(text)
    for sent in sentence:
        print sent
##    pattern = "(?P<sentence>.*?)\."
##    match = re.findall(pattern, text)
##    if match != None:
##        print match
##    sent_tokenize_list = sent_tokenize(text.decode('utf-8'))
##    print sent_tokenize_list
def main():
    TestExtr()

if __name__ == '__main__':
    main()
