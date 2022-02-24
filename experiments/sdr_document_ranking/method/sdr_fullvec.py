import math
from six.moves import xrange
import numpy
import scipy
from sklearn.feature_extraction.text import TfidfVectorizer

import random
# QLM parameters.
import os
Lamda= 0.2

class SDR_full(object):
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
            self.f.append(frequencies)
            for key in frequencies:
                if key not in self.wf:
                    self.wf[key] = 1
                else:
                    self.wf[key] += 1
        self.corpus_len = sum(self.doc_length)


    def get_score(self, document, index, weight_d):
        score = 0
        for word in document:
            if word not in self.f[index]:
                continue
            mle = self.wf[word] / self.corpus_len
            score += weight_d[word] * (self.query_dictionary[word])* math.log(1 + ((1-Lamda) / Lamda * (self.f[index][word] / (self.doc_length[index] * mle))))
        return score

    def get_scores(self, document, overall_corpus, weight_dict_stored, topic_id, output_dir):
        scores = []
        weight_dic = {}
        #query is at index[0], the all other document
        #tfidf_matrix = TfidfVectorizer().fit_transform(overall_corpus)

        tf_idf_numpy = TfidfVectorizer(min_df=1).fit_transform(overall_corpus).toarray()
        original_vector = [tf_idf_numpy[0]]
        for word in document:
            if word in weight_dict_stored:
                weight_dic[word] = weight_dict_stored[word]
            else:
                positive_vectors = [tf_idf_numpy[0]]
                negative_vectors = []
                for index in xrange(self.corpus_size):
                    matrix_index = index+1
                    a = tf_idf_numpy[matrix_index]
                    if word in self.f[index]:
                        positive_vectors.append(a)
                    else:
                        negative_vectors.append(a)
                positive_vectors_csr = positive_vectors
                negative_vectors_csr = negative_vectors

                if len(positive_vectors_csr)>0:
                    positive_values = scipy.spatial.distance.cdist(original_vector, positive_vectors_csr, 'cosine')[0]
                    #print(positive_values)
                    positive_value = 1 - ((sum(positive_values)) / len(positive_values))
                else:
                    #print(word, 'POSTIVIES-NULL')
                    positive_value = 0.1
                if len(negative_vectors_csr)>0:
                    negative_values = scipy.spatial.distance.cdist(original_vector, negative_vectors_csr, 'cosine')[0]
                    negative_values = numpy.nan_to_num(negative_values, nan=0.0)
                    negative_value = 1 - ((sum(negative_values)) / len(negative_values))
                else:
                    #print(word, 'NEGATIVES-NULL')
                    negative_value = 0.1
                #positive_value = numpy.average(linear_kernel(tfidf_matrix[0:1], positive_vectors_csr).flatten())
                #negative_value = numpy.average(linear_kernel(tfidf_matrix[0:1], negative_vectors_csr).flatten())
                weight_dic[word] = math.log(1 + (positive_value / negative_value))
                with open(os.path.join(output_dir, topic_id+'.tsv'), 'a+') as storing_file:
                    storing_file.write(word+'\t'+str(weight_dic[word]) + '\n')
                #print(word, weight_dic[word])

        for index in xrange(self.corpus_size):
            score = self.get_score(document, index, weight_dic)
            scores.append(score)
        return scores

    def get_scores_multiple(self, document, overall_corpus, weight_dict_stored, topic_id, output_dir):
        scores = []
        weight_dic = {}
        tf_idf_numpy = TfidfVectorizer().fit_transform(overall_corpus).toarray()
        original_vector = [tf_idf_numpy[0]]
        for word in document:
            positive_vectors = [tf_idf_numpy[0]]
            negative_vectors = []
            if word in weight_dict_stored:
                weight_dic[word] = weight_dict_stored[word]
            else:
                if self.corpus_size>50:
                    random_docs = random.sample(xrange(self.corpus_size), 50)
                else:
                    random_docs = xrange(self.corpus_size)
                for index in random_docs:
                    matrix_index = index+1
                    a = tf_idf_numpy[matrix_index]
                    if word in self.f[index]:
                        positive_vectors.append(a)
                    else:
                        negative_vectors.append(a)
                positive_vectors_csr = positive_vectors
                negative_vectors_csr = negative_vectors

                if len(positive_vectors_csr)>0:
                    positive_values = scipy.spatial.distance.cdist(original_vector, positive_vectors_csr, 'cosine')[0]
                    #print(positive_values)
                    positive_value = 1 - ((sum(positive_values)) / len(positive_values))
                else:
                    #print(word, 'POSTIVIES-NULL')
                    positive_value = 0.1
                if len(negative_vectors_csr)>0:
                    negative_values = scipy.spatial.distance.cdist(original_vector, negative_vectors_csr, 'cosine')[0]
                    negative_values = numpy.nan_to_num(negative_values, nan=0.0)
                    negative_value = 1 - ((sum(negative_values)) / len(negative_values))
                else:
                    negative_value = 0.1
                weight_dic[word] = math.log(1 + (positive_value / negative_value))
                with open(os.path.join(output_dir, topic_id+'.tsv'), 'a+') as storing_file:
                    storing_file.write(word+'\t'+str(weight_dic[word]) + '\n')
            #print(word, weight_dic[word])

        for index in xrange(self.corpus_size):
            score = self.get_score(document, index, weight_dic)
            scores.append(score)
        return scores


