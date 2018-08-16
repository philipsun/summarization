#-------------------------------------------------------------------------------
# Name:        sxpRougeConfig
# Purpose:
#
# Author:      sunxp
#
# Created:     04/05/2017
# Copyright:   (c) sunxp 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#code=utf-8
import sxpReadFileMan
import sxpParseRougeScore
import os
import numpy as np
import xlrd
import xlsxwriter

#anthology.aclweb.org/P/P14/P14-2052.pdf for Single Document Summarization based on Nested Tree Structure
dataroot = r'E:\pythonwork\code\paperparse\paper'
if os.path.exists(dataroot)==False:
    dataroot = r'E:\pythonworknew\code\paperparse\paper'
resultdir = r'L:\pythonworknew\tjrank_sentences\context\result'
if os.path.exists(resultdir)==False:
    resultdir = r'E:\pythonworknew\code\tjrank_sentences\context\result'
idname = {'para':'01',
    'tfidf':'02',
    'simgraph':'03',
    'wordgraph':'04',
    'subpara':'05',
    'parasec':'06',
    'subparasec':'07',
    'hybrid':'08',
    'sectitle':'09',
    'mywordgraph':'10',
    'sp1':'11',
    'sp3':'12',
    'sp5':'13',
    'sp7':'14',
    'sp9':'15',
    'sp11':'16',
    'sp13':'17',
    'sim1':'18',
    'sim3':'19',
    'sim5':'20',
    'sim7':'21',
    'sim9':'22',
    'sim11':'23',
    'sim13':'24'
}
def GetNameID():
    return idname
def GetModelNameDict():
    modlename={}
    for eachkey in idname.keys():
        idstr = idname[eachkey]
        modlename[idstr]=eachkey
    return modlename
def GetModelName(idname):
    modlename={}
    for eachkey in idname.keys():
        idstr = idname[eachkey]
        modlename[idstr]=eachkey
    return modlename
modename_dict=GetModelName(idname)

def duc_withstop_max100(rankthem =0,rougethem = 0):

    rankpara={
        u'idname':idname,
        u'useabstr':0,
        u'maxword' : 100,
        u'strictmax': 1,
        u'topksent': 5,
        u'outdir': os.path.join(resultdir,'duc_withstop_max100'),#r'E:\pythonworknew\code\tjrank_sentences\context\result\r4',
        u'rougetxthead':'duc_withstop_max100',
        u'model_test':['para','tfidf','simgraph','wordgraph','subpara','hybrid','mywordgraph'],
        u'plotwho':'duc',
      # u'model_test':['mywordgraph']
##        "pickle_path" : os.path.join(dataroot,r'papers\duc\txt\pickle')
##        "model_path":  os.path.join(dataroot,r'papers\duc\txt\model_html')
##        "system_path" = os.path.join(dataroot,r'papers\duc\txt\system_html1')
        u'dataroot':dataroot,
        u"pickle_path" : os.path.join(dataroot,r'duc\pickle'),
        u"model_path":  os.path.join(dataroot,r'duc\model_html'),
        u"system_path" : os.path.join(dataroot,r'duc\duc_withstop_max100'),
        u'modelpattern': r'D\d\d\d.P.100.[A-Z].[A-Z].#ID#.html',
        u'systempattern': r'^(\w+-\w+).html',
        u'model_filenames_pattern_id' : r'D\d\d\d.P.100.[A-Z].[A-Z].(\w+-\w+).html',
        u'system_filename_pattern_id' : r'#ID#.html',
        u'pickle_file_pattern_id' :r'#ID#', # inc_test
        u'remove_stopwords':0, #1 for filter out stopers, 0 for not filter out stopwords,

    }
    return rankpara
def duc_withoutstop_max100(rankthem =0,rougethem = 0):
    rankpara={
        u'idname':idname,
        u'useabstr':0,
        u'maxword' : 100,
        u'strictmax': 1,
        u'topksent': 5,
        u'outdir': os.path.join(resultdir,'duc_withoutstop_max100'),#r'E:\pythonworknew\code\tjrank_sentences\context\result\r3smax100',
        u'rougetxthead':'duc_withoutstop_max100',
        u'model_test':['para','tfidf','simgraph','wordgraph','subpara','hybrid','mywordgraph'],
        u'plotwho':'duc',
       # u'model_test':['mywordgraph']
##        "pickle_path" : os.path.join(dataroot,r'papers\duc\txt\pickle')
##        "model_path":  os.path.join(dataroot,r'papers\duc\txt\model_html')
##        "system_path" = os.path.join(dataroot,r'papers\duc\txt\system_html1')
        u'dataroot':dataroot,
        u"pickle_path" : os.path.join(dataroot,r'duc\pickle'),
        u"model_path" : os.path.join(dataroot,r'duc\model_html'),
        u"system_path" : os.path.join(dataroot,r'duc\duc_withoutstop_max100'),
        u'modelpattern': r'D\d\d\d.P.100.[A-Z].[A-Z].#ID#.html',
        u'systempattern': r'^(\w+-\w+).html',

        u'model_filenames_pattern_id' : r'D\d\d\d.P.100.[A-Z].[A-Z].(\w+-\w+).html',
        u'system_filename_pattern_id' : r'#ID#.html',
        u'pickle_file_pattern_id' :r'#ID#', # inc_test
        u'remove_stopwords':1 #1 for filter out stopers, 0 for not filter out stopwords,
    }
    return rankpara
def duc_withoutstop_topk(rankthem =0,rougethem = 0):
    rankpara={
        u'idname':idname,
        u'useabstr':0,
        u'maxword' : -1,
        u'strictmax': 0,
        u'topksent': 5,
        u'outdir': os.path.join(resultdir,'duc_withoutstop_topk'),#r'E:\pythonworknew\code\tjrank_sentences\context\result\r3',
        u'rougetxthead':'duc_withoutstop_topk',
        u'model_test':['para','tfidf','simgraph','wordgraph','subpara','hybrid','mywordgraph'],
        u'plotwho':'duc',

       # u'model_test':['mywordgraph']
##        "pickle_path" : os.path.join(dataroot,r'papers\duc\txt\pickle')
##        "model_path":  os.path.join(dataroot,r'papers\duc\txt\model_html')
##        "system_path" = os.path.join(dataroot,r'papers\duc\txt\system_html2')
        u'dataroot':dataroot,
        u"pickle_path" : os.path.join(dataroot, r'duc\txt\pickle'),
        u"model_path": os.path.join(dataroot,  r'duc\txt\model_html'),
        u"system_path" : os.path.join(dataroot, r'duc\duc_withoutstop_topk'),
        u'modelpattern': r'D\d\d\d.P.100.[A-Z].[A-Z].#ID#.html',
        u'systempattern': r'^(\w+-\w+).html',
        u'model_filenames_pattern_id' : r'D\d\d\d.P.100.[A-Z].[A-Z].(\w+-\w+).html',
        u'system_filename_pattern_id' : r'#ID#.html',
        u'pickle_file_pattern_id' :r'#ID#', # inc_test
        u'remove_stopwords':1 #1 for filter out stopers, 2 for not filter out stopwords,
    }
    return rankpara
def duc_withstop_topk(rankthem =0,rougethem = 0):
    rankpara={
        u'idname':idname,
        u'useabstr':0,
        u'maxword' : -1,
        u'strictmax': 0,
        u'topksent': 5,
        u'outdir': os.path.join(resultdir,'duc_withstop_topk'),#r'E:\pythonworknew\code\tjrank_sentences\context\result\r3',
        u'rougetxthead':'duc_withstop_topk',
        u'model_test':['para','tfidf','simgraph','wordgraph','subpara','hybrid','mywordgraph'],
        u'plotwho':'duc',

       # u'model_test':['mywordgraph']
##        "pickle_path" : os.path.join(dataroot,r'papers\duc\txt\pickle')
##        "model_path":  os.path.join(dataroot,r'papers\duc\txt\model_html')
##        "system_path" = os.path.join(dataroot,r'papers\duc\txt\system_html1')
        u'dataroot':dataroot,
        u"pickle_path" : os.path.join(dataroot, r'duc\txt\pickle'),
        u"model_path": os.path.join(dataroot,  r'duc\model_html'),
        u"system_path" : os.path.join(dataroot, r'duc\duc_withstop_topk'),
        u'modelpattern': r'D\d\d\d.P.100.[A-Z].[A-Z].#ID#.html',
        u'systempattern': r'^(\w+-\w+).html',
        u'model_filenames_pattern_id' : r'D\d\d\d.P.100.[A-Z].[A-Z].(\w+-\w+).html',
        u'system_filename_pattern_id' : r'#ID#.html',
        u'pickle_file_pattern_id' :r'#ID#', # inc_test
        u'remove_stopwords':0 #1 for filter out stopers, 2 for not filter out stopwords,
    }
    return rankpara
def acl_exc_withstop_max100(rankthem =0,rougethem = 0):
    rankpara={

        u'idname':idname,
        u'useabstr':0,
        u'maxword' : 100,
        u'strictmax': 1,
        u'topksent': 5,
        u'outdir': os.path.join(resultdir,'acl_exc_withstop_max100'),#r'E:\pythonworknew\code\tjrank_sentences\context\result\r4',
        u'rougetxthead':'exc_abs',
        u'plotwho':'acl_exc',
        u'model_test':['para','tfidf','simgraph','wordgraph','subpara','parasec','subparasec','hybrid','sectitle','mywordgraph'],
   #     u'model_test':['para','hybrid','sectitle','mywordgraph']
        u'dataroot':dataroot,
        u"pickle_path" : os.path.join(dataroot,  r'papers\pickle'),
        u"model_path": os.path.join(dataroot,   r'papers\model_html'),
        u"system_path" : os.path.join(dataroot,  r'papers\acl_exc_withstop_max100'),
        u'modelpattern':  r'P14-#ID#.xhtml.[A-Z].html',
        u"systempattern" : r'^P14-(\d+).xhtml.html', #note that in real dir, .0[1-7] is appended to the systempattern for the model id
        u'model_filenames_pattern_id' : r'P14-(\d+).xhtml.[A-Z].html',
        u'system_filename_pattern_id' : r'P14-#ID#.xhtml.html',
        u'pickle_file_pattern_id' :r'P14-#ID#.xhtml_3.pickle', # inc_test
        u'remove_stopwords':0 #1 for filter out stopers, 2 for not filter out stopwords

    }
    return rankpara
def acl_exc_withoutstop_max100(rankthem =0,rougethem = 0):
    rankpara={
        u'idname':idname,
        u'dataroot':dataroot,
        u'useabstr':0,
        u'maxword' : 100,
        u'strictmax': 1,
        u'topksent': 5,
        u'outdir': os.path.join(resultdir,'acl_exc_withoutstop_max100'),#r'E:\pythonworknew\code\tjrank_sentences\context\result\r3smax100',
        u'rougetxthead':'exc_abs',
        u'plotwho':'acl_exc',
        u'model_test':['para','tfidf','simgraph','wordgraph','subpara','parasec','subparasec','hybrid','sectitle','mywordgraph'],
   #     u'model_test':['para','hybrid','sectitle','mywordgraph']
        u'dataroot':dataroot,
        u"pickle_path" : os.path.join(dataroot,  r'papers\pickle'),
        u"model_path": os.path.join(dataroot,  r'papers\model_html'),
        u"system_path" : os.path.join(dataroot,  r'papers\acl_exc_withoutstop_max100'),
        u'modelpattern':  r'P14-#ID#.xhtml.[A-Z].html',
        u"systempattern" : r'^P14-(\d+).xhtml.html', #note that in real dir, .0[1-7] is appended to the systempattern for the model id
        u'model_filenames_pattern_id' : r'P14-(\d+).xhtml.[A-Z].html',
        u'system_filename_pattern_id' : r'P14-#ID#.xhtml.html',
        u'pickle_file_pattern_id' :r'P14-#ID#.xhtml_3.pickle', # inc_test
        u'remove_stopwords':1 #1 for filter out stopers, 2 for not filter out stopwords

    }
    return rankpara
def acl_exc_withoutstop_topk(rankthem =0,rougethem = 0):
    rankpara={

        u'idname':idname,
        u'useabstr':0,
        u'maxword' : -1,
        u'strictmax': 1,
        u'topksent': 5,
        u'outdir': os.path.join(resultdir,'acl_exc_withoutstop_topk'),#r'E:\pythonworknew\code\tjrank_sentences\context\result\r3',
        u'rougetxthead':'exc_abs',
        u'plotwho':'acl_exc',
        u'model_test':['para','tfidf','simgraph','wordgraph','subpara','parasec','subparasec','hybrid','sectitle','mywordgraph'],
   #     u'model_test':['para','hybrid','sectitle','mywordgraph']
        u'dataroot':dataroot,
        u"pickle_path" : os.path.join(dataroot,  r'papers\pickle'),
        u"model_path" : os.path.join(dataroot,  r'papers\model_html'),
        u"system_path" : os.path.join(dataroot,  r'papers\acl_exc_withoutstop_topk'),
        u'modelpattern':  r'P14-#ID#.xhtml.[A-Z].html',
        u"systempattern" : r'^P14-(\d+).xhtml.html', #note that in real dir, .0[1-7] is appended to the systempattern for the model id
        u'model_filenames_pattern_id' : r'P14-(\d+).xhtml.[A-Z].html',
        u'system_filename_pattern_id' : r'P14-#ID#.xhtml.html',
        u'pickle_file_pattern_id' :r'P14-#ID#.xhtml_3.pickle', # inc_test
        u'remove_stopwords':1  #1 for filter out stopers, 2 for not filter out stopwords

    }
    return rankpara
def acl_inc_withstop_max100(rankthem =0,rougethem = 0):
    rankpara={

        u'idname':idname,
        u'useabstr':0,
        u'maxword' : 100,
        u'strictmax': 1,
        u'topksent': 5,
        u'outdir': os.path.join(resultdir,'acl_inc_withstop_max100'),#r'E:\pythonworknew\code\tjrank_sentences\context\result\r4',
        u'rougetxthead':'inc_abs',
        u'plotwho':'acl_inc',
        u'model_test':['para','tfidf','simgraph','wordgraph','subpara','parasec','subparasec','hybrid','sectitle','mywordgraph'],
   #     u'model_test':['para','hybrid','sectitle','mywordgraph']
        u'dataroot':dataroot,
        u"pickle_path":os.path.join(dataroot,  r'papers\pickle'),
        u"model_path":os.path.join(dataroot,  r'papers\model_html'),
        u"system_path":os.path.join(dataroot,  r'papers\acl_inc_withstop_max100'),
        u'modelpattern':  r'P14-#ID#.xhtml.[A-Z].html',
        u"systempattern" : r'^P14-(\d+).xhtml.html', #note that in real dir, .0[1-7] is appended to the systempattern for the model id

        u'model_filenames_pattern_id' : r'P14-(\d+).xhtml.[A-Z].html',
        u'system_filename_pattern_id' : r'P14-#ID#.xhtml.html',
        u'pickle_file_pattern_id' :r'P14-#ID#.xhtml_2.pickle', # inc_test

        u'remove_stopwords':0 #1 for use, 2 for not use
##    pickle_path = os.path.join(dataroot,r'papers\pickle')
##    model_path =  os.path.join(dataroot,r'papers\model_html')
##    system_path = os.path.join(dataroot,r'papers\system_html5')
    }
    return rankpara
def acl_inc_withoutstop_max100(rankthem =0,rougethem = 0):
    rankpara={

        u'idname':idname,
        u'useabstr':0,
        u'maxword' : 100,
        u'strictmax': 1,
        u'topksent': 5,
        u'outdir': os.path.join(resultdir,'acl_inc_withoutstop_max100'),#r'E:\pythonworknew\code\tjrank_sentences\context\result\r3smax100',
        u'rougetxthead':'inc_abs',
        u'plotwho':'acl_inc',
        u'model_test':['para','tfidf','simgraph','wordgraph','subpara','parasec','subparasec','hybrid','sectitle','mywordgraph'],
   #     u'model_test':['para','hybrid','sectitle','mywordgraph']
        u'dataroot':dataroot,
        u"pickle_path" :os.path.join(dataroot,  r'papers\pickle'),
        u"model_path":os.path.join(dataroot,  r'papers\model_html'),
        u"system_path" :os.path.join(dataroot,  r'papers\acl_inc_withoutstop_max100'),
        u'modelpattern':  r'P14-#ID#.xhtml.[A-Z].html',
        u"systempattern" : r'^P14-(\d+).xhtml.html', #note that in real dir, .0[1-7] is appended to the systempattern for the model id

        u'model_filenames_pattern_id' : r'P14-(\d+).xhtml.[A-Z].html',
        u'system_filename_pattern_id' : r'P14-#ID#.xhtml.html',
        u'pickle_file_pattern_id' :r'P14-#ID#.xhtml_2.pickle', # inc_test

        u'remove_stopwords':1 #1 for use, 2 for not use
##    pickle_path = os.path.join(dataroot,r'papers\pickle')
##    model_path =  os.path.join(dataroot,r'papers\model_html')
##    system_path = os.path.join(dataroot,r'papers\system_html5')
    }
    return rankpara
def acl_inc_withoutstop_topk(rankthem =0,rougethem = 0):
    rankpara={

        u'idname':idname,
        u'useabstr':0,
        u'maxword' : -1,
        u'strictmax': 1,
        u'topksent': 5,
        u'outdir': os.path.join(resultdir,'acl_inc_withoutstop_topk'),#r'E:\pythonworknew\code\tjrank_sentences\context\result\r3',
        u'rougetxthead':'inc_abs',
        u'plotwho':'acl_inc',
        u'model_test':['para','tfidf','simgraph','wordgraph','subpara','parasec','subparasec','hybrid','sectitle','mywordgraph'],
   #     u'model_test':['para','hybrid','sectitle','mywordgraph']
        u'dataroot':dataroot,
        u"pickle_path" :os.path.join(dataroot,  r'papers\pickle'),
        u"model_path" :os.path.join(dataroot,  r'papers\model_html'),
        u"system_path" :os.path.join(dataroot,  r'papers\acl_inc_withoutstop_topk'),
        u'modelpattern':  r'P14-#ID#.xhtml.[A-Z].html',
        u"systempattern" : r'^P14-(\d+).xhtml.html', #note that in real dir, .0[1-7] is appended to the systempattern for the model id

        u'model_filenames_pattern_id' : r'P14-(\d+).xhtml.[A-Z].html',
        u'system_filename_pattern_id' : r'P14-#ID#.xhtml.html',
        u'pickle_file_pattern_id' :r'P14-#ID#.xhtml_2.pickle', # inc_test

        u'remove_stopwords':1 #1 for use, 2 for not use
##    pickle_path = os.path.join(dataroot,r'papers\pickle')
##    model_path =  os.path.join(dataroot,r'papers\model_html')
##    system_path = os.path.join(dataroot,r'papers\system_html5')
    }
    return rankpara
def single_withoutstop(rankthem =0,rougethem = 0):
    rankpara={

        u'idname':idname,
        u'useabstr':1,
        u'maxword' : 100,
        u'strictmax': 0,
        u'topksent': 5,
        u'outdir': os.path.join(resultdir,'single_withoutstop'),#r'E:\pythonworknew\code\tjrank_sentences\context\result\rsinglewithoutstopword',
        u'rougetxthead':'single_inc',
        u'plotwho':'single_inc',
        u'model_test':['para','tfidf','simgraph','wordgraph','subpara','parasec','subparasec','hybrid','sectitle','mywordgraph'],
        u'dataroot':dataroot,
        u"pickle_path" :os.path.join(dataroot,  r'single\pk'),
        u"model_path" :os.path.join(dataroot,  r'single\model'),
        u"system_path" :os.path.join(dataroot,  r'single\single_withoutstop'),
        u'modelpattern':  r'testdimension_#ID#.txt.pk.[A-Z].html',
        u"systempattern" : r'testdimension_(\d+).txt', #note that in real dir, .0[1-7] is appended to the systempattern for the model id

        u'system_filename_pattern_id' : r'testdimension_#ID#.txt',
        u'pickle_file_pattern_id':r'testdimension_#ID#.txt.pk', # inc_test

        u'model_filenames_pattern_id' : r'testdimension_(\d+).txt.pk.[A-Z].html',

        u'keyword_bench_path':os.path.join(dataroot,  r'single\keyword'),

        u'remove_stopwords':1, #1 for use, 2 for not use
        u'keyword_path':os.path.join(dataroot,r'single\keyword')
        }
    return rankpara
##    pickle_path = os.path.join(dataroot,r'papers\pickle')
##    model_path =  os.path.join(dataroot,r'papers\model_html')
##    system_path = os.path.join(dataroot,r'papers\system_html5')
def single_withstop():
    rankpara={

        u'idname':idname,
        u'useabstr':1,
        u'maxword' : 100,
        u'strictmax': 0,
        u'topksent': 5,
        u'outdir': os.path.join(resultdir,'single_withstop'),#r'E:\pythonworknew\code\tjrank_sentences\context\result\rsinglestopword',
        u'rougetxthead':'single_inc',
        u'plotwho':'single_inc',
        u'model_test':['para','tfidf','simgraph','wordgraph','subpara','parasec','subparasec','hybrid','sectitle','mywordgraph'],
   #     u'model_test':['para','hybrid','sectitle','mywordgraph']
        u'dataroot':dataroot,
        u"pickle_path" :os.path.join(dataroot,  r'single\pk'),
        u"model_path" :os.path.join(dataroot,  r'single\model'),
        u"system_path" :os.path.join(dataroot,  r'single\single_withstop'),
        u'modelpattern':  r'testdimension_#ID#.txt.pk.[A-Z].html',
        u"systempattern" : r'testdimension_(\d+).txt', #note that in real dir, .0[1-7] is appended to the systempattern for the model id

        u'model_filenames_pattern_id' : r'testdimension_(\d+).txt.pk.[A-Z]',
        u'system_filename_pattern_id' : r'testdimension_#ID#.txt',
        u'pickle_file_pattern_id' :r'testdimension_#ID#.txt.pk', # inc_test
        u'remove_stopwords':0 #1 for use, 2 for not use
    }
    return rankpara
def single_withoutstop_steplen():
    rankpara={

        u'idname':idname,
        u'useabstr':1,
        u'maxword' : 100,
        u'strictmax': 0,
        u'topksent': 5,
        u'outdir': os.path.join(resultdir,'single_withoutstop_steplen'),#r'E:\pythonworknew\code\tjrank_sentences\context\result\rsinglewithoutstopword',
        u'rougetxthead':'single_inc',
        u'plotwho':'single_inc',
        u'model_test':['sp1','sp3','sp5','sp7','sp9','sp11','sp13','subpara'],
        u'dataroot':dataroot,
        u"pickle_path" :os.path.join(dataroot,  r'single\pk'),
        u"model_path" :os.path.join(dataroot,  r'single\model'),
        u"system_path" :os.path.join(dataroot,  r'single\single_withoutstop_steplen'),
        u'modelpattern':  r'testdimension_#ID#.txt.pk.[A-Z].html',
        u"systempattern" : r'testdimension_(\d+).txt', #note that in real dir, .0[1-7] is appended to the systempattern for the model id

        u'system_filename_pattern_id' : r'testdimension_#ID#.txt',
        u'pickle_file_pattern_id':r'testdimension_#ID#.txt.pk', # inc_test

        u'model_filenames_pattern_id' : r'testdimension_(\d+).txt.pk.[A-Z].html',

        u'keyword_bench_path':os.path.join(dataroot,  r'single\keyword'),

        u'remove_stopwords':1, #1 for use, 2 for not use
        u'keyword_path':os.path.join(dataroot,r'single\keyword')
        }
    return rankpara
def single_withoutstop_steplen_sim():
    rankpara={

        u'idname':idname,
        u'useabstr':1,
        u'maxword' : 100,
        u'strictmax': 0,
        u'topksent': 5,
        u'outdir': os.path.join(resultdir,'single_withoutstop_steplen_sim'),#r'E:\pythonworknew\code\tjrank_sentences\context\result\rsinglewithoutstopword',
        u'rougetxthead':'single_inc',
        u'plotwho':'single_inc',
#        u'model_test':['sim1','sim3','sim5','sp7','sim9','sim11','sim13','simgraph'],
        u'model_test':['sim1','sim3','sim5','sim7','sim9','sim11','sim13','simgraph'],
        u'dataroot':dataroot,
        u"pickle_path" :os.path.join(dataroot,  r'single\pk'),
        u"model_path" :os.path.join(dataroot,  r'single\model'),
        u"system_path" :os.path.join(dataroot,  r'single\single_withoutstop_steplen_sim'),
        u'modelpattern':  r'testdimension_#ID#.txt.pk.[A-Z].html',
        u"systempattern" : r'testdimension_(\d+).txt', #note that in real dir, .0[1-7] is appended to the systempattern for the model id

        u'system_filename_pattern_id' : r'testdimension_#ID#.txt',
        u'pickle_file_pattern_id':r'testdimension_#ID#.txt.pk', # inc_test

        u'model_filenames_pattern_id' : r'testdimension_(\d+).txt.pk.[A-Z].html',

        u'keyword_bench_path':os.path.join(dataroot,  r'single\keyword'),

        u'remove_stopwords':1, #1 for use, 2 for not use
        u'keyword_path':os.path.join(dataroot,r'single\keyword'),
        u'borrow_allsent_path':os.path.join(dataroot,  r'single\single_withoutstop'),
        u'borrow_system_id':r'03'
        }
    return rankpara
conf_dict={
'duc_withstop_max100':duc_withstop_max100(),
'duc_withoutstop_max100':duc_withoutstop_max100(),
'duc_withoutstop_topk':duc_withoutstop_topk(),
'duc_withstop_topk':duc_withstop_topk(),
'acl_exc_withstop_max100':acl_exc_withstop_max100(),
'acl_exc_withoutstop_max100':acl_exc_withoutstop_max100(),
'acl_exc_withoutstop_topk':acl_exc_withoutstop_topk(),
'acl_inc_withstop_max100':acl_inc_withstop_max100(),
'acl_inc_withoutstop_max100':acl_inc_withoutstop_max100(),
'acl_inc_withoutstop_topk':acl_inc_withoutstop_topk(),
'single_withstop':single_withstop(),
'single_withoutstop':single_withoutstop(),
'single_withoutstop_steplen':single_withoutstop_steplen(),
'single_withoutstop_steplen_sim':single_withoutstop_steplen_sim(),
}
def GetSystemID(testset):
    test_id =[]
    for eachtest in testset:
        test_id.append(idname[eachtest])
    return test_id

def GetRankPara(dict_conf_name):
    if dict_conf_name not in conf_dict.keys():
        print 'no such name'
        return
    rankpara = conf_dict[dict_conf_name]
    return rankpara
def PrepareFilePrefix(rankpara):
    mid = []
    for eachmod in rankpara['model_test']:
        mid.append( idname[eachmod])
    smid = '_'.join(mid)
    shead = rankpara['rougetxthead']
    fileprefix = shead+'_'+smid
    return fileprefix
def GetConfResultFileName(dict_conf_name):
    if dict_conf_name not in conf_dict.keys():
        print 'no such name'
        return
    rankpara = conf_dict[dict_conf_name]
    fhead = GetConfResultFileName(rankpara)
    out_dir = rankpara['outdir']
    txtfilename = os.path.join(out_dir,fhead + '.txt')
    return txtfilename
def PlotScore(dict_conf_name,ifshow =0):
    if dict_conf_name not in conf_dict.keys():
        print 'no such name'
        return
    rankpara = conf_dict[dict_conf_name]
    scoreoutputdir = rankpara['outdir']#r'D:\pythonwork\code\tjrank_sentences\context\result\r3smax100'
    fhead = PrepareFilePrefix(rankpara)
    methodhead = rankpara['rougetxthead']#scoreoutputdir.split('\\')[-1]
    sxpReadFileMan.CheckMkDir(scoreoutputdir)
    para_file_name =methodhead + '_' +fhead +'_rankpara.pk'
    rankparafname = os.path.join(scoreoutputdir,para_file_name)
    sxpReadFileMan.StoreSxptext(rankpara, rankparafname)

    out_dir = rankpara['outdir']
    txtfilename = os.path.join(out_dir,fhead + '.txt')
    sxpParseRougeScore.TestSxpPyrougeScoreTxtFile(txtfilename,scoreoutputdir,dict_conf_name,ifshow =0)
def OutPutInYX(dict_conf_name,score_lable_list_dict,score_lable_list,model_lable_list_dict,model_lable_list):
    if dict_conf_name not in conf_dict.keys():
        print 'no such name'
        return
    rankpara = conf_dict[dict_conf_name]
    scoreoutputdir = rankpara['outdir']#r'D:\pythonwork\code\tjrank_sentences\context\result\r3smax100'
    fhead = PrepareFilePrefix(rankpara)
    methodhead = rankpara['rougetxthead']#scoreoutputdir.split('\\')[-1]
  #  sxpReadFileMan.CheckMkDir(scoreoutputdir)
    para_file_name =methodhead + '_' +fhead +'_rankpara.pk'
    rankparafname = os.path.join(scoreoutputdir,para_file_name)
##    sxpReadFileMan.StoreSxptext(rankpara, rankparafname)
    out_dir = rankpara['outdir']
    txtfilename = os.path.join(out_dir,fhead + '.txt')
    pkname = os.path.join(out_dir, txtfilename+'.pk')
    print txtfilename
    print pkname
    score_dict = sxpReadFileMan.LoadSxptext(pkname)
    print score_dict
#    print score_dict['02']
    metric_dict={}
    i=0
    j=0
    k=0
    model_num = len(score_dict.keys())
    print score_dict.keys()
    score_num =0
    metric_num =0
    modelname_list={}
    metric_name_list={}
    score_name_list={}

    for i,eachmodeid in enumerate( score_dict.keys()): #02, 03,..
        modelname = modename_dict[eachmodeid]
        modelname_list[i]=modelname
        print i,modelname #02,03
        metric_score = score_dict[eachmodeid]
        sub_score_len = len(metric_score.keys())
        print metric_score.keys()
        if sub_score_len>score_num:
            score_num=sub_score_len

        for j, sub_score_name in enumerate(metric_score.keys()):
            print j,sub_score_name
            score_name_list[j]=sub_score_name
            metric_val_list = metric_score[sub_score_name]
            metric_len = len(metric_val_list)
#            print metric_val_list
            if metric_num<metric_len:
                metric_num=metric_len
            metric_name=[]
            for k, val in enumerate(metric_val_list):
                metric_name_list[k]=val[0]

    print(model_num,score_num,metric_num)
    score_array=np.ndarray((model_num,score_num,metric_num),dtype=float)
    score_all_list=[]
    print 'modelname_list', modelname_list
    print 'score_name_list', score_name_list
    print 'metric_name_list', metric_name_list


    for i,eachmodeid in enumerate( score_dict.keys()): #02, 03,..
        modelname = modename_dict[eachmodeid]
        modelname_list[i]=modelname
#        print i,modelname #02,03
        metric_score = score_dict[eachmodeid]
        sub_score_len = len(metric_score.keys())
#        print metric_score.keys()
        if sub_score_len>score_num:
            score_num=sub_score_len

        for j, sub_score_name in enumerate(metric_score.keys()):
#            print j,sub_score_name
            score_name_list[j]=sub_score_name
            metric_val_list = metric_score[sub_score_name]
            metric_len = len(metric_val_list)
#            print metric_val_list
            if metric_num<metric_len:
                metric_num=metric_len
            metric_name=[]
            for k, val in enumerate(metric_val_list):
                metric_name_list[k]=val[0]
                score_array[i,j,k]=val[1]
                score_all_list.append([i,j,k,val[1:]])
#    print score_all_list
#now we begin to organize the score in precision, recall, and f-score,each being a table.
    xname = txtfilename + '.rouge_score_dim.xls'
    fname = xname
    print fname
##    try:
    workbook = xlsxwriter.Workbook(fname)
    worksheet = workbook.add_worksheet()

    metric_table_list={}
    rown = 0
    selected_model_name = []
    for each in model_lable_list:
        selected_model_name.append(model_lable_list_dict[each])
    model_id_dict ={}
    for eachid, modelname in modelname_list.items():
        model_id_dict[modelname]=eachid
    selected_model_id =[]
    for eachname in selected_model_name:
        if eachname in model_id_dict.keys():
            selected_model_id.append(model_id_dict[eachname])
    for k,eachmetric in metric_name_list.items():
        table = []
        head=[]
        worksheet.write(rown, 0, eachmetric)
        rown = rown + 1
        coli=1
        for key in score_lable_list:
            h=score_name_list[key]
            head.append(h)
            worksheet.write(rown, coli, h)
            coli = coli+1
        table.append(['',head])
        rown = rown + 1
        for i in selected_model_id:#range(model_num):
            row=[]
            if i not in modelname_list.keys():
                continue
            row.append(modelname_list[i])
            worksheet.write(rown, 0, modelname_list[i])
            coli=1
            for j in score_lable_list:
                value = score_array[i,j,k]
                row.append(value)
                worksheet.write(rown, coli, value)
                coli = coli+1
            rown=rown+1
            table.append(row)
        metric_table_list[eachmetric]=table
        print table
    workbook.close()
def OutPutCurrentResultDir(dict_conf_name):
    if dict_conf_name not in conf_dict.keys():
        print 'no such name'
        return
    print '-------------',dict_conf_name,'-----------'
    rankpara = conf_dict[dict_conf_name]
    scoreoutputdir = rankpara['outdir']#r'D:\pythonwork\code\tjrank_sentences\context\result\r3smax100'
    fhead = PrepareFilePrefix(rankpara)
    methodhead = rankpara['rougetxthead']#scoreoutputdir.split('\\')[-1]
  #  sxpReadFileMan.CheckMkDir(scoreoutputdir)
    para_file_name =methodhead + '_' +fhead +'_rankpara.pk'
    rankparafname = os.path.join(scoreoutputdir,para_file_name)
##    sxpReadFileMan.StoreSxptext(rankpara, rankparafname)
    out_dir = rankpara['outdir']
    print out_dir
    txtfilename = os.path.join(out_dir,fhead + '.txt')
    pkname = os.path.join(out_dir, txtfilename+'.pk')
    para_file_name =methodhead + '_' +fhead +'_rankpara.pk'
    xname = txtfilename + '.rouge_score_dim.xls'
    print xname
def ShowDir():
    OutPutCurrentResultDir('acl_inc_withstop_max100')
    OutPutCurrentResultDir('acl_exc_withstop_max100')

    OutPutCurrentResultDir('acl_inc_withoutstop_max100')
    OutPutCurrentResultDir('acl_exc_withoutstop_max100')

    OutPutCurrentResultDir('duc_withstop_max100')
    OutPutCurrentResultDir('duc_withoutstop_max100')

    OutPutCurrentResultDir('duc_withoutstop_topk')
    OutPutCurrentResultDir('acl_inc_withoutstop_topk')
    OutPutCurrentResultDir('acl_exc_withoutstop_topk')
def OutPutScoreDim():
    score_lable_list_dict={1: u'ROUGE-1', 2: u'ROUGE-2', 4: u'ROUGE-3', 3: u'ROUGE-4',0: u'ROUGE-L', }
    score_lable_list=[1,2,4,3,0]
    model_lable_list_dict={0: 'tfidf', 1: 'simgraph', 2: 'para', 3: 'parasec', 4: 'subparasec', 5: 'wordgraph', 6: 'subpara', 7: 'hybrid', 8: 'sectitle', 9: 'mywordgraph'}
    model_lable_list=[0,1,2,3,4,5,6,7,8]

    OutPutInYX('acl_inc_withstop_max100',score_lable_list_dict,score_lable_list,model_lable_list_dict,model_lable_list)
    OutPutInYX('acl_exc_withstop_max100',score_lable_list_dict,score_lable_list,model_lable_list_dict,model_lable_list)

    OutPutInYX('acl_inc_withoutstop_max100',score_lable_list_dict,score_lable_list,model_lable_list_dict,model_lable_list)
    OutPutInYX('acl_exc_withoutstop_max100',score_lable_list_dict,score_lable_list,model_lable_list_dict,model_lable_list)

    OutPutInYX('duc_withstop_max100',score_lable_list_dict,score_lable_list,model_lable_list_dict,model_lable_list)
    OutPutInYX('duc_withoutstop_max100',score_lable_list_dict,score_lable_list,model_lable_list_dict,model_lable_list)

    OutPutInYX('duc_withoutstop_topk',score_lable_list_dict,score_lable_list,model_lable_list_dict,model_lable_list)
    OutPutInYX('acl_inc_withoutstop_topk',score_lable_list_dict,score_lable_list,model_lable_list_dict,model_lable_list)
    OutPutInYX('acl_exc_withoutstop_topk',score_lable_list_dict,score_lable_list,model_lable_list_dict,model_lable_list)
#r3: without stopwords, topk
#r4: withstopword max100
#r3max: without stopwords max100

def main():
##    for eachname in conf_dict.keys():
##        print eachname
##        PlotScore(eachname)
##    OutPutScoreDim()
##    ShowDir()
    PlotScore('acl_inc_withoutstop_topk')
if __name__ == '__main__':
    main()
