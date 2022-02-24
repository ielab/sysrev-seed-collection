import math
from six import iteritems
from six.moves import xrange
import numpy
from numpy import dot
import sys
from numpy.linalg import norm
from gensim.models import KeyedVectors
from gensim.utils import simple_preprocess
import scipy
import scipy.spatial

# QLM parameters.
Lamda= 0.2

class AES(object):
    def __init__(self, corpus):
        self.corpus = corpus
        self.corpus_size = len(corpus)


    def get_scores(self, document):
        index_list = []
        for index in xrange(self.corpus_size):
            index_list.append(self.corpus[index])
        scores = scipy.spatial.distance.cdist(document, index_list, 'cosine')[0]

        return scores


