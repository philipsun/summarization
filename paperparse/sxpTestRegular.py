#-------------------------------------------------------------------------------
# Name:        模块1
# Purpose:
#
# Author:      sunxp
#
# Created:     31/03/2015
# Copyright:   (c) sunxp 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#coding: utf-8
import re
from collections import Counter
import sxpProcessParaText

def main():
    email = r'hello@kg.ict.ac.cn'
    g= re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email)
    if g is not None:
        print 'is ok', g.groups()

    str = 'abcd'
    p = r'abcd$'
    g = re.match(p,str)
    if g is not None:
        print g.groups()

    p = '^(S+)(\d+\\.S+)*'
    str = 'SSSS1.S2.SSS1'
    g = re.match(p,str)
    if g is not None:
        print len(g.groups()), g.groups()

    p = r'(S+)(\d+)'
    str = 'SSSS1.S2.SSS1'
    g = re.match(p,str)
    if g is not None:
        print len(g.groups()), g.groups()

    p = '(S+)(\d*)\\.p(\d+)'
    str = 'SSS1.p1'
    g = re.match(p,str)
    if g is not None:
        print len(g.groups()), g.groups()
    else:
        print 'none'

    p = '(.+)(\d+)\\.p(\d+)'
    str = 'SSS1.p1'
    g = re.match(p,str)
    if g is not None:
        print '4', len(g.groups()), g.groups()
    else:
        print 'none'


    p = '(.+)(\d+)\\.p(\d+)$'
    str = 'ss.SSS1.p1'
    g = re.match(p,str)
    if g is not None:
        print len(g.groups()), g.groups()
    else:
        print 'none'
    p = '(.+)\\.p(\d+)$'
    str = 's1.ss.SSS1.p1'
    g = re.match(p,str)
    if g is not None:
        print len(g.groups()), g.groups()
    else:
        print 'none'
def TestEnglishWord():
    textstr = r'''
    Before describing the algorithm, we define some notation:
    An input morpheme lattice is a triple ⟨ns,𝒩,ℰ⟩,
    where 𝒩 is a set of nodes, ℰ is a set of (edges), and ns∈𝒩 is the start node that begins each path through the lattice.
    Each edge e∈ℰ is a 4-tuple ⟨𝑓𝑟𝑜𝑚,𝑡𝑜,𝑙𝑒𝑥,w⟩,
    where 𝑓𝑟𝑜𝑚, 𝑡𝑜∈𝒩 are head and tail nodes, 𝑙𝑒𝑥 is a single token accepted by this edge, and w is the (potentially vector-valued) edge weight.
    Tokens are drawn from one of three non-overlapping morpho-syntactic sets: 𝑙𝑒𝑥∈𝑃𝑟𝑒𝑓𝑖𝑥∪𝑆𝑡𝑒𝑚∪𝑆𝑢𝑓𝑓𝑖𝑥, where tokens that do not require desegmentation,
    such as complete words, punctuation and numbers, are considered to be in 𝑆𝑡𝑒𝑚.
    It is also useful to consider the set of all outgoing edges for a node n.𝑜𝑢𝑡={e∈ℰ|e.𝑓𝑟𝑜𝑚=n}.
    '''

    p = r'([A-Za-z0-9,\.\-\+\:\?\\]+)\s+'

    print 'extracting dot, comma*******************'
    g = re.findall(p,textstr)
    if g is not None:
        for t in g:
            print t


    print 'extracting dot, comma*******************'
    p = r'([A-Za-z0-9]+)([,\.\-\+\:\?\\]*)\s+'

    g = re.findall(p,textstr)
    if g is not None:
        for t in g:
            print t

    p = r'([A-Za-z0-9]+|[A-Za-z0-9,\.\-\+\:\?\\]*)\s+'

    print 'extracting dot, comma*******************'
    g = re.findall(p,textstr)
    if g is not None:
        for t in g:
            print t


    print 'extracting dot, comma*******************'
    p = r'([A-Za-z0-9]+)([,\'\"\(\)\[\]\{\}\.\-\+\:\?\\]*)\s+'

    g = re.findall(p,textstr)
    if g is not None:
        for t in g:
            print t
def TestRegular():
    textstr = r'''
    Before describing the algorithm, we define some notation:
    An input morpheme lattice is a triple ⟨ns,𝒩,ℰ⟩,
    where 𝒩 is a set of nodes, ℰ is a set of (edges), and ns∈𝒩 is the start node that begins each path through the lattice.
    Each edge e∈ℰ is a 4-tuple ⟨𝑓𝑟𝑜𝑚,𝑡𝑜,𝑙𝑒𝑥,w⟩,
    where 𝑓𝑟𝑜𝑚, 𝑡𝑜∈𝒩 are head and tail nodes, 𝑙𝑒𝑥 is a single token accepted by this edge, and w is the (potentially vector-valued) edge weight.
    Tokens are drawn from one of three non-overlapping morpho-syntactic sets: 𝑙𝑒𝑥∈𝑃𝑟𝑒𝑓𝑖𝑥∪𝑆𝑡𝑒𝑚∪𝑆𝑢𝑓𝑓𝑖𝑥, where tokens that do not require desegmentation,
    such as complete words, punctuation and numbers, are considered to be in 𝑆𝑡𝑒𝑚.
    It is also useful to consider the set of all outgoing edges for a node n.𝑜𝑢𝑡={e∈ℰ|e.𝑓𝑟𝑜𝑚=n}.
    '''
    print 'extracting sentence, comma*******************'
    p = r'([^,^\.^\?]+)([,\.\?])'

    g = re.findall(p,textstr)
    if g is not None:
        for s in g:
            print s
            ws =sxpProcessParaText.ExtractEnglishWord(s[0])
            print ws
def TestTuple():
    paraid_str = 'S3.SS4.SSSx3.P1.p2'.lower()
    if isinstance(para_id,list):
        paraid_str = para_id[0]
    else:
        paraid_str = para_id
    if  paraid_str is not None:
        p = '(.+)\\.p(\d+)$'
        g = re.match(p,paraid_str,0)
        if g is not None:
            print g.groups()
        else:
            print [paraid_str,'0'];
    else:
        print['noid','0']
def TestTupleA():
    para_id = 'S3.SS4.SSSx3.P1.p2'.lower()
    if isinstance(para_id,list):
        paraid_str = para_id[0]
    else:
        paraid_str = para_id
    para_seg = paraid_str.split('.')
    p = '^(s+)x*\d+'
    pp = '^(p+)x*\d+'
    sectstr= ''
    parastr = ''
    for seg in para_seg:
        g = re.match(p,seg,0)
        if g is not None:
            if len(sectstr)==0:
                sectstr = sectstr+seg
            else:
                sectstr = sectstr+'.'+seg
        g = re.match(pp,seg,0)
        if g is not None:
            if len(parastr)==0:
                parastr = parastr+seg
            else:
                parastr = parastr+'.'+seg


    print sectstr, parastr
def TestTokenize():
    pt = u'(?u)\\b\\w\\w+\\b'
    pt = u'(?u)\\b\w+\\b'
    tp = re.compile(pt)
    f= lambda doc: tp.findall(doc)
    ctstr = u'hello this is a test, and we are going to let the test run'
    print f(ctstr)
if __name__ == '__main__':
   # TestEnglishWord()
    #TestRegular()
    #TestTupleA()
    TestTokenize()
