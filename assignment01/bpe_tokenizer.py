import sys
import pickle

def tokenizer(vocab, fin, fout):
    
    # input: vocab (list), fin (줄마다 단어가 있는 파일), fout (결과를 저장할 파일)

    # todo: 1) 각 줄의 단어를 글자별로 분리
    for line in fin:
        words = list(line.strip())
        if words == []:
            continue
        words.append("_")

    # todo: 2) vocabulary의 각 토큰 쌍을 순서대로 탐색
    # 읽은 단어 순서대로 앞뒤 한글자씩 연결해서 토큰 튜플 생성 후 리스트로 만들기
    # vocab 리스트를 순회하며 해당 토큰 튜플이 words에 있는지 확인
    # 있을 경우 하나로 합치기
    # 없을 경우 다음 토큰 튜플로 넘어가기
    # 더이상 토큰 튜플 리스트의 변화가 없거나 길이가 1일 때까지 반복

        for token in vocab:
            for i in range(len(words)-1):
                if token == tuple(words[i:i+2]):
                    words = words[:i] + ["".join(token)] + words[i+2:]
                    if len(words) == 1:
                        break
            if len(words) == 1:
                break

        print("%s\t%s" %(line.strip(), '+'.join(words)[:-1]), file=fout)

############################################################
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("%s fin"% sys.argv[0], file=sys.stderr)
        sys.exit()
    
    vocab = []
    with open('vocab.pickle', 'rb') as fin:
        vocab = pickle.load(fin)

    for file in sys.argv[1:]:

        print("processing %s -> %s" %(file, file+".bpe"), file=sys.stderr)

        fin = open(file, "rt")
        fout = open(file+".bpe", "wt")

        token_pair = tokenizer(vocab, fin, fout)