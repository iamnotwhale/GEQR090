#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import math # sqrt

###############################################################################
def read_frequency(filename):
    freqs = {}
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if line == '':
                continue
            
            words = line.split()
            if len(words) == 2:
                freqs[words[0]] = int(words[1])
    return freqs

###############################################################################
def calc_tscore(filename, unigrams, unigram_context, uni_N, cutoff):
    
    t_scores = {}

    with open(filename, 'r') as f: #.2gram file open
        for line in f:
            line = line.strip()
            if line == '':
                continue
            
            words = line.split()
            if len(words) != 3:
                continue

            w1, w2, freq = words
            freq = int(freq)
            
            if freq < cutoff:
                continue
            
            w1_freq = unigrams[w1]
            w2_freq = unigrams[w2]
            
            w1_context = unigram_context[w1]
            w2_context = unigram_context[w2]
            
            # O : w1, w2 공기 빈도
            # E : w1 문맥 빈도 * w2 빈도 / 코퍼스 크기
            # t-score = (O - E) / sqrt(O)

            t_score_w1_w2 = (freq - (w1_context * w2_freq / uni_N)) / math.sqrt(freq)
            t_score_w2_w1 = (freq - (w2_context * w1_freq / uni_N)) / math.sqrt(freq)
            if w2 not in w1:
                t_scores[(w1, w2)] = t_score_w1_w2
            if w1 not in w2:
                t_scores[(w2, w1)] = t_score_w2_w1

    return t_scores

###############################################################################
def print_tscore(filename, t_scores):   
    with open(filename, 'w') as f:
        for (w1, w2), t in sorted(t_scores.items()):
            if t < 0:
                continue
            else:
                print( "%s\t%s\t%.3f" %(w1, w2, t), file=f)
 
###############################################################################
if __name__ == "__main__":

    CUTOFF = 5 # 공기빈도가 이 값 이상인 경우만 t점수를 계산
    
    if len(sys.argv) < 2:
        print( "[Usage]", sys.argv[0], "in-file(s)", file=sys.stderr)
        sys.exit()

    for input_file in sys.argv[1:]:
        
        print( 'processing %s' %input_file, file=sys.stderr)

        file_stem = input_file
        pos = input_file.find(".")
        if pos != -1:
            file_stem = input_file[:pos] # ex) "2017.2gram" -> "2017"
    
        print("\tLoading %s.1gram" %file_stem, file=sys.stderr)
        unigrams = read_frequency(file_stem+".1gram")
        
        print("\tLoading %s.1gram_context" %file_stem, file=sys.stderr)
        unigram_context = read_frequency(file_stem+".1gram_context")
        
        uni_N = unigrams['#Total'] # unigram 빈도 합
        
        t_scores = calc_tscore(input_file, unigrams, unigram_context, uni_N, CUTOFF)
        
        print_tscore(file_stem+".tscore", t_scores)

