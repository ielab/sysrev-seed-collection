import math
from six import iteritems
from six.moves import xrange


# QLM parameters.
Lamda= 0.2

class QLM(object):

    def __init__(self, corpus, query_dictionary):
        self.query_dictionary = query_dictionary
        self.corpus_size = len(corpus)
        self.avgdl = sum(float(len(x)) for x in corpus) / self.corpus_size
        self.corpus = corpus
        self.f = []
        self.doc_length = []
        self.corpus_len = 0
        self.wf = {}
        self.initialize()

    def initialize(self):
        for document in self.corpus:
            frequencies = {}
            self.doc_length.append(len(document))
            for word in document:
                if word not in frequencies:
                    frequencies[word] = 0
                frequencies[word] += 1
                if word not in self.wf:
                    self.wf[word] = 0
                self.wf[word] += 1
            self.f.append(frequencies)

        self.corpus_len = sum(self.doc_length)

    def get_score(self, document, index, df_dic, background_s):
        score = 0
        for word in document:
            if word not in self.f[index]:
                continue
            mle = df_dic[word] / background_s
            score += (self.query_dictionary[word])* math.log(1 + ((1-Lamda) / Lamda * (self.f[index][word] / (self.doc_length[index] * mle))))
        return score

    def get_scores(self, document,df_dic, background_size):
        scores = []
        for index in xrange(self.corpus_size):
            score = self.get_score(document, index, df_dic, background_size)
            scores.append(score)
        return scores

