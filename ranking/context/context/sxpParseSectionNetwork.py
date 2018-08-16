#-------------------------------------------------------------------------------
# Name:        sxpParseSectionNetwork
# Purpose:
#
# Author:      sunxp
#
# Created:     16-11-2015
# Copyright:   (c) sunxp 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------
from sxpPackage import *
import sxpReadFileMan
import numpy as np
from scipy.sparse import csr_matrix
from scipy import *
def ParseSectionNetwork(sxptxt):
    cs = len(sxptxt.section_id_dict)
    c_c = csr_matrix(np.zeros((cs,cs), dtype=np.float))
##    for sxpsec1 in sxptxt.section_list:
##        print sxpsec1.id,sxpsec1.id_set

    for sxpsec1 in sxptxt.section_list:
        int_id1 = sxpsec1.id
        if len(sxpsec1.id_set) == 0:
            continue
        for sxpsec2 in sxptxt.section_list:
            int_id2 = sxpsec2.id
            if len(sxpsec2.id_set) == 0 and int_id1 == 0:
                c_c[0,int_id2] = 1# the last section is an unknown section with no title and section id
##                print 1
##                print int_id2, 'unknown'
##                print int_id1, sxpsec2.id_set
                continue
            if int_id2 == int_id1:
                continue
            prefix_len = CompareTwoIDs(sxpsec1.id_set,sxpsec2.id_set)
            if prefix_len == len(sxpsec1.id_set) and len(sxpsec2.id_set)==len(sxpsec1.id_set) + 1:
                c_c[int_id2,int_id1] = 1
            else:
                if prefix_len == len(sxpsec1.id_set) and len(sxpsec2.id_set)==len(sxpsec1.id_set):
                  c_c[int_id2,int_id1] = 1
##            if c_c[int_id2,int_id1] > 0:
##                print 1
##                print int_id2, sxpsec1.id_set
##                print int_id1, sxpsec2.id_set
    c_c = c_c + c_c.T
    return c_c
def ComputePrefix(sec_id1, sec_id2):
    n1=len(sec_id1)
    n2 = len(sec_id2)
    cl = 0
    if n2 >= n1:
        cl = 0
        for i in range(n1):
            s1 = sec_id1[i]
            s2 = sec_id2[i]
            if s1[0]==s2[0] and s1[1] == s2[1]:
                cl = cl + 1
            else:
                break
    if n2 < n1:
        cl = 0
        for i in range(n2):
            s1 = sec_id1[i]
            s2 = sec_id2[i]
            if s1[0]==s2[0] and s1[1] == s2[1]:
                cl = cl + 1
            else:
                break
    return cl

def CompareTwoIDs(sec_id1,sec_id2):
    n1=len(sec_id1)
    n2 = len(sec_id2)
    if sec_id1[0][0]==u'abstract':
        return 0 #means no coverage and no direct child relation because it is the abstract section
    else:
        if n2<n1:
            return 0
        else:
            if n2 == n1:
                if sec_id1[0][0] == u'top':
                    return 1 #means that the top section belongs to the root of the document, which is section 0
                else:
                    return 0 #means that two sections are both top, so they do not belong to each other
            else:
                dist = ComputePrefix(sec_id1, sec_id2)
                return dist

def TestSection():
    path = r'D:\pythonwork\code\paperparse\paper'
    paper_path = path + '\\papers\\'
    pickle_dir = path + '\\papers\\\pickle\\'
    #get the original filename list in the path variable
    file_list = sxpReadFileMan.GetDirFileList(paper_path)
    i = 0
    for file_name in file_list:
        if sxpReadFileMan.IsType(file_name,'xhtml') == False:
            continue
        print i, file_name
        pickle_path = pickle_dir + file_name + '_3.pickle'
        sxptxt = sxpReadFileMan.LoadSxptext(pickle_path)
        print sxptxt.d_c.shape
        print sxptxt.c_p.shape
        ParseSectionNetwork(sxptxt)
        i = i + 1
def ListSection():
    path = r'D:\pythonwork\code\paperparse\paper'
    paper_path = path + '\\papers\\'
    pickle_dir = path + '\\papers\\\pickle\\'
    #get the original filename list in the path variable
    file_list = sxpReadFileMan.GetDirFileList(paper_path)
    i = 0
    for file_name in file_list:
        if sxpReadFileMan.IsType(file_name,'xhtml') == False:
            continue
        print i, file_name
        pickle_path = pickle_dir + file_name + '_2.pickle'
        sxptxt = sxpReadFileMan.LoadSxptext(pickle_path)
        print sxptxt.d_c.shape
        print sxptxt.c_p.shape
        print sxptxt.c_c.shape
        for eachsec in sxptxt.section_list:
            print eachsec.id, eachsec.id_set, eachsec.id_str

        i = i + 1

def main():
    #TestSection()
    ListSection()

if __name__ == '__main__':
    main()
