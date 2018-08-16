#-------------------------------------------------------------------------------
# Name:        sxpTextEncode
# Purpose:
#
# Author:      sunxp
#
# Created:     22-03-2015
# Copyright:   (c) sunxp 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#coding=utf-8
import codecs
import urllib
def DetermineCode(s):
    typeset = GetTestTypeCode(s)
    for t in typeset:
        if t[1] == 'ok':
            return t[0]
    ignore = True;
    itypeset = GetTestTypeCode(s,ignore)
    for t in typeset:
        if t[1] == 'ok':
            return t[0]
    return 'ascii';
def GetTestTypeCode(s,ignore = False):
    typeset =[]
    if isinstance(s,unicode) == True:
       d = ('utf-8','ok',s)
       typeset.append(d)
       return typeset
    else:
        codetype =['utf-8','gbk','gb2311']
        for ctype in codetype:
            try:
                if ignore == False:
                    us = unicode(s,ctype)
                else:
                    us = unicode(s,ctype,'ignore')
                d = (ctype,1,us)
                typeset.append(d)
    #            print d;
            except Exception as e:
                d = (ctype,0,s)
                typeset.append(d)
    return typeset;
def GetGBKStr(s):
    us = GetUnicode(s);
    if us[0]=='utf-8':
        gs = us[1].encode('gbk');
    else:
        return s;
    return gs
def GetURLEncode(urlstr):
    gs = sxpTextEncode.GetUnicode(urlstr)
    gss = gs.encode('gbk')
    return urllib.quote(gss,':./=?%!&$')

def GetUnicode(s):
    if isinstance(s,unicode):
        return s;
    typeset = GetTestTypeCode(s)
    restr = None
    for t in typeset:
        if t[1] == 1 and t[0] == 'utf-8':
            restr = t[2];
            break;
        elif t[1] == 1:
            restr = t[2];
    return restr;
def GetUnicodePair(s):
    if isinstance(s,unicode):
        restr = ['utf-8',s];
        return restr;
    typeset = GetTestTypeCode(s)
    restr = ['', s]
    for t in typeset:
        if t[1] == 1 and t[0] == 'utf-8':
            restr = ['utf-8',t[2]];
            break;
        elif t[1] == 1:
            restr = [t[0],t[2]];
    return restr;
def GetPrintUTFStr(s):
    if isinstance(s,unicode):
        restr = ['utf-8',s];
        return restr;
    typeset = GetTestTypeCode(s)
    restr = ['utf-8',s];
    for i in range(len(typeset)):
            t = typeset[i]
            if t[1] == 1 and t[0] == 'utf-8':
                u = t[2]
                if isinstance(u,unicode)==False:
                    restr = ['utf-8',unicode(u,t[0])]
                else:
                    restr =['utf-8',u]
                break;
            elif t[1] == 1:
                u = t[2]
                if isinstance(u,unicode)==False:
                    restr = (t[0],unicode(u,t[0]))
                else:
                    restr = ['utf-8',u]
    return restr
def GetPrintUTFStrA(s):
    if isinstance(s,unicode):
        return s;
    typeset = GetTestTypeCode(s)
    restr = s;
    for i in range(len(typeset)):
            t = typeset[i]
            if t[1] == 1 and t[0] == 'utf-8':
                restr = t[2]
                if isinstance(restr,unicode)==False:
                    restr = unicode(restr,t[0])
    return restr

def TestTypeA():
    s = u'哈哈'
    us = GetPrintUTFStr(s)
    print us[0],us[1], isinstance(us[1],unicode)
    uss = GetUnicodePair(s)
    print uss[0], uss[1], isinstance(uss[1],unicode)
    print GetGBKStr(s)
    print '*****'
    s= r'雷军vs周鸿祎，20年的&quot;天地对决&quot;'
    us = GetPrintUTFStr(s)
    print us[0],us[1], isinstance(us[1],unicode)
    uss = GetUnicodePair(s)
    print uss[0], uss[1], isinstance(uss[1],unicode)
    gs = GetGBKStr(s)
    print gs;
    ugs = GetUnicodePair(gs)
    print ugs[1]
    ug = GetUnicode(gs)
    print ug

def main():
    TestTypeA()

if __name__ == '__main__':
    main()
