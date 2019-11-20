# summarization by ranking sentences.

This reporsitory contains all souce codes and data from the published article:

Sun, Xiaoping, and Hai Zhuge. "Summarization of Scientific Paper through Reinforcement Ranking on Semantic Link Network." IEEE Access (2018), Volume: 6, Issue:1, pp.40611-40625.2018.

This work is an extractive automatic summarization research work. It builds a network for the text oragnization structure of a paper and use the structure graph to rank sentences and structure objects. By extracting top-k sentences, an extractive survey can be formd.

It conduct test on DUC2002 and a set of ACL2014 papers for single text summarization evaluation.

It uses pyrouge to RUN ROUGE score evaluation.

Please refer to this article when you use the data and sources from this project.

#This code contains two parts:
One for parsing networks from articles, including, DUC2002, ACL2014 and a single paper:"
Another is for ranking sentences and do ROUGE scores using pyrouge in Windows platform.

Please read the two notes for these two different packages.

readme_paperparse.md for parsing articles.

readme_rankingandsummarization.md for ranking networks and do ROUGE scoring.




