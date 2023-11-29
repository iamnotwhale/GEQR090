#!/usr/bin/env python3
# coding: utf-8

import sys
import get_morphs_tags as mf

###############################################################################
# 색인어 추출
def get_index_terms( mt_list):
    nouns = []
    test = ['NNG', 'NNP', 'SL', 'SN', 'SH', 'NR', 'NNB']
    hap = []
    #nouns = [(m, t), (m, t), ...]

    for m, t in mt_list:
        # print(m, t, sep='\t', file=sys.stderr)
        # 앞 글자가 SL인지 먼저 확인 -> 만약 맞다면 nouns 에 있는 SL을 제거.
        if t in test:
            if nouns and hap and hap[-1][1] == 'SL' and nouns[-1][1] == 'SL':
                nouns.pop()
            if t in ['NNG', 'NNP', 'SH', 'SL']:
                if t == 'SL' and hap:
                    hap.append((m, t))
                else:
                    hap.append((m, t))
                    nouns.append((m, t))
            elif t in ['SN', 'NR', 'NNB']:
                hap.append((m, t))
        else:
            nouns.append(('/', '/'))
            if len(hap) > 1:
                temp = [m for m, t in hap]
                nouns.append((''.join(temp), 'HAP'))
            hap = []

    if len(hap) > 1:
        temp = [m for m, t in hap]
        nouns.append((''.join(temp), 'HAP'))
    
    filtered = [item for item in nouns if item != ('/', '/')]
    res = [m for m, t in filtered]
    return res

###############################################################################
# Converting POS tagged corpus to a context file
def tagged2context( input_file, output_file):
    try:
        fin = open( input_file, "r")
    except:
        print( "File open error: ", input_file, file=sys.stderr)
        sys.exit()

    try:
        fout = open( output_file, "w")
    except:
        print( "File open error: ", output_file, file=sys.stderr)
        sys.exit()

    for line in fin.readlines():
    
        # 빈 라인 (문장 경계)
        if line[0] == '\n':
            print("", file=fout)
            continue

        try:
            ej, tagged = line.split(sep='\t')
        except:
            print(line, file=sys.stderr)
            continue

        # 형태소, 품사 추출
        # return : list of tuples
        result = mf.get_morphs_tags(tagged.rstrip())
        
        # 색인어 추출
        # return : list
        terms = get_index_terms(result) 
        
        # 색인어 출력
        for term in terms:
            print(term, end=" ", file=fout)
        
    fin.close()
    fout.close()
    
###############################################################################
if __name__ == "__main__":

    if len(sys.argv) < 2:
        print( "[Usage]", sys.argv[0], "file(s)", file=sys.stderr)
        sys.exit()

    for input_file in sys.argv[1:]:
        output_file = input_file + ".context"
        print( 'processing %s -> %s' %(input_file, output_file), file=sys.stderr)
        
        # 형태소 분석 파일 -> 문맥 파일
        tagged2context( input_file, output_file)
