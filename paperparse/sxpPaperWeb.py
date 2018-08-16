#-------------------------------------------------------------------------------
# Name:        sxpPaperWeb
# Purpose:
#
# Author:      sunxp
#
# Created:     30/03/2015
# Copyright:   (c) sunxp 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import re
import os
import urllib
import urllib2
import logging
import random
import datetime
import socket
from datetime import timedelta
from bs4 import BeautifulSoup


paperpath = r'D:\pythonwork\code\paperparse\paper'

import sxpLoadWeb

def getWebPage(urlstr):
    timeout = 5;
    urlcontent = ''
    try:
        socket.setdefaulttimeout(timeout)
        sock = urllib2.urlopen(urlstr)
        #sock = urllib2.urlopen()
        urlcontent = sock.read()
        sock.close()
        return urlcontent
    except Exception as e:
        print('failed to access the web page:',urlstr)
        print(e)
        strmsg = '{0}:{1}'.format(urlstr,e)
        self.logThisMessageStr(self.logfilename, strmsg)
        return urlcontent
##1 find(id='xxx')                                  # 寻找id属性为xxx的
##2 find(attrs={id=re.compile('xxx'), algin='xxx'}) # 寻找id属性符合正则且algin属性为xxx的
##3 find(attrs={id=True, algin=None})
def ParseACL():
    urlstr = r'https://www.aclweb.org/anthology/P/P14'
#    urlstr = r'http://www.knowledgegrid.net'
    paperlistfile = paperpath + '\\' + 'acllist.html'
    print sxpLoadWeb.FetchWeb(urlstr,paperlistfile)

def TestParseFile():
    paperlist = paperpath + '\\' + 'acllist.html'
    urlstr = r'https://www.aclweb.org/anthology/P/P14'
##    ParseACLFile(urlstr,paperlist)
    ParseACLFileSubImg(urlstr,paperlist)
def ParseACLFile(urlstr, fname):
    htmlsrc = sxpLoadWeb.LoadFile(fname)
    print htmlsrc
    soup = BeautifulSoup(htmlsrc)
      #  urllinks = soup.a #this only return the first a tag, and you need to use next to find it
      #  self.urllinks = soup.find_all('a')
#    urlinks = soup.find_all("a", attr = {"href":'P14-2104.xhtml'})
    urlinks = soup.find_all(href=re.compile(".xhtml"))
    if not urlinks:
        print 'none link is obtained'
    i = 't';
    paperdown = r'D:\pythonwork\code\paperparse\paper\papers'
    for ul in urlinks:
        pfname = paperdown + '\\'+ul['href']
        paperulr = urlstr + r'/' + ul['href']
        sxpLoadWeb.FetchWeb(paperulr,pfname)

def ParseACLFileSubImg(urlstr, fname):
    htmlsrc = sxpLoadWeb.LoadFile(fname)
    print htmlsrc
    soup = BeautifulSoup(htmlsrc)
      #  urllinks = soup.a #this only return the first a tag, and you need to use next to find it
      #  self.urllinks = soup.find_all('a')
#    urlinks = soup.find_all("a", attr = {"href":'P14-2104.xhtml'})
    urlinks = soup.find_all(href=re.compile(".xhtml"))
    if not urlinks:
        print 'none link is obtained'
    i = 't';
    paperdown = r'D:\pythonwork\code\paperparse\paper\papers'
    for ul in urlinks:
        pfname = paperdown + '\\'+ul['href']
        paperulr = urlstr + r'/' + ul['href']
        sxpLoadWeb.FetchWebAndSubImg(paperulr,pfname)
def main():
    TestParseFile()

if __name__ == '__main__':
    main()
