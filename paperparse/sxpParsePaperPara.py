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
import sxpLoadWeb

class sxpTextPara:
    text = ''
    type = ''
    index = ''

paperpath = r'D:\pythonwork\code\paperparse'

class sxpExtractPara(HTMLParser):
    include_it = False
    unit_index = 0;
    text_type = 'p'
    para_set = []
    text_content = ''
    logfilename  = r'D:\pythonwork\code\paperparse\latexpaper.log'
    rootpath =  r'D:\pythonwork\data\baidunews'

    isendtag = False
    process_para = None;
    inner_tag = ['span','div','em','cite','a','math','sup']
    include_inner = None
    para_text = u''
    in_innertag = 0
    def __init__(self):
        HTMLParser.__init__(self)
        self.__text = []
        self.para_set = []
        self.inner_tag = ['em'] #['span','div','cite','a','math']
        self.include_inner = None
        self.para_text = u''
        self.process_para = None
        self.in_innertag = 0
    def initText(self,rpath):
        if not os.path.exists(rpath):
            print('create the path first')
            os.path.os.mkdir(rpath);
        self.rootpath =  rpath
        self.logfilename  = rpath+'\\'+'latexpaper.log'
    def handle_starttag(self, tag, attrs):
        if tag == 'p':
            for name,value in attrs:
                if name=='class' and value=='ltx_p':
                     #means that last para is still not
                    #stored, so first store the last paragraph
                    if len(self.para_text)>0:
                        self.para_text = sub('[ \s\t\r\n]+', ' ', sxpTestStringEncode.strdecode(self.para_text))
                        self.para_set.append(self.para_text)
                        self.para_text = u''
                        self.include_inner = None
                        self.in_innertag = 0
                    self.process_para=tag
                    self.in_innertag = 0
        else:
            #then, it means that it is still inside the paragraph but
            #in another deeper loop
            if self.process_para:
                self.in_innertag = self.in_innertag + 1;
                if tag in self.inner_tag:
                    self.include_inner = tag
                else:
                    self.include_inner = None
            else:
                self.in_innertag = 0;

##        self.isendtag = False
##        HTMLParser.handle_starttag(self, tag, attrs)

    def handle_data(self, data):
        text = data.strip()
        if len(text) > 0 :
            if self.process_para:
                if self.in_innertag > 0:
                    if self.include_inner:
                        text = sub('[ \s\t\r\n]+', ' ', text)
                        self.para_text = self.para_text + ' ' + text
                else:
                    try:
                        self.para_text = self.para_text + ' ' + unicode(text,'utf-8')
                    except Exception as e:
                        print e

    # Overridable -- handle end tag
    def handle_endtag(self, tag):
        if tag==self.process_para:
            self.para_set.append(self.para_text)
            self.para_text = u''
            self.process_para=None
            self.in_innertag = False
            self.include_inner = None

        else:
            if self.in_innertag>0:
                self.in_innertag = self.in_innertag - 1

    def handle_startendtag(self, tag, attrs):

        HTMLParser.handle_startendtag(self, tag, attrs)
    def ispara(self,tagstr):
        taglist = ['body','p','br','div','span','li','tr','td']
        if tagstr in taglist:
            return True;
        else:
            return False

    def text(self):
        ttext = ' '.join(self.para_set).strip()
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
#***************************************************
#*********************This is the main extraction interface
def ExtractParagraph(papersrc):
    parser = sxpExtractPara()
    parser.feed(papersrc)
    parser.close()
    return parser.para_set
#****************************************************
#****************************************************
def TestFileParaExtract():
    fname = r'D:\pythonwork\code\paperparse\paper\papers' + '\\' + 'P14-1007.xhtml'
    papersrc = sxpLoadWeb.LoadFile(fname)
    parser = sxpExtractPara()
    parser.feed(papersrc)
    parser.close()
    for tp in parser.para_set:
        print tp
        print '******'
def TestParaExtract():
    papersrc = '''
    <p class="ltx_p">Example (<a href="#S1.p3.1" title="1 Introduction ‣ Simple Negation Scope Resolution through Deep Parsing: A Semantic Solution to a Semantic Problem" class="ltx_ref"><span class="ltx_text ltx_ref_tag">1</span></a>), where
<math xmlns="http://www.w3.org/1998/Math/MathML" id="S1.p3.m1" class="ltx_Math" alttext="\langle\mbox{}\rangle" display="inline"><mrow><mo>⟨</mo><mrow/><mo>⟩</mo></mrow></math> marks the cue and <math xmlns="http://www.w3.org/1998/Math/MathML" id="S1.p3.m2" class="ltx_Math" alttext="\{" display="inline"><mo>{</mo></math><math xmlns="http://www.w3.org/1998/Math/MathML" id="S1.p3.m3" class="ltx_Math" alttext="\}" display="inline"><mo>}</mo></math> the in-scope elements,
illustrates the annotations, including how
negation inside a noun phrase can scope over discontinuous
parts of the sentence.<span class="ltx_note ltx_role_footnote"><sup class="ltx_note_mark">1</sup><span class="ltx_note_outer"><span class="ltx_note_content"><sup class="ltx_note_mark">1</sup>Our running example is a truncated
variant of an item from the Shared Task training data. The
remainder of the original sentence does not form part of the scope of
this cue.</span></span></span>
<span class="ltx_ERROR undefined">{exe}</span>

<li id="S1.p3.1" class="ltx_item">
<div id="S1.p3.p1" class="ltx_para">
<p class="ltx_p">
'''
    parser = sxpExtractPara()
    parser.feed(papersrc)
    parser.close()
    print parser.text()
##    for tp in parser.para_set:
##        print tp

def ParseHTMLContentStr(text):
    parser = sxpExtractPara()
    parser.feed(text)
    parser.close()
    return parser.text()

def main():
    #testlatex()
    #testurl()
    #TestParaExtract()
    TestFileParaExtract()
if __name__ == '__main__':
    main()
