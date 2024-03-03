"""
- 학습기 동작
1. 각 입력 파일에 대해, 각 단어에 대해, 개별 문자들로 이루어진 토큰 튜블, 빈도 쌍 -> corpus에 저장 (dictionary of tuples)
예) 'great' {('g', 'r', 'e', 'a', 't', '_'):빈도, ...}
2. corpus에서 인접한 토큰 쌍들의 빈도를 계산
3. 가장 높은 빈도를 가진 토큰 쌍을 vocabulary에 저장 (list)
4. 이 토큰 쌍을 corpus에 반영
5. 변화가 없으면 학습 종료, 가장 높은 빈도를 가진 토큰 쌍의 빈도가 1이면 학습 종료 
6. vocabulary를 pickle로 저장 (파일명 : vocab.pickle)
"""
import sys
from collections import defaultdict
import pickle

def calculate_adjacent_freq(corpus):
    adj_freq = defaultdict(int)

    for word_tuple, freq in corpus.items():
        for i in range(len(word_tuple) - 1):
            adj_freq[(word_tuple[i], word_tuple[i+1])] += freq

    max_adj_pair = max(adj_freq, key=adj_freq.get)

    return adj_freq, max_adj_pair

def update_corpus(corpus, vocab):
    adj_freq, max_adj_pair = calculate_adjacent_freq(corpus)

    if adj_freq[max_adj_pair] == 1:
        return None
    
    vocab.append(max_adj_pair)

    print("iteration: %d (max = %d, %s)" %(len(vocab)-1, adj_freq[max_adj_pair], ''.join(max_adj_pair)), file=sys.stderr)


    new_corpus = defaultdict(int)

    for word_tuple, freq in corpus.items():
        new_word_tuple = ()
        i = 0
        while i < len(word_tuple)-1:
            if (word_tuple[i], word_tuple[i+1]) == max_adj_pair:
                new_word_tuple += (word_tuple[i]+word_tuple[i+1],)
                i += 2
            else:
                new_word_tuple += (word_tuple[i],)
                i += 1
        if i == len(word_tuple)-1:
            new_word_tuple += (word_tuple[-1],)
        new_corpus[new_word_tuple] += freq

    
    if new_corpus == corpus:
        return None
    
    return new_corpus

#############################################################
if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("%s file(s)"% sys.argv[0], file=sys.stderr)
        sys.exit()
    corpus = defaultdict(int)
    vocab = []
    for file in sys.argv[1:]:
        print("processing %s" %file, file=sys.stderr)
        with open(file) as fin:
        # 입력 파일 -> token/빈도 쌍 사전에 넣기
            for line in fin:
                for w in line.split():
                    corpus[tuple(w+"_")] += 1
        
    print("corpus size = %d tokens" %len(corpus), file=sys.stderr)

    while True:
        new_corpus = update_corpus(corpus, vocab)
        if new_corpus is None:
            break
        corpus = new_corpus

    with open('vocab.pickle', 'wb') as fout:
        pickle.dump(vocab, fout)