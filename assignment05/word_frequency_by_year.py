#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from collections import defaultdict

def word_count_by_year(word_count, filename, index):

    word_freq = defaultdict(int)

    with open(filename, 'r', encoding='utf-8') as fin:
        for word in fin.read().split():
            word_freq[word] += 1

    if index == 0:
        for word in word_freq:
            word_count[word].append(word_freq[word])
        return word_count

    for word in word_count:
        if word in word_freq:
            word_count[word].append(word_freq[word])
        else:
            word_count[word].append(0)
    
    for word in word_freq:
        if word not in word_count:
            word_count[word] += [0] * index
            word_count[word].append(word_freq[word])

    return word_count


#############################################################################

if __name__ == "__main__":

    if len(sys.argv) < 2:
        print( "[Usage]", sys.argv[0], "in-file(s)", file=sys.stderr)
        sys.exit()

    word_count = defaultdict(list)

    for i, filename in enumerate(sys.argv[1:]):
        word_count = word_count_by_year( word_count, filename, i)

    for w, freq in sorted(word_count.items()):
        print("%s\t%s" %(w, freq))