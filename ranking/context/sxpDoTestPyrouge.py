#-------------------------------------------------------------------------------
# Name:        sxpDoTestPyrouge
# Purpose:
#
# Author:      kgxp
#
# Created:     10-11-2015
# Copyright:   (c) kgxp 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import matplotlib.pyplot as plt
import matplotlib.colors
import numpy as np
import sxpTimeManage
from pyrouge import Rouge155
from pyrouge import MyRouge155

import subprocess
from subprocess import check_output
import sxpReadFileMan
import xlrd
import xlsxwriter
import os
import re
import codecs

def Test():
    r = Rouge155()
    #SL.P.10.R.11.SL062003-01.html
    #SL.P.10.R.11.SL062003-(\d+).html
    r.system_dir = r'D:\Python27\Lib\site-packages\pyrouge\tests\data\systems'
    #SL.P.10.R.A.SL062003-01.html,
    #SL.P.10.R.[A-Z].SL062003-#ID#.html
    r.model_dir = r'D:\Python27\Lib\site-packages\pyrouge\tests\data\models'
    r.system_filename_pattern = 'SL.P.10.R.11.SL062003-(\d+).html'
    r.model_filename_pattern = 'SL.P.10.R.[A-Z].SL062003-#ID#.html'

    output = r.evaluate()
    print(output)
    output_dict = r.output_to_dict(output)


def CallMyPyrouge(system_path,model_path,modelpattern,systempattern,output_fname,system_id):
    conf_path = r'D:\pythonwork\code\paperparse\paper\rouge_conf.xml'
    perlpathname=r'D:\Perl\bin\perl'
    print system_path, systempattern,modelpattern
    output_set = []
    output = RunPaperMyRougeHtml(system_path,model_path,modelpattern,systempattern,conf_path,perlpath = perlpathname,system_idstr=system_id)
    output_set.append(output)
    output_fname = os.path.join(system_path,output_fname)
    sxpReadFileMan.StoreSxptext(output_set,output_fname)
    sxpReadFileMan.WriteStrFile(output_fname+'.txt',output,'utf-8')

def RunPaperMyRougeHtml(system_path,model_path,modelpattern,systempattern,config_file_path = None,perlpath='d:\\Perl\\bin\\perl',system_idstr=['None']):
    r = MyRouge155()
    #SL.P.10.R.11.SL062003-01.html
    #SL.P.10.R.11.SL062003-(\d+).html
    r.system_dir =system_path # r'D:\Python27\Lib\site-packages\pyrouge\tests\data\systems'
    #SL.P.10.R.A.SL062003-01.html,
    #SL.P.10.R.[A-Z].SL062003-#ID#.html
    #P14-1007.xhtml.A.html
    #P14-1007.xhtml.01.html
    r.config_file = config_file_path
    r.model_dir =  model_path #r'D:\Python27\Lib\site-packages\pyrouge\tests\data\models'
    r.system_filename_pattern = systempattern#'SL.P.10.R.11.SL062003-(\d+).html'
    r.model_filename_pattern = modelpattern # 'SL.P.10.R.[A-Z].SL062003-#ID#.html'
#    evaluate(self, system_id=1,conf_path = None, PerlPath =r'D:\Perl\bin\perl', rouge_args=None )
    output= r.evaluate(system_id=system_idstr,conf_path = config_file_path, PerlPath =perlpath)
    print(output)
    output_dict = r.output_to_dict(output)
    return output
def TestDUC():
    pickle_path =  r'D:\pythonwork\code\paperparse\paper\papers\duc\txt\pickle'
    model_path =   r'D:\pythonwork\code\paperparse\paper\papers\duc\txt\model_html'
    system_path =  r'D:\pythonwork\code\paperparse\paper\papers\duc\txt\system_html1'

    modelpattern = r'D\d\d\d.P.100.[A-Z].[A-Z].#ID#.html'
    systempattern = r'^(\w+-\w+).html'
#    system_id =['01','02','03','04','05','06','07']
    system_id =['01','02','03','04','05','08']
    output_fname = "output_set_model1_3_5.pk"
    CallMyPyrouge(system_path,model_path,modelpattern,systempattern,output_fname,system_id)
def TestExcAB():
    pickle_path = r'D:\pythonwork\code\paperparse\paper\papers\pickle'
    model_path =  r'D:\pythonwork\code\paperparse\paper\papers\model_html' #a,b
    system_path = r'D:\pythonwork\code\paperparse\paper\papers\system_html4'

    modelpattern = r'P14-#ID#.xhtml.[A-Z].html'
    systempattern = r'^P14-(\d+).xhtml.html'
    system_id =['01','02','03','04','05','06','07','08']
    system_id =['03','04','08']
    system_name = 'exc'+'_'.join(system_id)+'.pk'
    output_fname = system_name#"output_set_model1_inc.pk"
    CallMyPyrouge(system_path,model_path,modelpattern,systempattern,output_fname,system_id)
def TestIncAB():
    pickle_path = r'D:\pythonwork\code\paperparse\paper\papers\pickle'
    model_path =  r'D:\pythonwork\code\paperparse\paper\papers\model_html' #a,b
    system_path = r'D:\pythonwork\code\paperparse\paper\papers\system_html5'

    modelpattern = r'P14-#ID#.xhtml.[A-Z].html'
    systempattern = r'^P14-(\d+).xhtml.html' #note that in real dir, .0[1-7] is appended to the systempattern for the model id
#    system_id =['01','02','03','04','05','06','07','08']
    system_id =['03','04','08']
    system_name = 'inc'+'_'.join(system_id)+'.pk'
    output_fname = system_name#"output_set_model1_inc.pk"
    CallMyPyrouge(system_path,model_path,modelpattern,systempattern,output_fname,system_id)
def TestIncABSelect():
    pickle_path = r'D:\pythonwork\code\paperparse\paper\papers\pickle'
    model_path =  r'D:\pythonwork\code\paperparse\paper\papers\model_html' #a,b
    system_path = r'D:\pythonwork\code\paperparse\paper\papers\system_html5'

    modelpattern = r'P14-#ID#.xhtml.[A-Z].html'
    systempattern = r'P14-(\d+).xhtml.html.0[1-7]'
#    system_id =['01','02','03','04','05','06','07']
    system_id =['03','05','08']
    output_fname = "output_set_model1_3_5.pk"
    CallMyPyrouge(system_path,model_path,modelpattern,systempattern,output_fname,system_id)
def WriteRougeScoreToExcel():
    writemode = 'exc_paper'

    if writemode == "exc_paper":
        pkname = r'D:\pythonwork\code\paperparse\paper\papers\system_html4\output_set_model_exc.pk'
        fhead = 'exc_paper'
        ProcessRougeScore(fhead,pkname)
    writemode = 'inc_paper'
    if writemode == 'inc_paper':
        pkname = r'D:\pythonwork\code\paperparse\paper\papers\system_html5\output_set_model1_3_5.pk'
        fhead = 'inc_paper'
        ProcessRougeScore(fhead,pkname)
def TestParseMultiSysOutputInc():
    fname = r'D:\pythonwork\code\paperparse\paper\rouge_acl_inc.txt'
    system_id_set={'01':{},'02':{},'03':{},'04':{},'05':{},'06':{},'07':{},'08':{}}
    system_id_set_result =ParseMultiSysOutput(fname,system_id_set)
    pkname = fname+'.pk'
    sxpReadFileMan.StoreSxptext(system_id_set_result,pkname)
    ProcessRougeScore('rouge_acl_inc',pkname)
def TestParseMultiSysOutputExc():
    fname = r'D:\pythonwork\code\paperparse\paper\rouge_acl_exc.txt'
    system_id_set={'01':{},'02':{},'03':{},'04':{},'05':{},'06':{},'07':{},'08':{}}
    system_id_set_result =ParseMultiSysOutput(fname,system_id_set)
    pkname = fname+'.pk'
    sxpReadFileMan.StoreSxptext(system_id_set_result,pkname)
    ProcessRougeScore('rouge_acl_excc',pkname)
def TestParseMultiSysOutputDUC():
    fname = r'D:\pythonwork\code\paperparse\paper\rouge_duc.txt'
    system_id_set={'01':{},'02':{},'03':{},'04':{},'05':{},'08':{}}
    system_id_set_result =ParseMultiSysOutput(fname,system_id_set)
    pkname = fname+'.pk'
    sxpReadFileMan.StoreSxptext(system_id_set_result,pkname)
    ProcessRougeScore('rouge_duc',pkname)

def TestLoadParseWriteRougeScoreIntoExcel():
    fname = r'D:\pythonwork\code\paperparse\paper\rouge_acl_exc.txt'
    pkname = fname+'.pk'
    ProcessRougeScore('rouge_acl_exc',pkname)

def ParseMultiSysOutput(fname,system_id_set):
    txt = sxpReadFileMan.ReadTextUTF(fname)
  #  print txt
    recall_pattern = re.compile(r'(\d\d) (ROUGE-\S+) (Average_\w):\s+(\d.\d+)\s+' +   r"\(95%-conf.int. (\d.\d+) - (\d.\d+)\)")
    for line in txt.split("\n"):
        print line
        match = recall_pattern.match(line)
        if match:
            sys_id, rouge_type, metric, result, conf_begin, conf_end = \
                match.groups()
            print sys_id,rouge_type, metric, result, conf_begin, conf_end
            if rouge_type in system_id_set[sys_id]:
                a = system_id_set[sys_id][rouge_type]
                if a is None:
                    a = []
            else:
                a = []
            a.append([metric,result, conf_begin, conf_end])
            system_id_set[sys_id][rouge_type]=a
    return system_id_set
def ProcessRougeScore(fhead,pkname):
    ds = sxpReadFileMan.LoadSxptext(pkname)
    print ds
    modelname = {'01':'Para','02':'TFIDF','03':'GS','04':'GW',
    '05':'Context','06':'Section','07':'SecContext','08':'GW_Context'}
    plotmodel = ['04','02','03','01','05','08']
    metric_set = [
    ['ROUGE-1','Average_P','Average_R','Average_F'],
    ['ROUGE-2','Average_P','Average_R','Average_F'],
    ['ROUGE-3','Average_P','Average_R','Average_F'],
    ['ROUGE-4','Average_P','Average_R','Average_F'],
    ['ROUGE-L','Average_P','Average_R','Average_F']
    ]
    nsection = 1
    nrow = nsection+1
    nc = 1
    coorname = ['precision','recall','f-score']
    xname = fhead + 'rouge_score.xls'
    fname = r'D:\pythonwork\code\paperparse\paper'+'\\'+xname
    try:
        workbook = xlsxwriter.Workbook(fname)
        worksheet = workbook.add_worksheet()
        for em in metric_set:# weplot one bar figure
            title = em[0]
            colorset = ['r','b','g','c','m','y','k']
            value = str(title)
            row = nsection
            col = 0
            for ic in range(len(em)):
                value = str(em[ic])
                worksheet.write(row, col+ic, value)
            dataset= []
            metric_name = em[1:]

            i = 0
            #for figure rouge-1, we need to get
            #input = [['v1',[0.8,0.9,0.85],['tfidf',[0.3,0.2,0.4]]]
            print title
            for eachmodel in plotmodel:#for 7 models, we extract each model's metric
            #for tfidf model
                #this is the name 'tfidf'
                legendname  = modelname[eachmodel]
                value = str(legendname)
                row = row + 1
                col = 0
                print '1write',row,col,value
                worksheet.write(row, col, value)

                datarow = []
                for eachm in metric_name:
                    row = row
                    col = col + 1
                    result_set =ds[eachmodel][title]
                    for each_m in result_set:
                        if each_m[0]== eachm:
                            value =str(each_m[1]) #avergage score, not confidence value)
                            print '2write',row,col,value
                            worksheet.write(row, col, value)
                            datarow.append(float(value))
                dataset.append([legendname, datarow])
                i = i + 1
            nsection = row + 2
            print dataset
       #     PlotBarFromCoordSet(title,dataset,coorname,colorset)
            plt.savefig(fhead + title+'.jpg')
        workbook.close()
    except Exception as e:
        print 'error in writing excel',e
def TestDUCPyrougeNew():
    system_dir = r'D:\pythonwork\code\paperparse\paper\papers\duc\txt\system_html'
    model_dir = r'D:\pythonwork\code\paperparse\paper\papers\duc\txt\model_html'
    perpathname ='perl'
    conf_path = r'D:\pythonwork\code\paperparse\paper\papers\duc\rouge_conf.xml'
    filelist,subdir = sxpReadFileMan.GetDir(system_dir)
    print system_dir
    print subdir
    output_set = []
    modelpattern = r'D\d\d\d.P.100.[A-Z].[A-Z].#ID#.html'
    for eachdir in subdir:
        system_dir_sub = system_dir + '\\' + eachdir
        systempattern = r'D\d\d\d.P.100.[A-Z].[A-Z].(\w+-\w+).html'
        print system_dir_sub, systempattern,modelpattern
        try:
            output = RunPaperRougeHtml(system_dir_sub,model_dir,modelpattern,systempattern,config_file_path = conf_path, perlpath=perpathname )
            output_set.append(output)
        except Exception as e:
            print eachdir,e

    output_fname = system_dir + '\\output_set.pk'
    sxpReadFileMan.StoreSxptext(output_set,output_fname)
    rouge_score = sxpReadFileMan.LoadSxptext(output_fname)
    fhead = 'duc_'
    ProcessDUCRougeScore(rouge_score,fhead)
def main():
    test = 'exc_test_ab'
    if test == 'exc_test_ab':
        TestExcAB()
    test = 'inc_test_ab'
    if test == 'inc_test_ab':
        TestIncAB()
##    if test == 'select':
##        TestIncABSelect()
    if test == 'writeexcl':
        WriteRougeScoreToExcel()
    if test == 'parserougeout':
        TestParseMultiSysOutputInc()
        TestParseMultiSysOutputExc()
      #  TestLoadParseWriteRougeScoreIntoExcel()
    if test == 'duc':
        TestDUC()
    if test == 'duc_excel':
        TestParseMultiSysOutputDUC()
if __name__ == '__main__':
    main()
