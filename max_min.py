from common import *


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


word_group = []
result = []


def get_distance(comment):
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

    if len(word_group) == 0:
        for word in c:
            word_group.append([word[0], word[1], word[1]])
    else:
        for i in range(0, len(c)):
            c_count = 0
            for j in range(0, len(word_group)):
                if c[i][0] == word_group[j][0]:
                    if c[i][1] > word_group[j][1]:
                        word_group[j][1] = c[i][1]
                    if c[i][1] < word_group[j][2]:
                        word_group[j][2] = c[i][1]
                else:
                    c_count = c_count + 1

            if c_count == len(word_group):
                word_group.append([c[i][0], c[i][1], c[i][1]])
                c_count = 0

    num_words = 0
    sum_of_product = 0
    for i in range(len(c)):
        word, frequency = c[i]
        num_words += frequency
        score = polar_scores.get(word, 0)
        sum_of_product += score * frequency

    if num_words == 0:
        # 댓글에서 명사를 발견 못한 경우
        return -1

    return sum_of_product/num_words


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

polar_scores = load_polar_scores()

matched = 0
for comment in comments:
    splited = comment.split(',')
    joined = " ".join(splited[3:])
    score = get_distance(joined)
    label = splited[3]
#기준치 : 0.4
    if score >= 0.4:
        score = "P"
    else:
        score = "N"

    if label == score:
        matched = matched + 1

for word, max, min in word_group:
    if max == min:
        print("1")
    else:
        print(max-min)

# 정확도 출력
