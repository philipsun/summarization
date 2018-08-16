__author__ = 'a'


def display(file_list, result, title):
    print title
    measures = [0.0 for i in range(len(result[0]))]
    for j in range(len(result)):
        item = result[j]
        print file_list[j], item
        for i in range(len(item)):
            measures[i] += item[i]
    print "mean"
    for i in range(len(measures)):
        measures[i] = float(measures[i])/len(result)
    print measures
