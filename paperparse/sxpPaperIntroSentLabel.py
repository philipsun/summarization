#-------------------------------------------------------------------------------
# Name:        sxpPaperIntroSentLabel
# Purpose:
#
# Author:      sunxp
#
# Created:     26/05/2015
# Copyright:   (c) sunxp 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------
intro_sent = [['P14-1007.xhtml',
    r'Recently, there has been increased community interest in the theoretical and practical analysis of what \citeAMor:Dae:12 call modality and negation, i.e. linguistic expressions that modulate the certainty or factuality of propositions',
    r'Automated analysis of such aspects of meaning is important for natural language processing tasks which need to consider the truth value of statements, such as for example text mining [9] or sentiment analysis [5]',
    r'Owing to its immediate utility in the curation of scholarly results, the analysis of negation and so-called hedges in bio-medical research literature has been the focus of several workshops, as well as the Shared Task at the 2011 Conference on Computational Language Learning (CoNLL)',
    r'In this work, we return to the 2012 *SEM task from a deliberately semantics-centered point of view, focusing on the hardest of the three sub-problems: scope resolution',
    r'Resolving negation scope is a more difficult sub-problem at least in part because (unlike cue and event identification) it is concerned with much larger, non-local and often discontinuous parts of each utterance',
    r'Our contributions are three-fold',
    r'Theoretically, we correlate the structures at play in the \citeAMor:Dae:12 view on negation with formal semantic analyses',
    r'methodologically, we demonstrate how to approach the task in terms of underspecified, logical-form semantics',
    r'and practically, our combined system retroactively ‘wins’ the 2012 *SEM Shared Task'
    ],
    ['P14-1008.xhtml',
    r'Dependency-based Compositional Semantics (DCS) provides an intuitive way to model semantics of questions, by using simple dependency-like trees ',
    r'It is expressive enough to represent complex natural language queries on a relational database, yet simple enough to be latently learned from question-answer pairs.',
    r' In this paper, we equip DCS with logical inference, which, in one point of view, is “the best way of testing an NLP system’s semantic capacity”'
    r'It should be noted that, however, a framework primarily designed for question answering is not readily suited for logical inference',
    r'Because, answers returned by a query depend on the specific database, but implication is independent of any databases. ',
    r'Thus, our first step is to fix a notation which abstracts the calculation process of DCS trees, so as to clarify its meaning without the aid of any existing database',
    r'An inference engine is built to handle inference on abstract denotations.',
    r'Moreover, to compensate the lack of background knowledge in practical inference, we combine our framework with the idea of tree transformation [], to propose a way of generating knowledge in logical representation from entailment rules [], which are by now typically considered as syntactic rewriting rules.',
    r'We test our system on FraCaS [] and PASCAL RTE datasets [].'
    r'The experiments show: (i) a competitive performance on FraCaS dataset;',
    r'(ii) a big impact of our automatically generated on-the-fly knowledge in achieving high recall for a logic-based RTE system;',
    r'and (iii) a result that outperforms state-of-the-art RTE system on RTE5 data.'
    ],
    ['P14-1009.xhtml',
    r'The research of the last two decades has established empirically that distributional vectors for words obtained from corpus statistics can be used to represent word meaning in a variety of tasks [25].',
    r'If distributional vectors encode certain aspects of word meaning, it is natural to expect that similar aspects of sentence meaning can also receive vector representations, obtained compositionally from word vectors.',
    r'Developing a practical model of compositionality is still an open issue, which we address in this paper',
    r'One approach is to use simple, parameter-free models that perform operations such as pointwise multiplication or summing [20]. ',
    r'None of the proposals mentioned above, from simple to elaborate, incorporates in its architecture the intuitive idea (standard in theoretical linguistics) that semantic composition is more than a weighted combination of words. ',
    r' Generally one of the components of a phrase, e.g., an adjective, acts as a function affecting the other component (e.g., a noun). This underlying intuition, adopted from formal semantics of natural language, motivated the creation of the lexical function model of composition (lf) [4, 9]',
    r'The lf model can be seen as a projection of the symbolic Montagovian approach to semantic composition in natural language onto the domain of vector spaces and linear operations on them [3]. ',
    r'In lf, arguments are vectors and functions taking arguments (e.g., adjectives that combine with nouns) are tensors, with the number of arguments (n) determining the order of tensor (n+1).',
    r'With all the advantages of lf, scaling it up to arbitrary sentences, however, leads to several issues.',
    r'Estimating tensors of this size runs into data sparseness issues already for less common transitive verbs.',
    r'Things get even worse for other categories.',
    r'Adverbs like quickly that modify intransitive verbs have to be represented with 30022 = 8,100,000,000 dimensions.',
    r'Modifiers of transitive verbs would have even greater representation size, which may not be possible to store and learn efficiently.',
    r'Another issue is that the same or similar items that occur in different syntactic contexts are assigned different semantic types with incomparable representations.',
    r'In all those cases, the same word has to be mapped to tensors of different orders.',
    r'Since each of these tensors must be learned from examples individually, their obvious relation is missed.',
    r'Besides losing the comparability of the semantic contribution of a word across syntactic contexts, we also worsen the data sparseness issues.',
    r'The last, and related, point is that for the tensor calculus to work, one needs to model, for each word, each of the constructions in the corpus that the word is attested in.'
    ],
	['P14-1010.xhtml',
	r'Morphological segmentation is considered to be indispensable when translating between English and morphologically complex languages such as Arabic.',
	r'Morphological complexity leads to much higher type to token ratios than English, which can create sparsity problems during translation model estimation. ',
	r'Morphological segmentation addresses this issue by splitting surface forms into meaningful morphemes, while also performing orthographic transformations to further reduce sparsity.',
	r'Desegmentation is typically performed as a post-processing step that is independent from the decoding process. ',
	r'In this work, we show that it is possible to maintain the sparsity-reducing benefit of segmentation while translating directly into unsegmented text.',
	r'We desegment a large set of possible decoder outputs by processing n-best lists or lattices, which allows us to consider both the segmented and desegmented output before locking in the decoder’s decision.',
	r'We demonstrate that significant improvements in translation quality can be achieved by training a linear model to re-rank this transformed translation space.'
	],
	['P14-1011.xhtml',
	r'Due to the powerful capacity of feature learning and representation, Deep (multi-layer) Neural Networks (DNN) have achieved a great success in speech and image processing [13, 15, 6].',
	r'Recently, statistical machine translation (SMT) community has seen a strong interest in adapting and applying DNN to many tasks, such as word alignment [29], translation confidence estimation [19, 18, 31], phrase reordering prediction [16], translation modelling [1, 12] and language modelling [7, 26].',
	r'Most of these works attempt to improve some components in SMT based on word embedding, which converts a word into a dense, low dimensional, real-valued vector representation [2, 3, 5, 20].',
	r'However, in the conventional (phrase-based) SMT, phrases are the basic translation units. ',
	r'The models using word embeddings as the direct inputs to DNN cannot make full use of the whole syntactic and semantic information of the phrasal translation rules.',
	r'Therefore, in order to successfully apply DNN to model the whole translation process, such as modelling the decoding process, learning compact vector representations for the basic phrasal translation units is the essential and fundamental work.',
	r'In this paper, we explore the phrase embedding, which represents a phrase (sequence of words) with a real-valued vector. In some previous works, phrase embedding has been discussed from different views.',
	r'In this paper, we explore the phrase embedding, which represents a phrase (sequence of words) with a real-valued vector. In some previous works, phrase embedding has been discussed from different views. ',
	r'Therefore, these phrase embeddings are not suitable to fully represent the phrasal translation units in SMT due to the lack of semantic meanings of the phrase.',
	r'Instead, we focus on learning phrase embeddings from the view of semantic meaning, so that our phrase embedding can fully represent the phrase and best fit the phrase-based SMT. ',
	r'Assuming the phrase is a meaningful composition of its internal words, we propose Bilingually-constrained Recursive Auto-encoders (BRAE) to learn semantic phrase embeddings. ',
	r'The core idea behind is that a phrase and its correct translation should share the same semantic meaning.',
	r'Thus, they can supervise each other to learn their semantic phrase embeddings. ',
	r' Similarly, non-translation pairs should have different semantic meanings, and this information can also be used to guide learning semantic phrase embeddings.',
	r'In our method, the standard recursive auto-encoder (RAE) pre-trains the phrase embedding with an unsupervised algorithm by minimizing the reconstruction error [22], while the bilingually-constrained model learns to fine-tune the phrase embedding by minimizing the semantic distance between translation equivalents and maximizing the semantic distance between non-translation pairs.',
	r'With the learned model, we can accurately measure the semantic similarity between a source phrase and a translation candidate.',
	r'Accordingly, we evaluate the BRAE model on two end-to-end SMT tasks (phrase table pruning and decoding with phrasal semantic similarities) which need to check whether a translation candidate and the source phrase are in the same meaning.',
	r'In addition, our semantic phrase embeddings have many other potential applications.'
	],
	[
	'P14-1012.xhtml',
	r'Recently, many new features have been explored for SMT and significant performance have been obtained in terms of translation quality, such as syntactic features, sparse features, and reordering features.',
	r'However, most of these features are manually designed on linguistic phenomena that are related to bilingual language pairs, thus they are very difficult to devise and estimate.',
	r'Instead of designing new features based on intuition, linguistic knowledge and domain, for the first time, Maskey and Zhou (2012) explored the possibility of inducing new features in an unsupervised fashion using deep belief net (DBN) for hierarchical phrase-based translation model',
	r'Using the 4 original phrase features in the phrase table as the input features, they pre-trained the DBN by contrastive divergence and generated new unsupervised DBN features using forward computation.',
	r'These new features are appended as extra features to the phrase table for the translation decoder.',
	r'However, the above approach has two major shortcomings. ',
	r'First, the input original features for the DBN feature learning are too simple, the limited 4 phrase features of each phrase pair, such as bidirectional phrase translation probability and bidirectional lexical weighting, which are a bottleneck for learning effective feature representation.',
	r'Second, it only uses the unsupervised layer-wise pre-training of DBN built with stacked sets of Restricted Boltzmann Machines (RBM) [Hinton2002], does not have a training objective, so its performance relies on the empirical parameters. Thus, this approach is unstable and the improvement is limited.',
	r' In this paper, we strive to effectively address the above two shortcomings, and systematically explore the possibility of learning new features using deep (multi-layer) neural networks (DNN, which is usually referred under the name Deep Learning) for SMT.',
	r'To address the first shortcoming, we adapt and extend some simple but effective phrase features as the input features for new DNN feature learning, and these features have been shown significant improvement for SMT, such as, phrase pair similarity [Zhao et al.2004], phrase frequency, phrase length [Hopkins and May2011], and phrase generative probability [Foster et al.2010], which also show further improvement for new phrase feature learning in our experiments.'
	r'To address the second shortcoming, inspired by the successful use of DAEs for handwritten digits recognition [Hinton and Salakhutdinov2006, Hinton et al.2006], information retrieval [Salakhutdinov and Hinton2009, Mirowski et al.2010], and speech spectrograms [Deng et al.2010], we propose new feature learning using semi-supervised DAE for phrase-based translation model.',
	r'Moreover, to learn high dimensional feature representation, we introduce a natural horizontal composition for DAEs (HCDAE) that can be used to create large hidden layer representations simply by horizontally combining two (or more) DAEs [Baldi2012], which shows further improvement compared with single DAE in our experiments.',
	r'Finally, we conduct large-scale experiments on IWSLT and NIST Chinese-English translation tasks, respectively, and the results demonstrate that our solutions solve the two aforementioned shortcomings successfully.',
	r'Our semi-supervised DAE features significantly outperform the unsupervised DBN features and the baseline features, and our introduced input phrase features significantly improve the performance of DAE feature learning.',
	r'Thus, instead of GMM, we use DNN (DBN, DAE and HCDAE) to learn new non-parametric features, which has the similar evolution in speech recognition [Dahl et al.2012, Hinton et al.2012]. DNN features are learned from the non-linear combination of the input original features, they strong capture high-order correlations between the activities of the original features, and we believe this deep learning paradigm induces the original features to further reach their potential for SMT.'
	],
	['P14-1013.xhtml',
	r'Making translation decisions is a difficult task in many Statistical Machine Translation (SMT) systems. ',
	r' Current translation modeling approaches usually use context dependent information to disambiguate translation candidates. For example, translation sense disambiguation approaches [4, 5] are proposed for phrase-based SMT systems.',
	r'Meanwhile, for hierarchical phrase-based or syntax-based SMT systems, there is also much work involving rich contexts to guide rule selection ',
	r'Although these methods are effective and proven successful in many SMT systems, they only leverage within-sentence contexts which are insufficient in exploring broader information. ',
	r'Topic modeling is a useful mechanism for discovering and characterizing various semantic concepts embedded in a collection of documents.',
	r' Most of them also assume that the input must be in document level.',
	r'However, this situation does not always happen since there is considerable amount of parallel data which does not have document boundaries.',
	r' In addition, contemporary SMT systems often works on sentence level rather than document level due to the efficiency. ',
	r'Although we can easily apply LDA at the sentence level, it is quite difficult to infer the topic accurately with only a few words in the sentence.',
	r'This makes previous approaches inefficient when applied them in real-world commercial SMT systems.',
	r' Therefore, we need to devise a systematical approach to enriching the sentence and inferring its topic more accurately.',
	r'In this paper, we propose a novel approach to learning topic representations for sentences.',
	r'Since the information within the sentence is insufficient for topic modeling, we first enrich sentence contexts via Information Retrieval (IR) methods using content words in the sentence as queries, so that topic-related monolingual documents can be collected. ',
	r'These topic-related documents are utilized to learn a specific topic representation for each sentence using a neural network based approach. ',
	r'Our problem fits well into the neural network framework and we expect that it can further improve inferring the topic representations for sentences.',
	r'To incorporate topic representations as translation knowledge into SMT, our neural network based approach directly optimizes similarities between the source language and target language in a compact topic space. '
	r'This underlying topic space is learned from sentence-level parallel data in order to share topic information across the source and target languages as much as possible. ',
	r'Additionally, our model can be discriminatively trained with a large number of training instances, without expensive sampling methods such as in LDA or HTMM, thus it is more practicable and scalable.',
	r'Finally, we associate the learned representation to each bilingual translation rule. ',
	r'Topic-related rules are selected according to distributional similarity with the source text, which helps hypotheses generation in SMT decoding. ',
	r'We integrate topic similarity features in the log-linear model and evaluate the performance on the NIST Chinese-to-English translation task. ',
	r'Experimental results demonstrate that our model significantly improves translation accuracy over a state-of-the-art baseline.'
	],
    ['P14-1014.xhtml',
    r'Analysing and extracting useful information from the web has become an increasingly important research direction for the NLP community, where many tasks require part-of-speech (POS) tagging as a fundamental preprocessing step.',
    r'However, state-of-the-art POS taggers in the literature [5, 23] are mainly optimized on the the Penn Treebank (PTB), and when shifted to web data, tagging accuracies drop significantly [18].',
    r'The problem we face here can be considered as a special case of domain adaptation, where we have access to labelled data on the source domain (PTB) and unlabelled data on the target domain (web data).',
    r'Exploiting useful information from the web data can be the key to improving web domain tagging.',
    r' Towards this end, we adopt the idea of learning representations which has been demonstrated useful in capturing hidden regularities underlying the raw input data (web text, in our case).',
    r'In the pre-training phase, we learn an encoder that converts the web text into an intermediate representation, which acts as useful features for prediction tasks.',
    r'In the fine-tuning phase, the parameters of the network are optimized on a set of labelled training data using guided learning.',
    r'The learned model preserves the property of preferring to tag easy words first.',
    r'To our knowledge, we are the first to investigate guided learning for neural networks.'
    ],
    ['P14-1015.xhtml',
    r'Discussion forums have become a popular knowledge source for finding solutions to common problems. ',
    r'Mining problem-solution pairs from discussion forums has attracted much attention from the scholarly community in the recent past.',
    r'In this paper, we address the problem of unsupervised solution post identification',
    r'This problem has been referred to as answer extraction by some papers earlier.',
    r'However, we use solution identification to refer to the problem since answer and extraction have other connotations in the Question-Answering and Information Extraction communities respectively. from discussion forums.',
    r'All solution identification approaches since [4] have used supervised methods that require training data in the form of labeled solution and non-solution posts.',
    r'The techniques differ from one another mostly in the non-textual features that are employed in representing posts.',
    r'We propose an unsupervised method for solution identification.',
    r'The cornerstone of our technique is the usage of a hitherto unexplored textual feature, lexical correlations between problems and solutions, that is exploited along with language model based characterization of solution posts.',
    r'We model the lexical correlation and solution post character using regularized translation models and unigram language models respectively.',
    r'To keep our technique applicable across a large variety of forums with varying availability of non-textual features, we design it to be able to work with minimal availability of non-textual features.',
    r'In particular, we show that by using post position as the only non-textual feature, we are able to achieve accuracies comparable to supervision-based approaches that use many structural features [2]'
    ],
    ['P14-1018.xhtml',
    r'Inferring latent user attributes such as gender, age, and political preferences [30, 42, 6] automatically from personal communications and social media including emails, blog posts or public discussions has become increasingly popular with the web getting more social and volume of data available.',
    r'The existing batch models for predicting latent user attributes rely on thousands of tweets per author',
    r'However, most Twitter users are less prolific than those examined in these works, and thus do not produce the thousands of tweets required to obtain their levels of accuracy e.g., the median number of tweets produced by a random Twitter user per day is 10.',
    r'In this paper we analyze and go beyond static models formulating personal analytics in social media as a streaming task.',
    r'We first evaluate batch models that are cognizant of low-resource prediction setting described above, maximizing the efficiency of content in calculating personal analytics.',
    r'In addition, we propose streaming models for personal analytics that dynamically update user labels based on their stream of communications which has been addressed previously by Van Durme (2012b).',
    r'develop low-resource and real-time dynamic approaches for personal analytics using as an example the prediction of political preference of Twitter users',
    r'examine the relative utility of six different notions of “similarity” between users in an implicit Twitter social network for personal analytics;',
    r'experiments are performed across multiple datasets supporting the prediction of political preference in Twitter, to highlight the significant differences in performance that arise from the underlying collection and annotation strategies.'
    ],
    ['P14-1019.xhtml',
    r'Dependency parsing is commonly cast as a maximization problem over a parameterized scoring function.',
    r'In this view, the use of more expressive scoring functions leads to more challenging combinatorial problems of finding the maximizing parse.',
    r'Much of the recent work on parsing has been focused on improving methods for solving the combinatorial maximization inference problems. Indeed, state-of-the-art results have been obtained by adapting powerful tools from optimization [16, 17, 27].',
    r'We depart from this view and instead focus on using highly expressive scoring functions with substantially simpler inference procedures.',
    r'The key ingredient in our approach is how learning is coupled with inference.',
    r'Our combination outperforms the state-of-the-art parsers and remains comparable even if we adopt their scoring functions.',
    r'In this paper, we introduce a sampling-based parser that places few or no constraints on the scoring function.',
    r'The benefits of sampling-based learning go beyond stand-alone parsing.'
    ]
]
paperpath = r'D:\pythonwork\code\paperparse\paper\papers'
def TestTwoSent():
    print intro_sent

def main():
    TestTwoSent()

if __name__ == '__main__':
    main()
