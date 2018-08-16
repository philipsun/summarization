__author__ = 'a'
from Controller import *
import os

modeldir = r'D:\pythonwork\code\paperparse\paper\papers\model'
systemdir = r'D:\pythonwork\code\paperparse\paper\papers\system'
#dataroot = r'D:\pythonwork\code\paperparse\paper'
def sxpGetDirFileSubList(filedir):
    if not os.path.exists(filedir):
        print 'no dir to be read'
        print filedir
        return []
    filelist = []
    subdirlist = []
    try:
        files = os.listdir(filedir)
        #now we first read each file in the txtPath
        for f in files:
          df = os.path.join(filedir, f)
          if os.path.isdir(df):
             subdirlist.append(f)
          else:
             filelist.append(f)
    except Exception as e:
        msg = filedir + ':' + str(e)
        print msg
    return filelist, subdirlist
def GetSystemDir():
    subfile, subdir = sxpGetDirFileSubList(systemdir)
    systemsub_set = []
    for eachsub in subdir:
        subdirfull = systemdir + '\\' + eachsub
        systemsub_set.append(subdirfull)
    return systemsub_set
def TestDir():
    print modeldir
    print GetSystemDir()
##def main():
##    #path = r'C:\Users\a\PycharmProjects\extractInfo\papers'
##    path = r'D:\pythonwork\code\paperparse\paper\papers'
##    evaluate_all_forjava(path, 'context1',10,1,0)
##    evaluate_all_forjava(path, 'mymodel',10,1,0)
##    evaluate_all_forjava(path, 'tfidf',10,1,0)
##    evaluate_all_forjava(path, 'graphb',10,1,0)
##    evaluate_all_forjava(path, 'graphw',10,1,0)

idname = {'mymodel':'01',
    'tfidf':'02',
    'graphb':'03',
    'graphw':'04',
    'context1':'05',
    'mysecmodel':'06',
    'myseccontextmodel':'07',
    'hybrid':'08',
    'sectitle':'09',
    'mywordgraph':'10'
    }

def Rank_system_model_pyrouge_exc(dataroot,rankpara,testall=0,testset=[]):
##    idname = {'mymodel':'01',
##    'tfidf':'02',
##    'graphb':'03',
##    'graphw':'04',
##    'context1':'05',
##    'mysecmodel':'06',
##    'myseccontextmodel':'07',
##    'hybrid':'08',
##    'sectitle':'09'}
    if len(testset)==0:
        if testall==1:
            testset = ['mymodel','tfidf','graphb','graphw','context1','mysecmodel','myseccontextmodel','hybrid','sectitle','mywordgraph']
        else:
           testset = ['graphb','graphw','context1','mysecmodel','myseccontextmodel','hybrid']
           testset = ['graphw']
           testset =['mywordgraph']
    testset = rankpara['model_test']
##    pickle_path = os.path.join(dataroot,r'papers\pickle')
##    model_path =  os.path.join(dataroot,r'papers\model_html')
##    system_path = os.path.join(dataroot,r'papers\system_html4')

    pickle_path = os.path.join(dataroot,rankpara['pickle_path'])#'papers\duc\txt\pickle')
    model_path =  os.path.join(dataroot,rankpara['model_path'])#,r'papers\duc\txt\model_html')
    system_path = os.path.join(dataroot,rankpara['system_path'])#',r'papers\duc\txt\system_html1')

    model_filenames_pattern = r'p14-#ID#.xhtml.[A-Z].html'
    model_filenames_pattern_id = r'P14-(\d+).xhtml.[A-Z].html'
    system_filename_pattern =r'P14-(\d+).xhtml.html.0[1-7]'
    system_filename_pattern_id =r'P14-#ID#.xhtml.html'
    pickle_file_pattern_id =r'P14-#ID#.xhtml_3.pickle' # exc_test

##    if  inc_abscon == False:
##            pickle_path = pickle_dir + file_name + '_3.pickle'
##    else:
##            pickle_path = pickle_dir + file_name + '_2.pickle'

    pk_sys_set = PreparePickleByModelFileSet(model_path,model_filenames_pattern_id,pickle_path,pickle_file_pattern_id,system_filename_pattern_id)
    for eachpick in pk_sys_set:
        print(eachpick)
    for eachtest in testset:
        system_id= idname[eachtest]
        print eachtest,system_id
        run_one_rankmodel(pickle_path,pk_sys_set,system_path,system_id,eachtest,rankpara)
def Rank_single_paper(dataroot,rankpara,testall=0):
##    idname = {'mymodel':'01',
##    'tfidf':'02',
##    'graphb':'03',
##    'graphw':'04',
##    'context1':'05',
##    'mysecmodel':'06',
##    'myseccontextmodel':'07',
##    'hybrid':'08',
##    'sectitle':'09'}
    if testall==1:
        testset = ['mymodel','tfidf','graphb','graphw','context1','mysecmodel','myseccontextmodel','hybrid','sectitle','mywordgraph']
    else:
        testset = ['mywordgraph']
    #    testset = ['mysecmodel','myseccontextmodel']
    #    testset = ['hybrid']
    testset =rankpara['model_test']
##    pickle_path = os.path.join(dataroot,r'/pickle')
##    model_path =  os.path.join(dataroot,r'/model_html')
##    system_path = os.path.join(dataroot,r'/system_html5')

    model_path = os.path.join(dataroot,r'single\model')
    pickle_path = os.path.join(dataroot,r'single\pk')
    system_path = os.path.join(dataroot,r'single\system')

    model_filenames_pattern = r'testdimension_#ID#.txt.pk.[A-Z]'
    model_filenames_pattern_id = r'testdimension_(\d+).txt.pk.[A-Z]'
    system_filename_pattern =r'testdimension_(\d+).txt.pk.0[1-9]'
    system_filename_pattern_id =r'testdimension_#ID#.txt'
##    if  inc_abscon == False:
##            pickle_path = pickle_dir + file_name + '_3.pickle'
##    else:
##            pickle_path = pickle_dir + file_name + '_2.pickle'

#    pickle_file_pattern_id =r'P14-#ID#.xhtml_2.pickle' # inc_test
    pickle_file_pattern_id =r'testdimension_#ID#.txt.pk' # inc_test
    pk_sys_set = PreparePickleByModelFileSet(model_path,model_filenames_pattern_id,pickle_path,pickle_file_pattern_id,system_filename_pattern_id)
    for eachpick in pk_sys_set:
        print(eachpick)
    for eachtest in testset:
        system_id= idname[eachtest]
        run_one_rankmodel(pickle_path,pk_sys_set,system_path,system_id,eachtest,rankpara)

def Rank_system_model_pyrouge_inc(dataroot,rankpara,testall=0,testset=[]):
    if len(testset)==0:
        if testall==1:
            testset = ['mymodel','tfidf','graphb','graphw','context1','mysecmodel','myseccontextmodel','hybrid','sectitle','mywordgraph']
        else:
            testset = ['mywordgraph']
  #  testset = ['mywordgraph']
    testset = rankpara['model_test']

##    pickle_path = os.path.join(dataroot,r'papers\pickle')
##    model_path =  os.path.join(dataroot,r'papers\model_html')
##    system_path = os.path.join(dataroot,r'papers\system_html5')
    pickle_path = os.path.join(dataroot,rankpara['pickle_path'])#'papers\duc\txt\pickle')
    model_path =  os.path.join(dataroot,rankpara['model_path'])#,r'papers\duc\txt\model_html')
    system_path = os.path.join(dataroot,rankpara['system_path'])#',r'papers\duc\txt\system_html1')
    model_filenames_pattern = r'p14-#ID#.xhtml.[A-Z].html'
    model_filenames_pattern_id = r'P14-(\d+).xhtml.[A-Z].html'
    system_filename_pattern =r'P14-(\d+).xhtml.html.0[1-9]'
    system_filename_pattern_id =r'P14-#ID#.xhtml.html'
    pickle_file_pattern_id =r'P14-#ID#.xhtml_2.pickle' # inc_test
##    if  inc_abscon == False:
##            pickle_path = pickle_dir + file_name + '_3.pickle'
##    else:
##            pickle_path = pickle_dir + file_name + '_2.pickle'


    pk_sys_set = PreparePickleByModelFileSet(model_path,model_filenames_pattern_id,pickle_path,pickle_file_pattern_id,system_filename_pattern_id)
    for eachpick in pk_sys_set:
        print(eachpick)
    for eachtest in testset:
        system_id= idname[eachtest]
        print eachtest,system_id
        run_one_rankmodel(pickle_path,pk_sys_set,system_path,system_id,eachtest,rankpara)

def PreparePickleByModelFileSet(model_path,model_filenames_pattern_id,pickle_path,pickle_file_pattern_id,system_filename_pattern_id):
    flist, sublist = sxpGetDirFileSubList(model_path)
    model_filenames_pattern_id = re.compile(model_filenames_pattern_id)
    model_set_id = {}
    i = 0
    for eachf in flist:
        match = model_filenames_pattern_id.match(eachf)
        if match:
            id = match.groups(0)[0]
            model_set_id[id] = i
            i = i + 1

    pk_sys_set = []
    for eachid,index in model_set_id.items():
        pk_sys_set.append([pickle_file_pattern_id.replace('#ID#', eachid),system_filename_pattern_id.replace('#ID#', eachid)])

    return pk_sys_set
def Rank_duc_docs(dataroot,rankpara,testall=0, testset=[]):
    if len(testset)==0:
        if testall ==0:
            testset = ['mywordgraph']
        else:
            testset = ['mymodel','tfidf','graphb','graphw','context1','hybrid','mywordgraph']
    testset = rankpara['model_test']
##    print r"D:\pythonwork\code\paperparse\paper\papers\duc\txt\model_html"
##    pickle_path = os.path.join(dataroot,r'papers\duc\txt\pickle')
##    model_path =  os.path.join(dataroot,r'papers\duc\txt\model_html')
##    system_path = os.path.join(dataroot,r'papers\duc\txt\system_html1')
##    pickle_path = os.path.join(dataroot,rankpara['pickle_path'])#'papers\duc\txt\pickle')
##    model_path =  os.path.join(dataroot,rankpara['model_path'])#,r'papers\duc\txt\model_html')
##    system_path = os.path.join(dataroot,rankpara['system_path'])#',r'papers\duc\txt\system_html1')
    pickle_path = rankpara['pickle_path']#'papers\duc\txt\pickle')
    model_path =  rankpara['model_path']#,r'papers\duc\txt\model_html')
    system_path = rankpara['system_path']#',r'papers\duc\txt\system_html1')
    print pickle_path
    print model_path
    print system_path
##    pickle_path = r'D:\pythonwork\code\paperparse\paper\papers\duc\txt\pickle'
##    model_path =  r'D:\pythonwork\code\paperparse\paper\papers\duc\txt\model_html'
##    system_path = r'D:\pythonwork\code\paperparse\paper\papers\duc\txt\system_html1'
    model_filenames_pattern = r'D\d\d\d.P.100.[A-Z].[A-Z].#ID#.html'
    model_filenames_pattern_id = r'D\d\d\d.P.100.[A-Z].[A-Z].(\w+-\w+).html'

    system_filename_pattern =r'D\d\d\d.P.100.[A-Z].[A-Z].(\w+-\w+).html.0[1-8]'
   # system_filename_pattern_id =r'P14-#ID#.xhtml.html'
    system_filename_pattern_id = r'#ID#.html'
    pickle_file_pattern_id =r'#ID#' # inc_test

    model_filenames_pattern_id = rankpara['model_filenames_pattern_id']# r'D\d\d\d.P.100.[A-Z].[A-Z].(\w+-\w+).html',
    system_filename_pattern_id = rankpara['system_filename_pattern_id']#r'#ID#.html',
    pickle_file_pattern_id = rankpara['pickle_file_pattern_id']#r'#ID#' # inc_test
##    if  inc_abscon == False:
##            pickle_path = pickle_dir + file_name + '_3.pickle'
##    else:
##            pickle_path = pickle_dir + file_name + '_2.pickle'


    pk_sys_set = PreparePickleByModelFileSet(model_path,model_filenames_pattern_id,
    pickle_path,pickle_file_pattern_id,system_filename_pattern_id)
    for eachpick in pk_sys_set:
        print(eachpick)
    for eachtest in testset:
        system_id= idname[eachtest]
        print pickle_path
       # run_one_rankmodel_duc(pickle_path,pk_sys_set,system_path,system_id,eachtest,rankpara)
        run_one_rankmodel(pickle_path,pk_sys_set,system_path,system_id,eachtest,rankpara)
def RankPara(rankpara):

    testset = rankpara['model_test']
##    print r"D:\pythonwork\code\paperparse\paper\papers\duc\txt\model_html"
##    pickle_path = os.path.join(dataroot,r'papers\duc\txt\pickle')
##    model_path =  os.path.join(dataroot,r'papers\duc\txt\model_html')
##    system_path = os.path.join(dataroot,r'papers\duc\txt\system_html1')
##    pickle_path = os.path.join(dataroot,rankpara['pickle_path'])#'papers\duc\txt\pickle')
##    model_path =  os.path.join(dataroot,rankpara['model_path'])#,r'papers\duc\txt\model_html')
##    system_path = os.path.join(dataroot,rankpara['system_path'])#',r'papers\duc\txt\system_html1')
    pickle_path = rankpara['pickle_path']#'papers\duc\txt\pickle')
    model_path =  rankpara['model_path']#,r'papers\duc\txt\model_html')
    system_path = rankpara['system_path']#',r'papers\duc\txt\system_html1')
    print pickle_path
    print model_path
    print system_path
##    pickle_path = r'D:\pythonwork\code\paperparse\paper\papers\duc\txt\pickle'
##    model_path =  r'D:\pythonwork\code\paperparse\paper\papers\duc\txt\model_html'
##    system_path = r'D:\pythonwork\code\paperparse\paper\papers\duc\txt\system_html1'
##    model_filenames_pattern = r'D\d\d\d.P.100.[A-Z].[A-Z].#ID#.html'
##    model_filenames_pattern_id = r'D\d\d\d.P.100.[A-Z].[A-Z].(\w+-\w+).html'
##
##    system_filename_pattern =r'D\d\d\d.P.100.[A-Z].[A-Z].(\w+-\w+).html.0[1-8]'
##   # system_filename_pattern_id =r'P14-#ID#.xhtml.html'
##    system_filename_pattern_id = r'#ID#.html'
##    pickle_file_pattern_id =r'#ID#' # inc_test

    model_filenames_pattern_id = rankpara['model_filenames_pattern_id']# r'D\d\d\d.P.100.[A-Z].[A-Z].(\w+-\w+).html',
    system_filename_pattern_id = rankpara['system_filename_pattern_id']#r'#ID#.html',
    pickle_file_pattern_id = rankpara['pickle_file_pattern_id']#r'#ID#' # inc_test
    modelidname=rankpara['idname']
##    if  inc_abscon == False:
##            pickle_path = pickle_dir + file_name + '_3.pickle'
##    else:
##            pickle_path = pickle_dir + file_name + '_2.pickle'


    pk_sys_set = PreparePickleByModelFileSet(model_path,model_filenames_pattern_id,
    pickle_path,pickle_file_pattern_id,system_filename_pattern_id)
    for eachpick in pk_sys_set:
        print(eachpick)
    for eachtest in testset:
        system_id= modelidname[eachtest]
        #system_id= [eachtest]
        print pickle_path
       # run_one_rankmodel_duc(pickle_path,pk_sys_set,system_path,system_id,eachtest,rankpara)
        run_one_rankmodel(pickle_path,pk_sys_set,system_path,system_id,eachtest,rankpara)
def GetSystemModelFilePair(rankpara):

    testset = rankpara['model_test']
##    print r"D:\pythonwork\code\paperparse\paper\papers\duc\txt\model_html"
##    pickle_path = os.path.join(dataroot,r'papers\duc\txt\pickle')
##    model_path =  os.path.join(dataroot,r'papers\duc\txt\model_html')
##    system_path = os.path.join(dataroot,r'papers\duc\txt\system_html1')
##    pickle_path = os.path.join(dataroot,rankpara['pickle_path'])#'papers\duc\txt\pickle')
##    model_path =  os.path.join(dataroot,rankpara['model_path'])#,r'papers\duc\txt\model_html')
##    system_path = os.path.join(dataroot,rankpara['system_path'])#',r'papers\duc\txt\system_html1')
    pickle_path = rankpara['pickle_path']#'papers\duc\txt\pickle')
    model_path =  rankpara['model_path']#,r'papers\duc\txt\model_html')
    system_path = rankpara['system_path']#',r'papers\duc\txt\system_html1')
    print pickle_path
    print model_path
    print system_path
##    pickle_path = r'D:\pythonwork\code\paperparse\paper\papers\duc\txt\pickle'
##    model_path =  r'D:\pythonwork\code\paperparse\paper\papers\duc\txt\model_html'
##    system_path = r'D:\pythonwork\code\paperparse\paper\papers\duc\txt\system_html1'
##    model_filenames_pattern = r'D\d\d\d.P.100.[A-Z].[A-Z].#ID#.html'
##    model_filenames_pattern_id = r'D\d\d\d.P.100.[A-Z].[A-Z].(\w+-\w+).html'
##
##    system_filename_pattern =r'D\d\d\d.P.100.[A-Z].[A-Z].(\w+-\w+).html.0[1-8]'
##   # system_filename_pattern_id =r'P14-#ID#.xhtml.html'
##    system_filename_pattern_id = r'#ID#.html'
##    pickle_file_pattern_id =r'#ID#' # inc_test

    model_filenames_pattern_id = rankpara['model_filenames_pattern_id']# r'D\d\d\d.P.100.[A-Z].[A-Z].(\w+-\w+).html',
    system_filename_pattern_id = rankpara['system_filename_pattern_id']#r'#ID#.html',
    pickle_file_pattern_id = rankpara['pickle_file_pattern_id']#r'#ID#' # inc_test
    modelidname=rankpara['idname']
##    if  inc_abscon == False:
##            pickle_path = pickle_dir + file_name + '_3.pickle'
##    else:
##            pickle_path = pickle_dir + file_name + '_2.pickle'


    pk_sys_set = PreparePickleByModelFileSet(model_path,model_filenames_pattern_id,
    pickle_path,pickle_file_pattern_id,system_filename_pattern_id)
    print('pickle path',pickle_path)
    for eachpick in pk_sys_set:
        print(eachpick)
    all_model = []
    if rankpara.has_key('keyword_bench_path'):
        keyword_bench_path = rankpara['keyword_bench_path']
    else:
        keyword_bench_path = ''
    for eachtest in testset:
        system_id= modelidname[eachtest]
        #system_id= [eachtest]
        print('working on',system_id,eachtest)

       # run_one_rankmodel_duc(pickle_path,pk_sys_set,system_path,system_id,eachtest,rankpara)
        model_files=[]
        for file_name,system_name in pk_sys_set:
            pickle_file = os.path.join(pickle_path,file_name)
            if len(keyword_bench_path)>0:
                keybench =os.path.join(keyword_bench_path,file_name+'.key')
            else:
                keybench =''
            topksent_path = system_path + '\\' + system_name + '.'+system_id
            allpkfname = topksent_path + 'allsent.pk'
            toppkfname = topksent_path + 'topsent.pk'
          #  model_files.append([pickle_file,topksent_path,allpkfname,keybench])
            file_dict={}
            file_dict['modelpatter']=model_filenames_pattern_id
            file_dict['modelid']=eachtest
            file_dict['systemid']=system_id
            file_dict['filepk']=pickle_file
            file_dict['sys']=topksent_path
            file_dict['allsentpk']=allpkfname
            file_dict['topsentpk']=toppkfname
            file_dict['keyword']=keybench
            model_files.append(file_dict)
            print('allsent:', allpkfname)
        all_model.append(model_files)
    return all_model
def main():
# note that this is the latest 2017.01.17
    evaluate = r'0'
    if evaluate == 'exc_acl':
        testall=0
        Rank_system_model_pyrouge_exc(testall)

    evaluate = r'0'
    if evaluate =='inc_acl':
        testall=0
        Rank_system_model_pyrouge_inc(testall)

    evaluate = r'0'
    if evaluate == 'single':
        testall=0
        Rank_single_paper(testall)

    evaluate = r'0'
    if evaluate == 'duc':
        testall=0
        Rank_duc_docs(testall)
if __name__ == '__main__':
    main()
