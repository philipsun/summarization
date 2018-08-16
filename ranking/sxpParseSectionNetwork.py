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
import sxpPackage
def ParseSectionNetwork(sxptxt):
    for sxpsec in sxptxt.section_list:
        int_id = sxpsec.id
        set_sec_id = sxpsec.id_set
        print int_id, set_sec_id,
def TestSection():
    pickle_dir = path + '\\pickle\\'

def main():
    pass

if __name__ == '__main__':
    main()
