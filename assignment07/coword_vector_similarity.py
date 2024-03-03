#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import pickle
import math # sqrt

###############################################################################
def cosine_similarity(t_vector, c_vector):

    common_words = set(t_vector.keys()) & set(c_vector.keys())

    dot_prod = sum(t_vector[word] * c_vector[word] for word in common_words)

    norm_prod = math.sqrt(sum(t**2 for t in t_vector.values())) * math.sqrt(sum(t**2 for t in c_vector.values()))

    return dot_prod / norm_prod 

###############################################################################
def most_similar_words(word_vectors, target, topN=10):
    # 관련어 후보는 대상어의 공기어, 공기어들의 공기어만 해당함
    result = {}

    if target not in word_vectors:
        return None

    candidate = set(word_vectors[target].keys())

    for word in word_vectors[target].keys():
        candidate |= set(word_vectors[word].keys())

    for word in candidate:
        if word != target and word not in target:
            if cosine_similarity(word_vectors[target], word_vectors[word]) > 0.001:
                result[word] = cosine_similarity(word_vectors[target], word_vectors[word])
    
    return sorted(result.items(), key=lambda x: x[1], reverse=True)[:topN]

###############################################################################
def print_words(words):
    for word, score in words:
        print("%s\t%.3f" %(word, score))

###############################################################################
def search_most_similar_words(word_vectors, topN=10):

    print('\n검색할 단어를 입력하세요(type "^D" to exit): ', file=sys.stderr)
    query = sys.stdin.readline().rstrip()

    while query:
        # result : list of tuples, sorted by cosine similarity
        result = most_similar_words(word_vectors, query, topN)
        
        if result:
            print_words(result)
        else:
            print('\n결과가 없습니다.')

        print('\n검색할 단어를 입력하세요(type "^D" to exit): ', file=sys.stderr)
        query = sys.stdin.readline().rstrip()
    
###############################################################################
if __name__ == "__main__":

    if len(sys.argv) != 2:
        print( "[Usage]", sys.argv[0], "in-file(pickle)", file=sys.stderr)
        sys.exit()

    topN = 30
    
    with open(sys.argv[1],"rb") as fin:
        word_vectors = pickle.load(fin)
    
    search_most_similar_words(word_vectors, topN)
