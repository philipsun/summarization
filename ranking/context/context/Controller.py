__author__ = 'a'
import os
import re
from sxpPackage import *
from MyModel import *
from View import *
from tf_idf import *
from graph_base import GraphBased
from word_graph import WordGraph
from sxpContextModel import conTextModel
import sxpReadFileMan
from MySecModel import *
from MySecContextModel import *
from sxpHybridGraph import *
from MySecTitleNetwork import *
from MyWordGraph import *
def IsSubparasecStepModel(modeltype):
    pat=r"sp(\d+)"
    pt = re.compile(pat)
    match= pt.match(modeltype)
    if match:
         return int(match.groups(0)[0])
    else:
        return None
def IsSimStepModel(modeltype):
    pat=r"sim(\d+)"
    pt = re.compile(pat)
    match= pt.match(modeltype)
    if match:
         return int(match.groups(0)[0])
    else:
        return None
def run_one_rankmodel(pickle_path,pk_sys_set,system_path,system_id,modeltype='para',rankpara='',remove_stopwords=1):
    print modeltype, rankpara
    i = 1
    remove_stopwords=1 #using stopwords, keep those stop words, do not remove those stop words.
    remove_stopwords=0 #do not using stopwords, remove those stop words
    remove_stopwords=rankpara['remove_stopwords']
    useabstr = rankpara[u'useabstr']
    maxword = rankpara[u'maxword']
    strictmax =rankpara[u'strictmax']
    topksent = rankpara[u'topksent']

    for file_name,system_name in pk_sys_set:
##        if file_name.lower() not in labeled_data.keys():
##            continue
        topksent_path = system_path + '\\' + system_name + '.'+system_id

        pickle_file = os.path.join(pickle_path,file_name)
        print i, file_name
        if modeltype == 'para':
            model = MyModel(pickle_file,remove_stopwords=remove_stopwords)
        if modeltype == 'tfidf':
            model = TfIdf(pickle_file,remove_stopwords=remove_stopwords) #no code for stopwords yet
        if modeltype == 'simgraph':
            model = GraphBased(pickle_file,remove_stopwords=remove_stopwords) #no code for stopwords yet
        if modeltype == 'wordgraph':
            model = WordGraph(pickle_file,remove_stopwords=remove_stopwords) #no code for stopwords yet
        if modeltype == 'subpara':
            model = conTextModel(pickle_file,remove_stopwords=remove_stopwords)
        if modeltype == 'parasec':
            model = MySecModel(pickle_file,remove_stopwords=remove_stopwords)
        if modeltype == 'subparasec':
            model = SecConTextModel(pickle_file,remove_stopwords=remove_stopwords)
        if modeltype == 'hybrid':
            model = HybridGraph(pickle_file,remove_stopwords=remove_stopwords)
        if modeltype == 'sectitle':
            model = MySecTitleModel(pickle_file,remove_stopwords=remove_stopwords)
        if modeltype == 'mywordgraph':
            model = MyWordGraph(pickle_file,remove_stopwords=remove_stopwords) #no code for stopwords yet
        isSubPara= IsSubparasecStepModel(modeltype)
        if isSubPara:
           useabstr = 0
           maxword = -1
           strictmax =0
           topksent = isSubPara
           model = SecConTextModel(pickle_file,remove_stopwords=remove_stopwords)
        isSimLen= IsSimStepModel(modeltype)
        if isSimLen:
           useabstr = 0
           maxword = -1
           strictmax =0
           topksent = isSubPara
           borrow_allsent_path = os.path.join(rankpara['borrow_allsent_path'],system_name + '.'+rankpara['borrow_system_id'])
           borrow_allpkfname = borrow_allsent_path + 'allsent.pk'
           allsent = sxpReadFileMan.LoadSxptext(borrow_allpkfname)
           tops=allsent[0:isSimLen]
           st = ProduceSystem(tops,file_name,1)
    ##        for eachs in tops:
    ###            print st
    ##            st = st + eachs + '. \n'
           topsent_pk_file=topksent_path + 'topsent.pk'
           sxpReadFileMan.StoreSxptext(tops,topsent_pk_file)

           sxpReadFileMan.WriteStrFile(topksent_path,st, 'utf-8')
           pkfname = topksent_path + 'allsent.pk'
           sxpReadFileMan.StoreSxptext(allsent,pkfname)

           print 'result is ok'
           i = i + 1
           continue
          # model = GraphBased(pickle_file,remove_stopwords=remove_stopwords)
        #save text ranked sentences to text
##        tops = model.OutPutTopKSent(topksent,1,-1)
##        useabstr = 0
##        maxword = 100
##        strictmax =1


        #tops = model.OutPutTopKSent(topksent,useabstr,maxword,strictmax)
        tops = OutPutTopKSent(model,topksent,useabstr,maxword,strictmax)
        print len(tops)
        st = ProduceSystem(tops,file_name,1)
##        for eachs in tops:
###            print st
##            st = st + eachs + '. \n'
        sxpReadFileMan.WriteStrFile(topksent_path,st, 'utf-8')

        topsent_pk_file=topksent_path + 'topsent.pk'
        sxpReadFileMan.StoreSxptext(tops,topsent_pk_file)

        allsent = model.OutputAllRankSentence()
        pkfname = topksent_path + 'allsent.pk'
        sxpReadFileMan.StoreSxptext(allsent,pkfname)
        #save text abstact text and conclusion text

        i = i + 1

    print "result is ok"
def OutPutTopKSent(model,topksent,useabstr = 1,maxwords = -1,strictmax=0):
        ranked_sentences = [model.text.sentenceset[model.idx_s[i, 0]]
                            for i in range(len(model.text.sentenceset))]
        sent_txt_set = []
        i = 0
        if useabstr == 0:
            if maxwords==-1:
                usetopk = True;
            else:
                usetopk = False
        if useabstr == 1:
            abstractlen = len(model.text.abstract.split(' '))
            maxwords = abstractlen
            usetopk = False

        if useabstr == 2:
            abstractlen = len(model.text.conclusion.split(' '))
            maxwords = abstractlen
            usetopk = False
        wordlen = 0
        print 'use abs:',useabstr,'use topk:', usetopk,topksent, 'set maxword:',maxwords
        for sentence in ranked_sentences:
            if len(sentence.sentence_text)<=1:
                 continue
            words = sentence.sentence_text.split(' ')
            wl = len(words)
            if usetopk:
                if i>=topksent:
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
def run_one_rankmodel_duc(pickle_path,pk_sys_set,system_path,system_id,modeltype='para',rankpara=''):
    print modeltype, rankpara
    i = 1
    for file_name,system_name in pk_sys_set:
##        if file_name.lower() not in labeled_data.keys():
##            continue
        pickle_file = os.path.join(pickle_path,file_name)
        print i, file_name
        if modeltype == 'para':
            model = MyModel(pickle_file)
        if modeltype == 'tfidf':
            model = TfIdf(pickle_file)
        if modeltype == 'simgraph':
            model = GraphBased(pickle_file)
        if modeltype == 'wordgraph':
            model = WordGraph(pickle_file)
        if modeltype == 'subpara':
            model = conTextModel(pickle_file)
        if modeltype == 'parasec':
            model = MySecModel(pickle_file)
        if modeltype == 'subparasec':
            model = SecConTextModel(pickle_file)
        if modeltype == 'hybrid':
            model = HybridGraph(pickle_file)
        if modeltype == 'sectitle':
            model = MySecTitleModel(pickle_file)
        if modeltype == 'mywordgraph':
            model = MyWordGraph(pickle_file)

        #save text ranked sentences to text
        topksent_path = system_path + '\\' + system_name + '.'+system_id
##        maxword= 100
##        useabstr = 0
##        strictmax=1
##        topksent=5
##        useabstr = 0
##        strictmax = 0
##        maxword = -1

        useabstr = rankpara[u'useabstr']
        maxword = rankpara[u'maxword']
        strictmax =rankpara[u'strictmax']
        topksent = rankpara[u'topksent']
        if useabstr>=1:
            useabstr=0
            maxword = 100
        tops = model.OutPutTopKSent(topksent,useabstr,maxword,strictmax)
        print len(tops)
#        print tops
#        tops = model.OutPutTopKSent(topksent,1,-1)
        st = ProduceSystem(tops,file_name,1)
#        print st
##        for eachs in tops:
###            print st
##            st = st + eachs + '. \n'
        sxpReadFileMan.WriteStrFile(topksent_path,st, 'utf-8')

        allsent = model.OutputAllRankSentence()
        pkfname = topksent_path + 'allsent.pk'
        sxpReadFileMan.StoreSxptext(allsent,pkfname)
        #save text abstact text and conclusion text

        i = i + 1

    print "result is ok"

def GetDirFileList(filedir):
    if not os.path.exists(filedir):
        print 'no dir to be read'
        return []
    filelist = []
    files = os.listdir(filedir)
    #now we first read each file in the txtPath
    for f in files:
      if os.path.isdir(os.path.join(filedir, f)):
         pass
      else:
         filelist.append(f)
    return filelist

def ProduceSystem(tops, fn, formatsent = 0):
        modeltxt  = '''<html>\n<head>\n<title>%s</title>\n</head>\n'''%(fn)
        sentenceset = tops
        i = 0
        abstract_str = ''
        for sent in sentenceset:
            rsent = RemoveUStrSpace(sent)
            if len(rsent)<=0:
                rsent = 'test sentence is empty'
            i = i + 1
            if formatsent == 1:
                sentr ='''<a name="%d">[%d]</a> <a href="#%d" id=%d>%s.</a>\n'''%(i,i,i,i,rsent)
            if formatsent == 0:
                sentr = rsent + '\n'
            abstract_str = abstract_str +sentr
        if formatsent == 1:
            bodytxt = '''<body bgcolor="white">\n%s</body>\n</html>'''%(abstract_str)
        if formatsent == 0:
            bodytxt = abstract_str

        if formatsent== 0:
            abstract_str = bodytxt
        if formatsent == 1:
            abstract_str = modeltxt + bodytxt

        return abstract_str

def RemoveUStr(strtxt):
    patstr = r"u'\\u\w\w\w\w'"
    pattern = re.compile(patstr)
    nstr = pattern.sub('',strtxt)
##    patstr = "\s"
##    pattern = re.compile(patstr)
##    nstr = pattern.sub(' ',nstr)
    return nstr
def RemoveUStrSpace(strtxt):
    patstr = r"u'\\u\w\w\w\w'"
    pattern = re.compile(patstr)
    nstr = pattern.sub('',strtxt)
    patstr = "\s+"
    pattern = re.compile(patstr)
    nstr = pattern.sub(' ',nstr)
    return nstr
def Test():
    print IsSimStepModel('sim2')
if __name__ == '__main__':
    Test()
