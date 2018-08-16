__author__ = 'a'
from sxpPackage import *

def test_compare(path, file_name, intro_id_list, intro_labeled_id_set):
    print "In test_compare() function...."
    print intro_id_list
    print intro_labeled_id_set
    compare_result(path, file_name, intro_id_list, intro_labeled_id_set)
    return "Complete successfully!"


def compare_result(path, file_name, intro_id_set, paper_intro_id_set):
    print intro_id_set
    print paper_intro_id_set
    pickle_path = path + '\\pickle\\' + file_name + '_1.pickle'
    #get the sxpText object
    text = LoadSxptext(pickle_path)
    sentence_set = text.sentenceset
    print "======================================================="
    print "This is result given by machine... "
    print "======================================================="
    for intro_id in intro_id_set:
        print intro_id, sentence_set[intro_id].sentence_text
    print
    print "========================================================"
    print "This is result given by human..."
    print "========================================================"
    for intro_id in paper_intro_id_set:
        print intro_id, sentence_set[intro_id].sentence_text

