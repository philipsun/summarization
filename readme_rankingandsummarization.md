# Ranking sentence and Do Rouge Test.

This prackage contains two major parts, (1) first it load document structure that are parsed by the PAPERPARSE package and then rank sentences using many models; (2) It calls pyrouge to measure the resulted outputs of summarization models to obtain ROUGE-1,2,3,4,L scores.

#The Major entry function:
sxpDoPyrougeScoreTest.py

In this function, you need to specify root data directory for the program.

> dataroot = r"E:/pythonwork/code/paperparse/paper"
> 
> if os.path.exists(dataroot)==False:
> 
>     dataroot = r"E:/pythonworknew/code/paperparse/paper"
> 
> sxpPyrougeEvaluate.conf_path = r"./rouge_conf.xml"
> 
> sxpPyrougeEvaluate.perlpathname=r"C:/Perl/bin/perl"
> 
> 

### ranking the graph

Then, the major entry call function is:
This is to rank sentences and score them, according to the three control parameters: 

>     cmdstr = "RunRankAndParseScore"
>     if cmdstr == 'RunRankAndParseScore':
>         rankthem =0
>         rougethem =0
>         ifshow = 1
>         RunConfig('duc_withoutstop_max100',rankthem,rougethem)
>         RunConfig('acl_exc_withoutstop_max100',rankthem,rougethem,ifshow =ifshow)
> 
> 

You should **ensure that '/contex/\result' already exists**

In our case, ./context/result will contains all files and subs.

### To make pyrouge and ROUGE work in Windows

It is not so easy to make pyrouge work in Windows. You need to fix some bugs before calling it by our packages:

First, you need to install Perl in your <b>C:Perl</b>

Then you need to copy pyrouge to your project directory

Set up the ini file in your pyrouge directory, <b>settings.ini</b>

and copy it to 

<b>C:\\Users\\your account in windows\\AppData\\Roaming\\pyrouge\\settings.ini</b>

>[pyrouge settings]
>
>home_dir = D:\\pythonwork\\code\\ROUGE-1.5.5\\RELEASE-1.5.5

ROUGE's codes also has some problem when coping with Pyrouge, to fixed please use our ROUGE-1.5.5.pl file to replace the one in original implementation of ROUGE 1.5.5. We provide the revised version in this package files.


###  Model configurations

To ranking the models:

We need to add an model configuration in 

sxpRougeConfig.py

First, you need to set up data dir for the network piclke files:

> dataroot = r"E:\\pythonwork\\code\\paperparse\\paper"
> 

Second, you need to setup model ids in dict <b>idname</b>:

> idname = {'para':'01',
>     'tfidf':'02',
>     'simgraph':'03',
>     'wordgraph':'04',
>     'subpara':'05',
>     'parasec':'06',
>     'subparasec':'07',
>     'hybrid':'08',
>     'sectitle':'09',
>     'mywordgraph':'10',
>     'sp1':'11',
>     'sp3':'12',
>     'sp5':'13',
>     'sp7':'14',
>     'sp9':'15',
>     'sp11':'16',
>     'sp13':'17',
>     'sim1':'18',
>     'sim3':'19',
>     'sim5':'20',
>     'sim7':'21',
>     'sim9':'22',
>     'sim11':'23',
>     'sim13':'24'
> }

Then, you can define your new model

in a model dict <i><b>conf_dict</b></i> so that it can be called by name of the model.

Then, you need to define the real function in a function like this:

`
def single_withoutstop_steplen_sim():
    rankpara = {
    ...
    }
    return rankpara

`
You can copy one of existing model configuration to make your new one.

## Ranking Model

All ranking models are implemented in a sub directory <b>.\\context</b>

They are call by the function <b>RankPara(rankpara)</b> in the <b>sxpdorank.py </b>

In this function, each model to be tested is in <b>testset.</b>.

For each such a testing model, a function is called:

`
run_one_rankmodel(pickle_path,pk_sys_set,system_path,system_id,eachtest,rankpara)
`

In <b>run_one_rankmodel</b>, you need to add an if-then statement to let your model be called by the model's name:

`        if modeltype == \'sectitle\':
            model = MySecTitleModel(pickle_file,remove_stopwords=remove_stopwords)
`

For each your model, a python package file is implemented with a class named in your model name being implemented in the package file:

For example, MySectitleNetwork.py will be the model for mysectitlenetwork. 

All running stuffs are implemented in __init__() function of the model class.


###Keyword Tree Evaluation

The following is to build keyword tree and compare model sentences withe the keyword tree

`    
    if cmdstr == "keytree":

        MakeAllFileCSV('single_withoutstop')

        print GetModSysFileNames('single_withoutstop','keywordfile')[0]

        TestBuildTree() #first build tree

        TestRankNetwork() #sec rank nodes on the tree

        TestGraphScore() # test evaluation, now they are all test ok

        CompareTopkWithKeyword('single_withoutstop',buildtree=False)
`


##DUC 2002:

./paper/duc/* original documents selected from DUC 2002, sentences are separated by '*****'

./paper/duc/txt: pure model txt of the raw data of duc 2002 news. This is to be used to produce model_html.

./paper/duc/model_html: produced model files for summarization for each doc in ./paper/duc/txt

./paper/duc/pickle: produce network data for each doc in our collection, which can be loaded and iteratative models can be applied for ranking sentences.

##ACL 2014 Paper Collection

./paper/papers/* original documents selected from the ACL2014 Proceedings

./paper/papers/txt: pure txt of abstraction and conclusion of the raw data of the ACL2014 Proceedings.

./paper/papers/model_html: produced model files for summarization for each doc in  the ACL2014 Proceedings

./paper/papers/pickle: produce network data for each doc in our collection, which can be loaded and iteratative models can be applied for ranking sentences.

## Single Paper Collection

    modelpath = r'.\paper\single\model': summarization model of the paper

    pkpath = r'.\paper\single\pk': structural graph data of the paper

    fname = r'.\paper\single\testdimension_2.txt', raw paper text


# To Run Code

All codes are starting from the __main__() function

`
sxpACLPaperAnalysis.py: This is to parse the ACL 2014 Proceedings Text.

sxpParseDUCText.py: This is to parse structural graph from the DUC collections.

sxpParseSinglePaper.py: This is to parse the single paper structure.

`


