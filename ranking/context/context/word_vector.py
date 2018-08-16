__author__ = 'a'
from MyModel import MyModel
from tf_idf import TfIdf
from word_graph import WordGraph
from sxpPackage import *

# test the word weight of different models


def get_word_weight(pickle_path):
    my_model = MyModel(pickle_path)
    tf_idf_model = TfIdf(pickle_path)
    words_graph = WordGraph(pickle_path)
    # my model word and weight
    print "My Model...."
    print
    for i in my_model.idx_w[:30]:
        print my_model.words[i], my_model.w[i]
    print "TF-IDF model..."
    print
    for k, v in tf_idf_model.count_words:
        print v, k
    print "Word Graph model..."
    print
    for i in words_graph.idx_w[:15]:
        print words_graph.words[i], words_graph.w[i]


def main():
    path = r'C:\Users\a\PycharmProjects\extractInfo\papers'
    file_name = 'P14-1007.xhtml'
    pickle_path = path + '\\pickle\\' + file_name + '_1.pickle'
    get_word_weight(pickle_path)


if __name__ == '__main__':
    main()