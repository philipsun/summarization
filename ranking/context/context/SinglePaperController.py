__author__ = 'a'
import os
from sxpPackage import *
from MyModel import *
from View import *
from tf_idf import *
from graph_base import GraphBased
from word_graph import WordGraph
from sxpContextModel import conTextModel
import sxpReadFileMan

def evaluate_singpaper(pkpath,modelpath,systempath, modeltype='mymodel',topksent=10, choice=1,maketxt = 1):
    print modeltype, topksent
    pickle_dir = pkpath + '\\'

    if modeltype == 'mymodel':
        idstr ='01'
    if modeltype == 'tfidf':
        idstr ='02'
    if modeltype == 'graphb':
        idstr ='03'
    if modeltype == 'graphw':
        idstr ='04'
    if modeltype == 'context1':
        idstr ='05'

    systemdirstr = systempath + '\\' + idstr
    if os.path.exists(systemdirstr)==False:
        os.mkdir(systemdirstr)

    #get the original filename list in the path variable
    file_list = GetDirFileList(pkpath)

    result = []
    intro_id_list = []
    i = 0
    for file_name in file_list:
        print i, file_name
        pickle_path = pickle_dir + file_name
        if modeltype == 'mymodel':
            model = MyModel(pickle_path)
        if modeltype == 'tfidf':
            model = TfIdf(pickle_path)
        if modeltype == 'graphb':
            model = GraphBased(pickle_path)
        if modeltype == 'graphw':
            model = WordGraph(pickle_path)
        if modeltype == 'context1':
            model = conTextModel(pickle_path)
        for title in model.section2sentence_id_list.keys():
            if title.lower().find('introduction') > 0:
                intro_id_list = model.section2sentence_id_list[title]
                break
#        if len(intro_id_list) == 0:
#            continue

        #save text ranked sentences to text
        topksent_path = systemdirstr + '\\' + file_name + '.' + idstr + '.html'
        tops = model.OutPutTopKSent(topksent,1,-1)
        st = ProduceSystem(tops,file_name + '.' + idstr,1)
##        for eachs in tops:
###            print st
##            st = st + eachs + '. \n'
        sxpReadFileMan.WriteStrFile(topksent_path,st, 'utf-8')
        #save text abstact text and conclusion text

        i = i + 1
    if choice == 1:
        title = "title\tprecision\trecall"
    elif choice == 2:
        title = "title\tprecision"
    print "finished"
def evaluate_all(path,modeltype='mymodel',topksent=10, choice=1,maketxt = 1):
    print modeltype, topksent
    pickle_dir = path + '\\pickle\\'

    if modeltype == 'mymodel':
        idstr ='01'
    if modeltype == 'tfidf':
        idstr ='02'
    if modeltype == 'graphb':
        idstr ='03'
    if modeltype == 'graphw':
        idstr ='04'
    if modeltype == 'context1':
        idstr ='05'

    systemdirstr = path + '\\system_html\\' + idstr
    if os.path.exists(systemdirstr)==False:
        os.mkdir(systemdirstr)

    txt_dir = path + '\\' + 'model\\'
    if os.path.exists(txt_dir)==False:
        os.mkdir(txt_dir)
    #get the original filename list in the path variable
    file_list = GetDirFileList(path)

    labeled_file = pickle_dir + '\\intro_sent_dict_id.pickle'
    labeled_data = LoadSxptext(labeled_file)
    result = []
    intro_id_list = []
    i = 0
    for file_name in file_list:
        if file_name.lower() not in labeled_data.keys():
            continue
        print i, file_name
        pickle_path = pickle_dir + file_name + '_2.pickle'
        if modeltype == 'mymodel':
            model = MyModel(pickle_path)
        if modeltype == 'tfidf':
            model = TfIdf(pickle_path)
        if modeltype == 'graphb':
            model = GraphBased(pickle_path)
        if modeltype == 'graphw':
            model = WordGraph(pickle_path)
        if modeltype == 'context1':
            model = conTextModel(pickle_path)
        for title in model.section2sentence_id_list.keys():
            if title.lower().find('introduction') > 0:
                intro_id_list = model.section2sentence_id_list[title]
                break
#        if len(intro_id_list) == 0:
#            continue

        #save text ranked sentences to text
        topksent_path = systemdirstr + '\\' + file_name + '.' + idstr + '.html'
        tops = model.OutPutTopKSent(topksent,1,-1)
        st = ProduceSystem(tops,file_name + '.' + idstr,1)
##        for eachs in tops:
###            print st
##            st = st + eachs + '. \n'
        sxpReadFileMan.WriteStrFile(topksent_path,st, 'utf-8')
        #save text abstact text and conclusion text

        i = i + 1
    if choice == 1:
        title = "title\tprecision\trecall"
    elif choice == 2:
        title = "title\tprecision"
    print "result"
    print result
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
def evaluate_all_forjava(path,modeltype='mymodel',topksent=10, choice=1,maketxt = 1):
    print modeltype, topksent
    pickle_dir = path + '\\pickle\\'

    top_k_sent_dir = path +'\\system\\'
    if modeltype == 'mymodel':
        idstr ='1'
    if modeltype == 'tfidf':
        idstr ='2'
    if modeltype == 'graphb':
        idstr ='3'
    if modeltype == 'graphw':
        idstr ='4'
    if modeltype == 'context1':
        idstr ='5'
    systemidstr = idstr
    systemdirstr = path + '\\system\\'
    if os.path.exists(systemdirstr)==False:
        os.mkdir(systemdirstr)

    txt_dir = path + '\\' + 'model\\'
    if os.path.exists(txt_dir)==False:
        os.mkdir(txt_dir)
    #get the original filename list in the path variable
##    file_list = [file_name for file_name in os.listdir(path)
##                 if os.path.isfile(path + '\\' + file_name)]
    file_list = GetDirFileList(path)

    labeled_file = pickle_dir + '\\intro_sent_dict_id.pickle'
    labeled_data = LoadSxptext(labeled_file)
    result = []
    intro_id_list = []
    i = 0
    for file_name in file_list:
        fset = file_name.split('.')
        n = len(fset)
        if n <= 1:
            continue
        else:
            sf = fset[-1].lower()
            if sf == 'xhtml':
                print i, file_name
                pickle_path = pickle_dir + file_name + '_2.pickle'
                if modeltype == 'mymodel':
                    model = MyModel(pickle_path)
                if modeltype == 'tfidf':
                    model = TfIdf(pickle_path)
                if modeltype == 'graphb':
                    model = GraphBased(pickle_path)
                if modeltype == 'graphw':
                    model = WordGraph(pickle_path)
                if modeltype == 'context1':
                    model = conTextModel(pickle_path)
                #save text ranked sentences to text
           #     topksent_path = systemdirstr + '\\' + file_name + '.' + systemidstr + '.txt'
                topksent_path = systemdirstr + '\\' + fset[0] + '_system' + systemidstr + '.txt'
                tops = model.OutPutTopKSent(topksent)
                st = ProduceSystem(tops, fset[0] + '_system' + systemidstr, 0 )
        ##        for eachs in tops:
        ###            print st
        ##            st = st + eachs + '. \n'
                sxpReadFileMan.WriteStrFile(topksent_path,st, 'utf-8')
                #save text abstact text and conclusion text

                i = i + 1
    if choice == 1:
        title = "title\tprecision\trecall"
    elif choice == 2:
        title = "title\tprecision"
    print "result"
    print result
def ProduceSystem(tops, fn, formatsent = 0):
        modeltxt  = '''
<html><head>
    <title>%s</title>
</head>
'''%(fn)
        sentenceset = tops
        i = 0
        abstract_str = ''
        for sent in sentenceset:
            rsent = RemoveUStrSpace(sent)
            if len(rsent)<=0:
                rsent = 'test sentence is empty'
            i = i + 1
            if formatsent == 1:
                sentr ='''
     <a name="%d">[%d]</a> <a href="#%d" id=%d>%s.</a>\n'''%(i,i,i,i,rsent)
            if formatsent == 0:
                sentr = rsent + '\n'
            abstract_str = abstract_str +sentr
        if formatsent == 1:
            bodytxt = '''
   <body bgcolor="white">
       %s
   </body>
</html>
        '''%(abstract_str)
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
def evaluate(intro_id_list, intro_labeled_id_set, choice=1):
    #calc_topK_distance(intro_id_list, intro_labeled_id_set)
    if len(intro_id_list) == 0:
        print "no introduction"
        return -1
    if choice == 1:
        return top_k_precision_and_recall(15, intro_id_list, intro_labeled_id_set)
    elif choice == 2:
        return precision(intro_id_list, intro_labeled_id_set)


# evaluate method three
# use the Jaccard Distance to evaluate the set returned by
# my algorithm and the manually given set
def calc_top_k_distance(intro_id_list, intro_labeled_id_set):
    distance = []
    print intro_id_list
    print intro_labeled_id_set
    for i in range(len(intro_id_list) / 5 + int((len(intro_id_list) % 5) > 0)):
        topK = intro_id_list[:(i + 1) * 5]
        common_ids = set(topK).intersection(set(intro_labeled_id_set))
        #total_ids = set(topK).union(set(intro_label_id_set))
        #jaccard = float(len(common_ids)) / len(total_ids)
        #distance.append(jaccard)
        #print jaccard
    return distance


#evaluate method one
def top_k_precision_and_recall(k, intro_id_list, intro_labeled_id_set):
    size = k
    if len(intro_id_list) < k:
        size = len(intro_id_list)
    common_ids = set(intro_labeled_id_set).intersection(set(intro_id_list[:size]))
    pre = float(len(common_ids)) / size
    recall = float(len(common_ids)) / len(intro_labeled_id_set)
    if pre == 0 or recall == 0:
        f_score = 0
    else:
        f_score = pre * recall / float(pre + recall)
    return pre, recall, f_score


#evaluate method two
#use the precision to evaluate the algorithms
def precision(intro_id_list, intro_label_id_set):
    size = len(intro_label_id_set)
    top_k = intro_id_list[:size]
    common_ids = set(intro_label_id_set).intersection(set(top_k))
    return [len(common_ids) / float(size)]
