#!/usr/bin/env python3
# coding: utf-8

import sys

###############################################################################
def get_morphs_tags(tagged):

    morphs_tags=tagged.split('+')
    for i in range(len(morphs_tags)):
        if morphs_tags[i]=='/SW':
            morphs_tags[i]='+/SW'
    morphs_tags = [pair for pair in morphs_tags if pair != '']

    ans = []

    for i in range(len(morphs_tags)):
        if morphs_tags[i]=='//SP':
            morph='/'
            tag='SP'
        else:
            morph, tag=morphs_tags[i].split('/')
        ans += [(morph, tag)]

    return ans        

###############################################################################
if __name__ == "__main__":

    if len(sys.argv) != 2:
        print( "[Usage]", sys.argv[0], "in-file", file=sys.stderr)
        sys.exit()

    with open(sys.argv[1]) as fin:

        for line in fin.readlines():

            # 2 column format
            segments = line.split('\t')

            if len(segments) < 2: 
                continue

            # result : list of tuples
            result = get_morphs_tags(segments[1].rstrip())
        
            for morph, tag in result:
                print(morph, tag, sep='\t')
