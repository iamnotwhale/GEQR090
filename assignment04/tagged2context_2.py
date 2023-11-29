#!/usr/bin/env python3
# coding: utf-8

import sys
import get_morphs_tags as mf

###############################################################################
# 색인어 추출

"""
* 색인어를 추출할 때 유의할 점
  - 색인 대상 형태소는 다음의 품사임
    NNG(일반명사), NNP(고유명사), NR(수사), NNB(의존명사), SL(외국어; 영어), SH(한자), SN(숫자)
  - 색인어는 단일어 뿐만 아니라 복합어도 추출해야 함
    여기서의 복합어란 동일한 어절 내에서 연속된 색인 대상 형태소들의 결합형을 의미함
  - 동일한 어절에 단일어와 복합어가 함께 나타나는 경우, 
    출력 순서는 단일어들을 먼저 출력한 후 복합어를 출력해야 함
  - 셋 이상의 단일어가 연속되는 경우 가장 긴 복합어만 출력함
    예) 정부/NNG+조직/NNG+개편/NNG -> 정부, 조직, 개편, 정부조직개편
  - NNG, NNP, SH, SL은 단일어로도 색인어로 추출함 (단, SL이 복합어에 속하는 경우 단일어로는 색인어로 추출하지 않음)
  - NR, NNB, SN은 단일어로는 색인어로 추출하지 않음
"""
def get_index_terms( mt_list):
    #input: list of tuples [(형태소, 품사), ...], 어절 단위
    terms = []
    search_list = ['NNG', 'NNP', 'NR', 'NNB', 'SL', 'SH', 'SN']

    wordhap = ''

    for i in range(len(mt_list)):
        if mt_list[i][1] in search_list:
            if mt_list[i][1] in ['NR', 'NNB', 'SN']:
                wordhap += mt_list[i][0]
                continue
            elif mt_list[i][1] == 'SL':
                if len(mt_list) == 1:
                    wordhap += mt_list[i][0]
                    continue
                elif i != 0 and i != len(mt_list)-1:
                    if mt_list[i-1][1] in search_list or mt_list[i+1][1] in search_list:
                        wordhap += mt_list[i][0]
                        continue
                    else:
                        wordhap += '/'
                        continue
                elif i == 0:
                    if mt_list[i+1][1] in search_list:
                        wordhap += mt_list[i][0]
                        continue
                    else:
                        wordhap += '/'
                        continue
                else:
                    if mt_list[i-1][1] in search_list:
                        wordhap += mt_list[i][0]
                        continue
                    else:
                        wordhap += '/'
                        continue
            terms.append(mt_list[i][0])
            wordhap += mt_list[i][0]
        else:
            wordhap += '/'

    wordhaplist = wordhap.split('/')
    count = wordhaplist.count('')

    i = 0
    while i < count:
        wordhaplist.remove('')
        i += 1

    for word in wordhaplist:
        if word not in terms:
            terms.append(word)

    return terms

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
