import common

def get_word_count_pair_list(word_list: list):
    '''
    명사 리스트를 (명사, 빈도수) 리스트로 변환
    get_word_count_pair_list(['apple', 'apple']) == [('apple', 2)] 
    '''
    word_list = sorted(word_list)
    result = []
    start = 0
    end = 0
    while start < len(word_list):
        while end < len(word_list) and word_list[start] == word_list[end]:
            end = end + 1
        result.append([word_list[start], end - start])
        start = end
    return result


def get_nounlist(comment):
    word_list = comment.split(' ')
    noun_list = []
    for i in range(len(word_list)):
        if word_list[i] in noun:
            noun_list.append(word_list[i])
        elif common.combi2(word_list[i]) != []:
            t = common.combi2(word_list[i])
            for j in range(len(t)):
                noun_list.append(t[j])
        elif common.combi3(word_list[i]) != []:
            t = common.combi3(word_list[i])
            for j in range(len(t)):
                noun_list.append(t[j])

    c = get_word_count_pair_list(noun_list)
    return c

noun = common.load_nouns()
postp = common.load_postpositions()
haday = common.load_haday()


# train 댓글을 가져오기
file = open('train.csv', 'r', encoding='utf-8')
rows = file.readlines()

# 모든 댓글에 대해 max, min 찾고
count = 0
max
for row in rows:
    splited = row.split(',')
    joined = " ".join(splited[3:])
    nounlist=get_nounlist(joined)
    for j in range (len(nounlist[row])) :
        if nounlist[row][j] == nounlist[ro
            count = count + 1


# test 댓글을 가져오기

# test의 댓글(1)과 train댓글(n)간의 거리 구하고

# 가장 가까운 3개 찾기

# 레이블 추측
