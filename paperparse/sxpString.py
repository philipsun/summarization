#-------------------------------------------------------------------------------
# Name:        sxpString
# Purpose:
#
# Author:      sunxp
#
# Created:     13/12/2016
# Copyright:   (c) sunxp 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import re
import sxpTestStringEncode

def SplitSpace(strtxt):
    pat = r'\s+'
    s = re.split(pat,strtxt)
    return s
def DecEncStrUtf(strtext):
    s = sxpTestStringEncode.strdecode(strtext,'utf-8').encode('utf-8')
    return s
def EncDecStrUtf(strtext):
    s = sxpTestStringEncode.strencode(strtext,'utf-8').decode('utf-8')
    return s
def Test():
    a = u'adb \ndfd'
    a= DecEncStrUtf(a)
    print a
    a = EncDecStrUtf(a)
    print a
    c = SplitSpace(a)
    print(c)
def main():
    Test()

if __name__ == '__main__':
    main()
