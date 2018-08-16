#-------------------------------------------------------------------------------
# Name:        sxpJudgeCharacter
# Purpose:     This is the package for judging a character is a text or something else
#
# Author:      sunxp
#
# Created:     04/02/2015
# Copyright:   (c) sunxp 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------
# -*- coding:GBK -*-
## -*- coding=utf-8 -*-
import re
import sxpTestStringEncode
import urlparse
def is_chinese(uchar):
##        """判断一个unicode是否是汉字"""
        if uchar >= u'\u4e00' and uchar<=u'\u9fa5':
                return True
        else:
                return False

def is_number(uchar):
##        """判断一个unicode是否是数字"""
        if uchar >= u'\u0030' and uchar<=u'\u0039':
                return True
        else:
                return False

def is_alphabet(uchar):
##         """判断一个unicode是否是英文字母"""
        if (uchar >= u'\u0041' and uchar<=u'\u005a') or (uchar >= u'\u0061' and uchar<=u'\u007a'):
                return True
        else:
                return False

def is_other(uchar):
##         """判断是否非汉字，数字和英文字符"""
        if not (is_chinese(uchar) or is_number(uchar) or is_alphabet(uchar)):
                return True
        else:
                return False

def B2Q(uchar):
##         """半角转全角"""
        inside_code=ord(uchar)
        if inside_code<0x0020 or inside_code>0x7e:      #不是半角字符就返回原来的字符
                return uchar
        if inside_code==0x0020: #除了空格其他的全角半角的公式为:半角=全角-0xfee0
                inside_code=0x3000
        else:
                inside_code+=0xfee0
        return unichr(inside_code)

def Q2B(uchar):
##         """全角转半角"""
        inside_code=ord(uchar)
        if inside_code==0x3000:
                inside_code=0x0020
        else:
                inside_code-=0xfee0
        if inside_code<0x0020 or inside_code>0x7e:      #转完之后不是半角字符返回原来的字符
                return uchar
        return unichr(inside_code)



def stringQ2B(ustring):
##         """把字符串全角转半角"""
        return "".join([Q2B(uchar) for uchar in ustring])

def uniform(ustring):
##         """格式化字符串，完成全角转半角，大写转小写的工作"""
        return stringQ2B(ustring).lower()

def string2List(ustring):
##         """将ustring按照中文，字母，数字分开"""
        retList=[]
        utmp=[]
        for uchar in ustring:
                if is_other(uchar):
                        if len(utmp)==0:
                                continue
                        else:
                                retList.append("".join(utmp))
                                utmp=[]
                else:
                        utmp.append(uchar)
        if len(utmp)!=0:
                retList.append("".join(utmp))
        return retList
def string2ListChinese(ustring, keepnonchinese=False):
##         """将ustring按照中文，非中文分开,只保留中文字符，不保留其他字符"""
        retList=[]
        utmp=[]
        dtmp=[]
        for uchar in ustring:
                if not is_chinese(uchar):
                        if len(utmp)==0 and len(dtmp)==0:
                                continue
                        else:
                                if len(utmp) !=0:
                                    retList.append("".join(utmp))
                                    utmp=[]
                                dtmp.append(uchar)
                else:
                        if keepnonchinese==True:
                            if len(dtmp) !=0:
                                retList.append("".join(dtmp))
                            dtmp = []
                        utmp.append(uchar)
        if len(utmp)!=0:
                retList.append("".join(utmp))
        if len(dtmp) !=0:
                retList.append("".join(dtmp))
        return retList
def ReplaceNonEnglishCharacter(str):
#    print type(str)
    if isinstance(str, unicode) == True:
        unc = str;
    else:
        unc =sxpTestStringEncode.strdecode(str,'utf-8')
    p = re.compile(ur"([^\x00-\xff])")

    def func(m):
        st = repr(m.group(1).title())
        st = ' ' + st + ' '
        return st
    g = p.sub(func, unc)
    return g
def Test():
    #test uniform
    ustring=u'中国 人“名”ａ高频,3..Ａ‣'
    ustring=uniform(ustring)
    ret=string2ListChinese(ustring,True)
    for ch in ret:
        print ch

def Test1():
    str = "12ab,:a啊中国‣"
    ustr = sxpTestStringEncode.strencode(str,'utf-8')
    unc =sxpTestStringEncode.strdecode(str,'utf-8')
    print type(ustr)
    print type(unc)
    #print ustr
    print ustr.decode('utf-8')
    print repr(ustr.decode('utf-8'))

    p = re.compile(ur"([^\x00-\xff])")

    def func(m):
        st = repr(m.group(1).title())

        st = ' ' + st + ' '
        return st
    print 'sub begin:'

    g= p.sub(func, unc)
    print 'sub result:'
    print g.decode('utf-8')
    #print unc.encode('utf-8')

#    g = re.match(ur"([\u4e00-\u9fa5]+)",ustr.decode('utf-8'))
#    g = re.search(ur"([^\w]+)",ustr.decode('utf-8'))
#    g = re.search(ur"([\u4e00-\u9fa5]+)",ustr.decode('utf-8'))
    g = re.search(ur"([^\x00-\xff]+)",ustr.decode('utf-8'))
    if g is not None:
        for g in g.groups():
            print g
    else:
        print g

if __name__=="__main__":
    Test1()
        #test Q2B and B2Q
##        for i in range(0x0020,0x007F):
##                print Q2B(B2Q(unichr(i))),B2Q(unichr(i))
