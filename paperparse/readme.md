#Parsing out structural Graph from papers.

This prackage contains major files for parsing semantic link networks from acl2014 papers, a DUC2002 collection, and a single selected paper.

#Data Set:

##DUC 2002:

./paper/duc/* original documents selected from DUC 2002, sentences are separated by '*****'

./paper/duc/txt: pure model txt of the raw data of duc 2002 news. This is to be used to produce model_html.

./paper/duc/model_html: produced model files for summarization for each doc in ./paper/duc/txt

./paper/duc/pickle: produce network data for each doc in our collection, which can be loaded and iteratative models can be applied for ranking sentences.

##ACL 2014 Paper Collection

./paper/papers/* original documents selected from the ACL2014 Proceedings

./paper/papers/txt: pure txt of abstraction and conclusion of the raw data of the ACL2014 Proceedings.

./paper/papers/model_html: produced model files for summarization for each doc in  the ACL2014 Proceedings

./paper/papers/pickle: produce network data for each doc in our collection, which can be loaded and iteratative models can be applied for ranking sentences.

## Single Paper Collection

    modelpath = r'.\paper\single\model': summarization model of the paper

    pkpath = r'.\paper\single\pk': structural graph data of the paper

    fname = r'.\paper\single\testdimension_2.txt', raw paper text


# To Run Code

All codes are starting from the __main__() function

`
sxpACLPaperAnalysis.py: This is to parse the ACL 2014 Proceedings Text.

sxpParseDUCText.py: This is to parse structural graph from the DUC collections.

sxpParseSinglePaper.py: This is to parse the single paper structure.

`


