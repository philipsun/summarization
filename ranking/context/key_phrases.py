__author__ = 'a'
from sxpPackage import *
from MyModel import *
from tf_idf import *
from word_graph import *


def extract_key_phrases(word_list, sentences):
    key_phrases = []
    for sent in sentences:
        words = [word.strip() for word in sent.split()]
        words = [word.lower() for word in words]
        is_key = []
        for word in words:
            if word in word_list:
                is_key.append(1)
            else:
                is_key.append(0)
        index_list = key_phrases_index_pair_list(is_key)
        key_phrases.extend(get_key_phrases(words, index_list))
    return key_phrases


def get_key_phrases(words, index_list):
    phrases_list = []
    for beg, end in index_list:
        phrase = ''
        if beg == end:
            continue
        for i in range(beg, end + 1):
            phrase = phrase + ' ' + words[i]
        phrases_list.append(phrase)
    return phrases_list


def key_phrases_index_pair_list(is_key_list):
    index_list = []
    begin = -1
    end = begin
    for idx in range(len(is_key_list)):
        if is_key_list[idx] == 0 and begin == -1:
            continue
        if is_key_list[idx] == 1 and begin != -1:
            end += 1
        elif is_key_list[idx] == 1 and begin == -1:
            begin = idx
            end = begin
        elif is_key_list[idx] == 0 and begin != -1:
            index_list.append((begin, end))
            begin = -1
            end = begin
    if begin != -1:
        index_list.append((begin, end))
    return index_list


def test(pickle_path):
    #model = MyModel(pickle_path)
    #model = TfIdf(pickle_path)
    model = WordGraph(pickle_path)
    keys = []
    for index in model.idx_w[:30]:
        keys.append(model.words[index])
    #print keys
    #print my_model.text.sentenceset
    #keys = []
    #for k, v in model.count_words:
     #   keys.append(v)
    sentences = []
    for sent in model.text.sentenceset:
        sentences.append(sent.sentence_text)
    #print sentences
    phrases = extract_key_phrases(keys[:20], sentences)

    for phrase in set(phrases):
        print phrase


def main():
    path = r'C:\Users\a\PycharmProjects\extractInfo\papers'
    file_name = 'P14-1007.xhtml'
    pickle_path = path + '\\pickle\\' + file_name + '_1.pickle'
    test(pickle_path)


if __name__=='__main__':
    main()