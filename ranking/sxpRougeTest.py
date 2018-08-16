#-------------------------------------------------------------------------------
# Name:        sxpRougeTest
# Purpose:
#
# Author:      sunxp
#
# Created:     10-11-2015
# Copyright:   (c) sunxp 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------
from pyrouge import Rouge155
def Test():
    r = Rouge155()
    r.system_dir = 'path/to/system_summaries'
    r.model_dir = 'path/to/model_summaries'
    r.system_filename_pattern = 'some_name.(\d+).txt'
    r.model_filename_pattern = 'some_name.[A-Z].#ID#.txt'

    output = r.convert_and_evaluate()
    print(output)
    output_dict = r.output_to_dict(output)
def main():
    pass

if __name__ == '__main__':
    main()
