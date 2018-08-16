#-------------------------------------------------------------------------------
# Name:        sxpPattern
# Purpose:
#
# Author:      sunxp
#
# Created:     14/10/2015
# Copyright:   (c) sunxp 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#coding=utf-8
import sxpReadFileMan
import sxpTextEncode
import re

class sxpSearchPattern:
    patstr = ''
    pat_name =''
    pat_dic = {}
    def __init__(self):
        self.patstr = ''
        self.pat_name =''
        self.pat_dict = {}
    def AddPat(self, pat_name,patstrset):
        if pat_name in self.pat_dict:
            oldpat = self.pat_dict[pat_name]
            newpat = oldpat.extend(patstrset)
        else:
            self.pat_dict[pat_name] =patstrset

    def UsePat(self, pat_name, s):
        if pat_name in self.pat_dict:
            pat_set = self.pat_dict[pat_name]
            pi =0
            p_list = []
            for eachpat in pat_set:
                pos_date=SearchProcess(eachpat, s, 'y',pat_name,pi)
                if len(pos_date)>0:
                    p_list.append(pos_date)
                pi = pi + 1
            return p_list

        else:
            return None
def SearchSentProcess(patstr, s, pat_name,pi):
    sent_list = SegSent(s)
    sent_pos_list = []
    i = 0;
    for eachs in sent_list:
        sent_pos = SearchProcess(patstr, eachs,'n', pat_name,pi)
        for eachsubpos in sent_pos:
            eachsubpos.extend([i])
            sent_pos_list.append(eachsubpos)
        i  = i + 1
    return sent_pos_list
def SearchProcess(patstr, s, sent='y', pat_name='',pi=0):
    if sent == 'y':
        return SearchSentProcess(patstr,s, pat_name,pi)
    pattern = re.compile(patstr)
    match =pattern.search(s)
    pattern_pos = []
    while match:
        tg = match.groups()
        tgtxt = match.group()
        posd = match.span()
        match = pattern.search(s,posd[1])
        pattern_pos.append([tgtxt,posd,tg,pat_name,pi,0])
    return pattern_pos
def SegSent(s):
    patstr = u',|\.|\:|\?|，|。|：|？|！|；'
    pattern = re.compile(patstr)
    ss = pattern.split(s)
    return ss
def TestSegSent():
    s = u'宝宝十岁了，每天晚上咳嗽夜里睡不好，白天咳嗽轻点吃药已有十天不见好转。到医院拍片说是支气管炎，医生让住院治疗，打点滴8天后夜里咳嗽好转，偶尔咳嗽，医生讲可以出院了并且不要吃药了，在家注意不要受凉，出院一星期目前还是不定期偶尔咳嗽，发现口臭。请指教谢谢！'
    ss = SegSent(s)
    for eachs in ss:
        print eachs
def main():
    TestSegSent()

if __name__ == '__main__':
    main()
