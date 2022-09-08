from math import sqrt
import common


def combi2(t):
    n = len(t)
    for i in range(n-1, 0, -1):
        if (t[0:i] in noun and t[i:n] in haday):
            return [t[0:i]]
        elif (t[0:i] in noun and t[i:n] in noun):
            return [t[0:i], t[i:n]]
        elif (t[0:i] in noun and t[i:n] in postp):
            return [t[0:i]]
    return []


def combi3(t):
    n = len(t)
    for i in range(1, n):
        for j in range(i+1, n):
            if (t[0:i] in noun and t[i:j] in noun and t[j:n] in postp):
                return [t[0:i], t[i:j]]
    return []


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
        elif combi2(word_list[i]) != []:
            t = combi2(word_list[i])
            for j in range(len(t)):
                noun_list.append(t[j])
        elif combi3(word_list[i]) != []:
            t = combi3(word_list[i])
            for j in range(len(t)):
                noun_list.append(t[j])
        c = get_word_count_pair_list(noun_list)

    return c


def get_maxmin(nounlist):
    word_group = []
    if len(word_group) == 0:
        for word in nounlist:
            word_group.append([word[0], word[1], word[1]])
    else:
        for i in range(0, len(nounlist)):
            n_count = 0
            for j in range(0, len(word_group)):
                if nounlist[i][0] == word_group[j][0]:
                    if nounlist[i][1] > word_group[j][1]:
                        word_group[j][1] = nounlist[i][1]
                    if nounlist[i][1] < word_group[j][2]:
                        word_group[j][2] = nounlist[i][1]
                else:
                    n_count = n_count + 1

            if n_count == len(word_group):
                word_group.append(
                    [nounlist[i][0], nounlist[i][1], nounlist[i][1]])
                n_count = 0

    return word_group


def get_distance(new_num, noun_num, max_min) -> float:

    sum_term = 0
    for word, value1, value2 in max_min:
        dividend = (new_nounlist[new_num][1] - nounlist[noun_num][1])
        dividend = 1 if dividend == 0 else dividend

        divisor = value1 - value2
        divisor = 1 if divisor == 0 else divisor

        sum_term += (dividend/divisor) ** 2
    return sqrt(sum_term)


nounf = open('noun.txt', 'r', encoding='utf-8')
nounl = nounf.readlines()
noun = []
for i in range(len(nounl)):
    noun.append(nounl[i].strip('.\n'))

postpf = open('postPosition.txt', 'r', encoding='utf-8')
postpl = postpf.readlines()
postp = []
for i in range(len(postpl)):
    postp.append(postpl[i].strip('.\n'))

hadayf = open('joyolist.txt', 'r', encoding='utf-8')
hadayl = hadayf.readlines()
haday = []
for i in range(len(hadayl)):
    haday.append(hadayl[i].strip('.\n'))

file = open('news.csv', 'r', encoding='utf-8')
comments = file.readlines()

polar_scores = common.load_polar_scores()


new_comment = input("댓글을 입력하세요: ")
new_nounlist = get_nounlist(new_comment)

top3 = []

count = 0
for comment in comments:
    splited = comment.split(',')
    joined = " ".join(splited[3:])
    nounlist = get_nounlist(joined)
    max_min = get_maxmin(nounlist)
    for i in range(len(nounlist)):
        for j in range(len(new_nounlist)):
            if new_nounlist[j][0] == nounlist[i][0]:
                distance = get_distance(j, i, max_min)
                top3.append([distance, count])
    count = count + 1

top3.sort(reverse=True)
print(top3)

P = 0
for i in range(0, 3):
    splited_top3 = comments[top3[i][1]].split(',')
    if splited_top3[3] == "P":
        P = P + 1

if P >= 2:
    print("긍정적인 댓글입니다.")
else:
    print("부정적인 댓글입니다.")
