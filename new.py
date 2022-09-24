from math import sqrt
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
comments = file.readlines()

# 모든 댓글에 대해 max, min 찾고
count = 0
word_group = []
for comment in comments:
    for i in range (len(comments)): 
        splited = comment.split(',')
        joined = " ".join(splited[3:])
        nounlist = get_nounlist(joined)
        if len(word_group) == 0:
            for word in nounlist:
                word_group.append([word[0], word[1], 1])
        else:
            for j in range(0, len(word_group[i])):
                n_count = 0
                for k in range(0, len(word_group[i]-1)):
                    if word_group[i][j][0] == word_group[i][k][0]:
                        word_group[i][j][1] = word_group[i][j][1] + 1
                    else:
                        n_count = n_count + 1

                if n_count == len(word_group[i]):
                    word_group.append([word_group[i][j][0], word_group[i][j][1], 1])
                    n_count = 0
    max_min=word_group
    print(nounlist)
    print(max_min)

# test 댓글을 가져오기
file = open('test.csv', 'r', encoding='utf-8')
new_comments = file.readlines()

# test의 댓글(1)과 train댓글(n)간의 거리 구하고
new_nounlist = get_nounlist(new_comments)

def get_distance(new_num, noun_num, max_min) -> float:
    sum_term = 0

    for word, max_count, min_count in max_min:
        dividend = (new_nounlist[new_num][1] - nounlist[noun_num][1])
        dividend = 1 if dividend == 0 else dividend
        divisor = max_count - min_count

        sum_term += (dividend/divisor) ** 2
    return sqrt(sum_term)

for i in range(len(comments)):
    for j in range(len(nounlist[i])):
        for k in range (len(new_comments)):
            for l in range (len(new_nounlist[k])) : 
                if get_nounlist(comments[i])[0]==new_nounlist[k][0] :
                        distance = get_distance(k, j, max_min)
print(distance)

# 가장 가까운 3개 찾기


# 레이블 추측
