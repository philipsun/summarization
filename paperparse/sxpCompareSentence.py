#-------------------------------------------------------------------------------
# Name:        模块1
# Purpose:
#
# Author:      sunxp
#
# Created:     13-06-2015
# Copyright:   (c) sunxp 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import sxpExtractText
import sxpPaperIntroSentLabel
import tjPaperIntroSentLabel
import sxpReadFileMan
#from  sxpPaperAnalysisA1 import *
import pickle
import os
import re
import win32file
def StoreSxptext(sxptxt, fname):
    f = open(fname,'wb')
    pickle.dump(sxptxt,f)
    f.close()
def LoadSxptext(fname):
    f = open(fname,'rb')
    sxptxt = pickle.load(f)
    f.close()
    return sxptxt
def GetIntroLabel():
    return sxpPaperIntroSentLabel.intro_sent
def GetIndexInSet(v, listset,prevmatch):
    if v in listset[prevmatch:]:
        return listset.index(v,prevmatch)
    else:
        return -1
def MatchOneList2Another(list1, list2):
    matchindex =[]
    n1 = len(list1)
    i = 0
    prevmatch = -1
    while i < n1:
        el=list1[i]
        if prevmatch == -1:
            m = GetIndexInSet(el,list2,0)
            if m>-1:
                prevmatch = m
            else:
                prevmatch = -1
            matchindex.append(m)
        else:
            m = GetIndexInSet(el,list2,prevmatch)
            if m>-1:
                prevmatch = m
            else:
                prevmatch = -1
            matchindex.append(m)
        i = i + 1
    return matchindex
def MaxMatch(matchindex):
    n = len(matchindex)
    i = 0
    con_len = 0
    con_index = -1
    max_len = -1
    starti= 0
    while i<n:
        starti = i
        if matchindex[i]== -1:
            i = i + 1
            continue
        j = i+1
        if j>= n:
            break
        match = 0
        while j<n:
            if matchindex[i]==matchindex[j]-1:
                i = j
                j = j + 1
                match = 1
            else:
                break
        if match == 1:
            con_len = j - starti
            if con_len>max_len:
                con_index = starti
                max_len = con_len
        i = j
    return [max_len, con_index]
def TestMatch():
    list1 = [0,0,0]
    list2 = [1,1,1]
    list3 = [1,0,1]
    list4 = [0,1,1]
    list5 = [0,0,1]
    list6 = [1,1,0]
    print MaxMatch(list1)
    print MaxMatch(list2)
    print MaxMatch(list3)
    print MaxMatch(list4)
    print MaxMatch(list5)
    print MaxMatch(list6)
def CalcuDistTwoSent(st1, st2):
    rst1 = sxpExtractText.ExtractEnglishWordA(st1.lower())
    rst2 = sxpExtractText.ExtractEnglishWordA(st2.lower())
    matchindex12 = MatchOneList2Another(rst1,rst2)
    matchindex21 = MatchOneList2Another(rst2,rst1)
    maxmatch12 = MaxMatch(matchindex12)
    maxmatch21 = MaxMatch(matchindex21)
    dist = maxmatch12[0] + maxmatch21[0]
    n1 = len(rst1)
    n2 = len(rst2)
    if dist< (n1+n2)/2:
        parth = -1
    else:
        parth = 1
    return dist, parth

def CompareTwoSent(st1, st2):
    rst1 = sxpExtractText.ExtractEnglishWordA(st1.lower())
    rst2 = sxpExtractText.ExtractEnglishWordA(st2.lower())
    matchindex12 = MatchOneList2Another(rst1,rst2)
    matchindex21 = MatchOneList2Another(rst2,rst1)
    maxmatch12 = MaxMatch(matchindex12)
    maxmatch21 = MaxMatch(matchindex21)
#    dist = maxmatch12[0] + maxmatch21[0]
    dist = zip(maxmatch12, maxmatch21)
    return dist
def FindMatchSentence(srcsent,sxpSentset):
    idset = []
    for sent in srcsent:
        id = FindClosedMatch(sent,sxpSentset)
        idset.append(id)
    return idset
def DeterminMatched(sent, sxpSentset):
    dists =[]
    for sxpsent in sxpSentset:
        st = sxpsent.sentence_text
        dist = CompareTwoSent(sent, st)
        dists.append(dist)
    d = max(dists)
    id = dists.index(d)
    nl = len(sent)
    sl = len(sxpSentset[id].sentence_text)
    if d>= (nl+sl)/2:
        return id
    return -1
def FindClosedMatch(sent, sxpSentset):
    dists =[]
    for sxpsent in sxpSentset:
        st = sxpsent.sentence_text
        dist = CompareTwoSent(sent, st)
        dists.append(dist)
    d = max(dists)
    id = dists.index(d)
    return id
def TestTwoSent():
    pap= sxpPaperIntroSentLabel.intro_sent[0]
    n = len(pap)
    sentset = pap[1:n]

    st1 = sentset[0]
    st2 = sentset[5]
    rst1 = sxpExtractText.ExtractEnglishWordA(st1.lower())
    rst2 = sxpExtractText.ExtractEnglishWordA(st2.lower())
    print rst1
    print rst2
    matchindex12 = MatchOneList2Another(rst1,rst2)
    matchindex21 = MatchOneList2Another(rst2,rst1)
    print matchindex12
    print matchindex21
    maxmatch12 = MaxMatch(matchindex12)
    maxmatch21 = MaxMatch(matchindex21)
    print maxmatch12
    print maxmatch21
def TestCompareTwoSent():
    dist = []
    pap= sxpPaperIntroSentLabel.intro_sent[0]
    n = len(pap)
    sentset = pap[1:n]
    n = len(sentset)
    st1 = sentset[0]
    i = 0
    while i < n:
         st2 = sentset[i]
         dist.append(CompareTwoSent(st1,st2))
         i = i + 1
    print dist
def MarkLabelSentID(fname):
    sxptxt = LoadSxptext(fname)
    sentenceset = sxptxt.sentenceset
    labelsentID = []
    for sent in sentenceset:
        id = FindClosedMatch(sent, sxpSentset)
        labelsentID.append(id)
    return labelsentID

paperpath = r'D:\pythonwork\code\paperparse\paper\papers'
def GetSentenceIDs(sentset, idsentset):
    matchidset = []
    for labelsent in sentset:
        id = DeterminMatched(labelsent,sxpSentset)
        matchidset.append(id)
        if id >= 0:
            matchedsent = sxpSentset[id]
            print 'label:', labelsent
            print 'sent:',matchedsent.sentence_text
            print '********'
        else:
            print 'label:',labelsent
            print 'not found'
    return matchidset

def TestIntroLabelID():
  #  LabelSet = sxpPaperIntroSentLabel.intro_sent
    pickpath = r'D:\pythonwork\code\paperparse\paper\papers\pickle'
    paperpath =  r'D:\pythonwork\code\paperparse\paper\papers'
    LabelSet = tjPaperIntroSentLabel.intro_sent
    include_absconc = True
    if include_absconc == True:
        filesuffix = '.xhtml_2.pickle'
        savepicklepref  = 'xhtml_2'
    if include_absconc == False:
        filesuffix = '.xhtml_3.pickle'
        savepicklepref  = 'xhtml_3'
    sentenceID,sentdictID =GetLabelSentID(LabelSet,pickpath,filesuffix)
    fname = pickpath + '\\'+savepicklepref+'intro_sent_id.pickle'
    StoreSxptext(sentenceID,fname)
    fname = pickpath + '\\'+savepicklepref+'intro_sent_dict_id.pickle'
    StoreSxptext(sentdictID,fname)
def DisplayID():
    pickpath = r'D:\pythonwork\code\paperparse\paper\papers\pickle'
    paperpath =  r'D:\pythonwork\code\paperparse\paper\papers'
    include_absconc = True
    if include_absconc == True:
        filesuffix = '.xhtml_2.pickle'
        savepicklepref  = 'xhtml_2'
    if include_absconc == False:
        filesuffix = '.xhtml_3.pickle'
        savepicklepref  = 'xhtml_3'
    fname = pickpath + '\\'+savepicklepref+'intro_sent_id.pickle'
    ids = LoadSxptext(fname)
    for eachs in ids:
        print ids
    fname = pickpath + '\\'+savepicklepref+'intro_sent_dict_id.pickle'
    print len(ids)
    ids = LoadSxptext(fname)
    print len(ids)
    for eachs in ids:
        print ids

def GetLabelSentID(LabelSet,pickpath,filesuffix):
    LabelPaperIDSet = []
    LabelDictIDSet ={}
    i = -1
    for each_paper in LabelSet:
        papername = each_paper[0]
        paplabel = each_paper[1:]
      #  fname = paperpath + '\\pickle\\'  + papername +  '.xhtml_1.pickle'
        fname = pickpath + '\\'+papername + filesuffix
        paperkeyname = papername + '.xhtml'
        print fname
        i = i + 1
        if os.path.exists(fname) == False:
            matchidset =[]
            for labelsent in paplabel:
                matchidset.append(-1)
            print 'no such file'
            LabelPaperIDSet.append(matchidset)
            continue;
        sxptxt = LoadSxptext(fname)
        sxpSentset = sxptxt.sentenceset
        matchidset =[]
     #   matchidset.append(i*-1)
        for labelsent in paplabel:
            id = DeterminMatched(labelsent,sxpSentset)
            if id >= 0:
                matchedsent = sxpSentset[id]
                print 'label:', labelsent
                print 'sent:',matchedsent.sentence_text
                print '********'
                if id in matchidset:
                    print 'already in'
                    continue
                matchidset.append(id)
            else:
                print 'label:',labelsent
                print 'not found'
        LabelPaperIDSet.append(matchidset)
        LabelDictIDSet[paperkeyname.lower()] = matchidset
    return LabelPaperIDSet,LabelDictIDSet
def TestProduceIntroModel():
  #  LabelSet = sxpPaperIntroSentLabel.intro_sent
    pickpath = r'D:\pythonwork\code\paperparse\paper\papers\pickle'
    paperpath =  r'D:\pythonwork\code\paperparse\paper\papers'
    modelpath = r'D:\pythonwork\code\paperparse\paper\papers\model3_html'
    LabelSet = tjPaperIntroSentLabel.intro_sent

    include_absconc = True
    if include_absconc == True:
        filesuffix = '_2.pickle'
        savepicklepref  = 'xhtml_2'
    if include_absconc == False:
        filesuffix = '_3.pickle'
        savepicklepref  = 'xhtml_3'

  #  sentenceID,sentdictID =GetLabelSentID(LabelSet,pickpath,filesuffix)

    fname = pickpath + '\\'+savepicklepref+'intro_sent_id.pickle'
    sentenceID_2 = LoadSxptext(fname)
    fname = pickpath + '\\'+savepicklepref+'intro_sent_dict_id.pickle'

    sentenceID_2_dict = LoadSxptext(fname)

    for eachf,intro_set in sentenceID_2_dict.items():
        fn = eachf
        pickfname = pickpath + '\\'+ fn + filesuffix
        sxptxt = LoadSxptext(pickfname)
        print fn, intro_set # the first number in intro_set is the index of file in introduction_lable list in py file
        senttxt_set =[]
        for eachid in intro_set:
            senttxt_set.append(sxptxt.sentenceset[eachid].sentence_text)
        ProduceModelByPickle(modelpath, sxptxt,senttxt_set,fn)
def TestProduceOnlyIntroModel():
  #  LabelSet = sxpPaperIntroSentLabel.intro_sent
    pickpath = r'D:\pythonwork\code\paperparse\paper\papers\pickle'
    paperpath =  r'D:\pythonwork\code\paperparse\paper\papers'
    modelpath = r'D:\pythonwork\code\paperparse\paper\papers\model4_html'
    LabelSet = tjPaperIntroSentLabel.intro_sent

    include_absconc = True
    if include_absconc == True:
        filesuffix = '_2.pickle'
        savepicklepref  = 'xhtml_2'
    if include_absconc == False:
        filesuffix = '_3.pickle'
        savepicklepref  = 'xhtml_3'

  #  sentenceID,sentdictID =GetLabelSentID(LabelSet,pickpath,filesuffix)

    fname = pickpath + '\\'+savepicklepref+'intro_sent_id.pickle'
    sentenceID_2 = LoadSxptext(fname)
    fname = pickpath + '\\'+savepicklepref+'intro_sent_dict_id.pickle'

    sentenceID_2_dict = LoadSxptext(fname)

    for eachf,intro_set in sentenceID_2_dict.items():
        fn = eachf
        pickfname = pickpath + '\\'+ fn + filesuffix
        sxptxt = LoadSxptext(pickfname)
        print fn, intro_set # the first number in intro_set is the index of file in introduction_lable list in py file
        senttxt_set =[]
        for eachid in intro_set:
            senttxt_set.append(sxptxt.sentenceset[eachid].sentence_text)
        ProduceModelByPickle(modelpath, sxptxt,senttxt_set,fn)

def ProduceModelByPickle(modelpath,sxptxt,intro_set,fn):
##    absf = modelpath + '\\' + fn + '.A' + '.html'
##    conf =modelpath  +'\\' +  fn + '.B' + '.html'
##    abstract = ProduceModelFileByTxt(absf, fn + '.A', sxptxt.abstract )
##    conclusion = ProduceModelFileByTxt( conf, fn + '.B',sxptxt.conclusion )
    intrf =modelpath  +'\\' +  fn + '.A' + '.html'
    ProduceModelFileBySentSet(intrf, fn + '.A',intro_set)

def ProduceModelFileBySentSet(fname,fn,sentenceset):
    fcontent = MakeModel(sentenceset,fn, formatsent = 1)
    sxpReadFileMan.WriteStrFile(fname, fcontent, 'utf-8')
def ProduceModelFileByTxt(fname,fn,txt):
    sentenceset = re.split(r'\*\*\.',txt)
    fcontent = MakeModel(sentenceset,fn, formatsent = 1)
    sxpReadFileMan.WriteStrFile(fname, fcontent, 'utf-8')
    return fcontent
def MakeModel(sentenceset,fn, formatsent = 1):
        modeltxt  = '<html>\n<head>\n<title>%s</title>\n</head>\n'%(fn)
        i = 0
        abstract_str = ''
        for sent in sentenceset:
            rsent = RemoveUStrSpace(sent)
            if len(rsent)<=1:
                continue
            i = i + 1
            if formatsent == 1:
                sentr ='''<a name="%d">[%d]</a> <a href="#%d" id=%d>%s.</a>\n'''%(i,i,i,i,rsent)
                abstract_str = abstract_str +sentr
            if formatsent == 0:
                abstract_str = abstract_str +rsent + '\n'
        if formatsent == 1:
            bodytxt ='<body bgcolor="white">\n%s</body>\n</html>'%(abstract_str)
        if formatsent == 0:
            bodytxt = abstract_str
        if formatsent == 1:
            abstract_str = modeltxt + bodytxt
        if formatsent== 0:
            abstract_str = bodytxt

        return abstract_str
def RemoveUStrSpace(strtxt):
    patstr = r"u'\\u\w\w\w\w'"
    pattern = re.compile(patstr)
    nstr = pattern.sub('',strtxt)
    patstr = "\s+"
    pattern = re.compile(patstr)
    nstr = pattern.sub(' ',nstr)
    return nstr
def MakeModelSystem3Dir():
  #  LabelSet = sxpPaperIntroSentLabel.intro_sent
    pickpath = r'D:\pythonwork\code\paperparse\paper\papers\pickle'
    paperpath =  r'D:\pythonwork\code\paperparse\paper\papers'
    modelpath = r'D:\pythonwork\code\paperparse\paper\papers\model3_html'
    TargetSystempath = r'D:\pythonwork\code\paperparse\paper\papers\system3_html'
    LabelSet = tjPaperIntroSentLabel.intro_sent

    include_absconc = True
    if include_absconc == True:
        filesuffix = '_2.pickle'
        savepicklepref  = 'xhtml_2'
        SrcSystempath = r'D:\pythonwork\code\paperparse\paper\papers\system_html2'

    if include_absconc == False:
        filesuffix = '_3.pickle'
        savepicklepref  = 'xhtml_3'
        SrcSystempath = r'D:\pythonwork\code\paperparse\paper\papers\system_html3'

  #  sentenceID,sentdictID =GetLabelSentID(LabelSet,pickpath,filesuffix)

    fname = pickpath + '\\'+savepicklepref+'intro_sent_id.pickle'
    sentenceID_2 = LoadSxptext(fname)
    fname = pickpath + '\\'+savepicklepref+'intro_sent_dict_id.pickle'

    sentenceID_2_dict = LoadSxptext(fname)

    filelist,subdir = sxpReadFileMan.GetDir(SrcSystempath)
    print SrcSystempath
    print subdir
    print TargetSystempath
    for eachf,intro_set in sentenceID_2_dict.items():
        fn = eachf
        pickfname = pickpath + '\\'+ fn + filesuffix
        sxptxt = LoadSxptext(pickfname)
        print fn, intro_set # the first number in intro_set is the index of file in introduction_lable list in py file
        senttxt_set =[]
        for eachid in intro_set:
            senttxt_set.append(sxptxt.sentenceset[eachid].sentence_text)
   #     ProduceModelByPickle(modelpath, sxptxt,senttxt_set,fn)

        for eachdir in subdir:
            system_dir_sub = SrcSystempath + '\\' + eachdir
            srcfilelist,sd = sxpReadFileMan.GetDir(system_dir_sub)
            targsystemdirstr = TargetSystempath + '\\' + eachdir
            if os.path.exists(targsystemdirstr)==False:
                os.mkdir(targsystemdirstr)
                srcpath = targsystemdirstr
            for  srcf in srcfilelist:
                if srcf.lower().find(fn)>=0:
                    sf = system_dir_sub + '\\' + srcf
                    tf = targsystemdirstr + '\\' + srcf
                    win32file.CopyFile(sf,tf, 0)
                    break;
def MakeModelSystem4Dir():
  #  LabelSet = sxpPaperIntroSentLabel.intro_sent
    pickpath = r'D:\pythonwork\code\paperparse\paper\papers\pickle'
    paperpath =  r'D:\pythonwork\code\paperparse\paper\papers'
    modelpath = r'D:\pythonwork\code\paperparse\paper\papers\model4_html'
    TargetSystempath = r'D:\pythonwork\code\paperparse\paper\papers\system4_html'
    LabelSet = tjPaperIntroSentLabel.intro_sent

    include_absconc = True
    if include_absconc == True:
        filesuffix = '_2.pickle'
        savepicklepref  = 'xhtml_2'
        SrcSystempath = r'D:\pythonwork\code\paperparse\paper\papers\system_html2'

    if include_absconc == False:
        filesuffix = '_3.pickle'
        savepicklepref  = 'xhtml_3'
        SrcSystempath = r'D:\pythonwork\code\paperparse\paper\papers\system_html3'

  #  sentenceID,sentdictID =GetLabelSentID(LabelSet,pickpath,filesuffix)

    fname = pickpath + '\\'+savepicklepref+'intro_sent_id.pickle'
    sentenceID_2 = LoadSxptext(fname)
    fname = pickpath + '\\'+savepicklepref+'intro_sent_dict_id.pickle'

    sentenceID_2_dict = LoadSxptext(fname)

    filelist,subdir = sxpReadFileMan.GetDir(SrcSystempath)
    print SrcSystempath
    print subdir
    print TargetSystempath
    for eachf,intro_set in sentenceID_2_dict.items():
        fn = eachf
        pickfname = pickpath + '\\'+ fn + filesuffix
        sxptxt = LoadSxptext(pickfname)
        print fn, intro_set # the first number in intro_set is the index of file in introduction_lable list in py file
        senttxt_set =[]
        for eachid in intro_set:
            senttxt_set.append(sxptxt.sentenceset[eachid].sentence_text)
   #     ProduceModelByPickle(modelpath, sxptxt,senttxt_set,fn)

        for eachdir in subdir:
            system_dir_sub = SrcSystempath + '\\' + eachdir
            srcfilelist,sd = sxpReadFileMan.GetDir(system_dir_sub)
            targsystemdirstr = TargetSystempath #+ '\\' + eachdir
            if os.path.exists(targsystemdirstr)==False:
                os.mkdir(targsystemdirstr)
                srcpath = targsystemdirstr
            for  srcf in srcfilelist:
                if srcf.lower().find(fn)>=0:
                    sf = system_dir_sub + '\\' + srcf
                    tf = targsystemdirstr + '\\' + srcf + '.'+ eachdir
                    win32file.CopyFile(sf,tf, 0)
                    break;

def TestLabelSentID():
    pap = 1
    LabelSet = sxpPaperIntroSentLabel.intro_sent
    paplabel = LabelSet[pap][1:]
    papername = LabelSet[pap][0]
    fname = paperpath + '\\pickle\\'  + papername +  '_1.pickle'
    print fname
    sxptxt = LoadSxptext(fname)
    sxpSentset = sxptxt.sentenceset
    matchidset =[]
    for labelsent in paplabel:
        id = DeterminMatched(labelsent,sxpSentset)
        matchidset.append(id)
        if id >= 0:
            matchedsent = sxpSentset[id]
            print 'label:', labelsent
            print 'sent:',matchedsent.sentence_text
            print '********'
        else:
            print 'label:',labelsent
            print 'not found'
def TestTwoSentComp():
    sent = r' Resolving negation scope is a more difficult sub-problem at least in part because (unlike cue and event identification) it is concerned with much larger, non-local and often discontinuous parts of each utterance'
    papername = 'P14-1007.xhtml'
    fname = paperpath + '\\pickle\\'  + papername +  '_1.pickle'
    print fname
    sxptxt = LoadSxptext(fname)
    sxpSentset = sxptxt.sentenceset
    dists =[]
    for sxpsent in sxpSentset:
        st = sxpsent.sentence_text
        dist = CalcuDistTwoSent(sent, st)
        dists.append(dist[0]*dist[1])
    d = max(dists)
    id = dists.index(d)
    print d,id
    print sent
    print sxpSentset[id].sentence_text
##    for es in sxpSentset:
##        print es.sentence_text
def TestTwo():
    sent = r' Resolving negation scope is a more difficult sub-problem at least in part because (unlike cue and event identification) it is concerned with much larger, non-local and often discontinuous parts of each utterance'
    sent1 = '''
    2 2 Resolving negation scope is a more difficult sub-problem at least in part because (unlike cue and event identification) it is concerned with much larger, non-local and often discontinuous parts of each utterance
    '''
    sent2 ='''
    Furthermore, we have benefited from comments by participants of the 2013 DELPH-IN Summit, in particular Joshua Crowgey, Guy Emerson, Glenn Slayden, Sanghoun Song, and Rui Wang
    '''

    dist1,ph1 = CalcuDistTwoSent(sent, sent1)
    dist2,ph2 =CalcuDistTwoSent(sent, sent2)
    print dist1,ph1
    print dist2,ph2

def main():
    #TestTwoSent()
    #TestCompareTwoSent()

    #TestTwoSentComp()
    #TestTwo()
    #TestLabelSentID()
  #  TestIntroLabelID() #the latest one 2016-03-29
   # DisplayID()
  #  TestProduceIntroModel() # the latest one in 2016-03-29
  #  TestProduceOnlyIntroModel()
    #MakeModelSystem3Dir()
    MakeModelSystem4Dir()
if __name__ == '__main__':
    main()
