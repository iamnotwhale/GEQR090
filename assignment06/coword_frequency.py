#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from collections import defaultdict
from itertools import combinations

###############################################################################
def get_word_freq(filename):
    word_freq = defaultdict(int)
    total_unigram_count = 0
    
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if line == '':
                continue
            
            words = line.split()
            for word in set(words):
                word_freq[word] += 1

    for word, freq in word_freq.items():
        total_unigram_count += word_freq[word]

    return word_freq, total_unigram_count

###############################################################################
def print_word_freq(filename, word_freq):
    with open(filename, 'w') as f:
        if '#Total' in word_freq:
            print("#Total\t%d" %word_freq['#Total'], file=f)
            del word_freq['#Total']
        for word, freq in sorted(word_freq.items()):
            print("%s\t%d" %(word, freq), file=f)


###############################################################################
def get_coword_freq(filename):
    coword_freq = defaultdict(int)
    word_context_size = defaultdict(int)

    word_freq, total_unigram_count = get_word_freq(filename)

    word_freq['#Total'] = total_unigram_count

    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if line == '':
                continue
            
            words = line.split()
            for w1, w2 in combinations(set(words), 2):
                if w1 < w2:
                    coword_freq[(w1, w2)] += 1
                else:
                    coword_freq[(w2, w1)] += 1

            for word in set(words):
                word_context_size[word] += len(set(words))

    return word_freq, coword_freq, word_context_size

###############################################################################
def print_coword_freq(filename, coword_freq):
    with open(filename, 'w') as f:
        for (w1, w2), freq in sorted(coword_freq.items()):
            print("%s\t%s\t%d" %(w1, w2, freq), file=f)

###############################################################################
if __name__ == "__main__":

    if len(sys.argv) < 2:
        print( "[Usage]", sys.argv[0], "in-file(s)", file=sys.stderr)
        sys.exit()

    for input_file in sys.argv[1:]:
        
        print( 'processing %s' %input_file, file=sys.stderr)
        
        file_stem = input_file
        pos = input_file.find(".")
        if pos != -1:
            file_stem = input_file[:pos] # ex) "2017.tag.context" -> "2017"
        
        # 1gram, 2gram, 1gram context 빈도를 알아냄
        word_freq, coword_freq, word_context_size = get_coword_freq(input_file)

        # unigram 출력
        print_word_freq(file_stem+".1gram", word_freq)
        
        # bigram(co-word) 출력
        print_coword_freq(file_stem+".2gram", coword_freq)

        # unigram context 출력
        print_word_freq(file_stem+".1gram_context", word_context_size)
