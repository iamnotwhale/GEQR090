#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from collections import defaultdict
from itertools import combinations

###############################################################################
def get_word_freq(filename):








            
    return word_freq, total_unigram_count

###############################################################################
def print_word_freq(filename, word_freq):






###############################################################################
def get_coword_freq(filename):
    






























                
    return word_freq, coword_freq, word_context_size

###############################################################################
def print_coword_freq(filename, coword_freq):





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
