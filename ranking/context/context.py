__author__ = 'jane'
from sim import *
'''
:param:
sentences: list, contain sentence set
s : sentence object
Method one
'''


def is_relevant(sentences, s, t):
    max_dis = 0
    for sentence in sentences :
        sim = Similarity(sentence, s)
        if sim > max_dis:
            max_dis = sim
    if max_dis > t:
        return True
    return False

'''
Method two
def is_relevant(sentences, s, t):
    dis_sum = 0
    for sentence in sentences:
        dis_sum += Similarity(sentence,s)
    avg = dis_sum / len(sentences)
    if avg < t:
        return True
    return False
'''


def context_divide(text):
    context = []
    result = []
    for s in text:
        if len(context) == 0:
            context.append(s)
        elif is_relevant(context, s, 0.6):
            context.append(s)
        else:
            result.append(context)
            context = []
    return result


def test(filename):
    path = r'E:\Desktop'
    f = open(path + '\\' + filename)
    text = f.readlines()
    f.close()
    contexts = context_divide(text)
    for l in contexts:
        print l
        print


def main():
    test('test.txt');


if __name__ == '__main__':
    main()
