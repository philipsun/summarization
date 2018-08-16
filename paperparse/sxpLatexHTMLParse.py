#-------------------------------------------------------------------------------
# Name:        sxpLatexHTMLParse
# Purpose:
#
# Author:      sunxp
#
# Created:     23/03/2015
# Copyright:   (c) sunxp 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#coding=UTF-8
from HTMLParser import HTMLParser
from re import sub
from sys import stderr
from traceback import print_exc
import sxpTestStringEncode
import codecs
import urllib
import socket
import sxpTextEncode
import sxpIsCharacter
import sxpLogger
import os

class sxpTextPara:
    text = ''
    type = ''
    index = ''

paperpath = r'D:\pythonwork\code\paperparse'

class sxpLatexHtmlPaper(HTMLParser):
    include_it = False
    unit_index = 0;
    text_type = 'p'
    text_set = []
    text_para = False;
    text_content = ''
    logfilename  = r'D:\pythonwork\code\paperparse\latexpaper.log'
    rootpath =  r'D:\pythonwork\data\baidunews'
    reference_id = 0;
    reference_set = []
    isendtag = False
    def __init__(self):
        HTMLParser.__init__(self)
        self.__text = []
        self.unit_index = 0;
        self.starttag = ''
        self.startendtag = ''
        self.text_set = []
        self.text_para = False
        self.isendtag = False
    def initText(self,rpath):
        if not os.path.exists(rpath):
            print('create the path first')
            os.path.os.mkdir(rpath);
        self.rootpath =  rpath
        self.logfilename  = rpath+'\\'+'latexpaper.log'

    def handle_data(self, data):
        text = data.strip()
        HTMLParser.handle_data(self, data)
        if len(text) > 0 :
            if self.skiptag(self.starttag):
                return;
            text = sub('[ \s\t\r\n]+', ' ', sxpTestStringEncode.strdecode(text))
            self.__text.append(text)
#           print self.startendtag,':st-end:',self.starttag,':st:',text,'\n\n'
    def skiptag(self, tagstr):
        if tagstr == 'script':
            return True
        elif tagstr == 'style':
            return True
        elif tagstr == 'code':
            return True
##        elif tagstr == 'sup':
##            return True
##        elif tagstr == 'span':
##            return True
        return False;

    def handle_starttag(self, tag, attrs):
        self.isendtag = False
        HTMLParser.handle_starttag(self, tag, attrs)

    # Overridable -- handle end tag
    def handle_endtag(self, tag):
        self.isendtag = True;
        pass

    def handle_startendtag(self, tag, attrs):
        self.startendtag = tag;
        if tag == 'br':
            self.__text.append('\n\n')
            self.include_it = True
        HTMLParser.handle_startendtag(self, tag, attrs)
    def ispara(self,tagstr):
        taglist = ['body','p','br','div','span','li','tr','td']
        if tagstr in taglist:
            return True;
        else:
            return False

    def text(self):
        ttext = ' '.join(self.__text).strip()
        self.text_content = sub('[\n]+', '\n', ttext)
        return self.text_content
    def savefiletext(self,fname,text):
        try:
            uc = sxpTestStringEncode.strdecode(text)
            f = codecs.open(fname,'w+','utf-8')
            #uc = sxpIsCharacter.toUTF(content)
            #uc = unicode(content,'gbk','ignore').encode('gkb','ignore')
            #uc = content.decode('gbk','ignore').encode('gbk','ignore')
            #uc = unicode(content, 'gbk')
            #uc = sxpIsCharacter.toGBK(content)
            #if using GetUnicode, it will be written
            f.write(uc)
            f.close()
        except Exception as e:
            msg = 'file:{0}:{1}'.format(fname,e)
            sxpLogger.logThisMessageStr(self.logfilename,msg)
            print msg;
    def savefile(self,fname):
        try:
            uc = sxpTestStringEncode.strdecode(self.text_content)
            f = codecs.open(fname,'w+','utf-8')
            #uc = sxpIsCharacter.toUTF(content)
            #uc = unicode(content,'gbk','ignore').encode('gkb','ignore')
            #uc = content.decode('gbk','ignore').encode('gbk','ignore')
            #uc = unicode(content, 'gbk')
            #uc = sxpIsCharacter.toGBK(content)
            #if using GetUnicode, it will be written
            f.write(uc)
            f.close()
        except Exception as e:
            msg = 'file:{0}:{1}'.format(fname,e)
            sxpLogger.logThisMessageStr(self.logfilename,msg)
            print msg;

    def handle_dataA(self, data):
        text = data.strip()
        if len(text) > 0 :
            text = sub('[ \t\r\n]+', ' ', sxpTestStringEncode.strdecode(text))
            print self.startendtag,':st-end:',self.starttag,':st:',text,'\n\n'

            self.__text.append(text +':'+ self.starttag+': ')
            self.include_it = False;
            self.unit_index =self.unit_index + 1;
            self.starttag = '';
    def handle_dataB(self, data):
        text = data.strip()
        if len(text) > 0 :
            if self.skiptag(self.starttag):
                return;
            else:
                text  = sub('[ \t\r\n]+', ' ', sxpTestStringEncode.strdecode(text))
                if len(text)==0 or text == ' ' or not text:
                    return;
                txtu = sxpTextUnit()
                txtu.text_content = text;
                print self.startendtag,':st-end:',self.starttag,':st:',text,'\n\n'
                txtu.texttypeA = self.starttag
                txtu.texttypeB = self.startendtag
                txtu.text_index = self.unit_index
                self.text_set.append(txtu)
                self.unit_index =self.unit_index + 1;
    def handle_starttagA(self, tag, attrs):
        self.include_it = True
        if tag == 'p':
            self.__text.append('\n\n')
            self.include_it = True
            self.text_type = 'p'
        elif tag == 'br':
            self.__text.append('\n')
            self.include_it = True
            self.text_type = 'p'
        elif tag == 'div':
             self.__text.append('\n')
             self.include_it = True
             self.text_type = 'p'
        elif tag == 'span':
             self.__text.append('\n')
             self.include_it = True
             self.text_type = 'p'
        if tag == 'script':
            self.include_it = False
        elif tag == 'style':
            self.include_it = False
    def RetrieveWeb(self, urlstr):
        timeout = 6
        try:
            socket.setdefaulttimeout(timeout)
            sock = urllib.urlopen(urlstr)
            #sock = urllib2.urlopen()
            urlcontent = sock.read()
            sock.close()
        except Exception as e:
            print('failed to access the web page')
            strmsg = '{0}:{1}:{2}'.format('RetrieveWeb',urlstr,e)
            print strmsg
            return 0
        return urlcontent;

def parsesave(self,fname):
    try:
        f = codecs.open(fname,'r+','utf-8')
        #uc = sxpIsCharacter.toUTF(content)
        #uc = unicode(content,'gbk','ignore').encode('gkb','ignore')
        #uc = content.decode('gbk','ignore').encode('gbk','ignore')
        #uc = unicode(content, 'gbk')
        #uc = sxpIsCharacter.toGBK(content)
        #if using GetUnicode, it will be written
        urltext = f.read()
        f.close()
        parser = _DeHTMLParser()
        parser.feed(urltext)
        parser.close()
        parser.savefilet(fname)
    except Exception as e:
        msg = 'file:{0}:{1}'.format(fname,e)
        sxpLogger.logThisMessageStr(self.logfilename,msg)
        print msg;
def dehtml(text):
    parser = sxpLatexHtmlPaper()
    parser.feed(text)
    parser.close()
    return parser.text()


def testtext():
    text = r'''''
        <html>
            <body>
                <b>Project:</b> DeHTML<br>
                <b>Description</b>:<br>
                This small script is intended to allow conversion from HTML markup to
                plain text.
            </body>
            <script>function {}</script>
            <style> cccs </style>
        </html>
    '''
    print(dehtml(text))
def testtext1():
    text = r'''
        <html>
            <body>
               <b>Project:</b> DeHTML<br>
                <b>Description</b>:<br>
                This small script is intended to allow conversion from HTML markup to
                plain text.
                <li><a href="http://pinyin.sogou.com/">输入法</a></li>
            </body>
            <script>function {}</script>
            <div class="c-abstract">本文实例讲述了<em>Python单链表</em>的简单实现方法,分享给大家供大家参考。具体方法如下:通常来说,要定义一个单链表,首先定义<em>链表元素</em>:Element.它包含3个字段:...</div>
            <style> cccs </style>
        </html>
    '''
    print(dehtml(text))
def testlatex():
    text = r'''
        <p class="ltx_p">An <math xmlns="http://www.w3.org/1998/Math/MathML" id="S3.SS3.p1.m1" class="ltx_Math" alttext="n" display="inline"><mi>n</mi></math>-best list reflects a tiny portion of a decoder’s search space, typically fixed at 1000 hypotheses.
    Lattices<span class="ltx_note ltx_role_footnote"><sup class="ltx_note_mark">2</sup><span class="ltx_note_outer"><span class="ltx_note_content"><sup class="ltx_note_mark">2</sup>Or forests for hierarchical and syntactic decoders.</span></span></span> can represent an exponential number of hypotheses
    in a compact structure.
    In this section, we discuss how a lattice from a multi-stack phrase-based decoder such as Moses <cite class="ltx_cite">[<a href="#bib.bib16" title="Moses: open source toolkit for statistical machine translation" class="ltx_ref">17</a>]</cite> can be desegmented
    to enable word-level features.</p>
    '''
    print(dehtml(text))

def testurl():
    url = r'http://www.sohu.com/'
    parser = sxpLatexHtmlPaper()
    rpath = r'D:\pythonwork\data\baidunews\taskset\1\text'
    parser.initText(rpath)
    text = parser.RetrieveWeb(url)

    utext = sxpTestStringEncode.strdecode(text)
    parser.feed(utext)
    parser.close()
    print parser.text()
    fname = r'D:\pythonwork\data\baidunews\taskset\1\text' + '\\' + '1.txt'
    parser.savefiletext(fname,parser.text_content)

def ParseHTMLContentStr(text):
    parser = sxpLatexHtmlPaper()
    parser.feed(text)
    parser.close()
    return parser.text()

def main():
    #testlatex()
    #testurl()
    testlatex()
if __name__ == '__main__':
    main()
