# Import the itertools, time libarary
# This library ships with Python 3 so you don't have to download anything
import itertools
import time


def load_polar_scores() -> dict:
    polar_scores = {}
    file = open('dicty.txt', 'r', encoding='utf-8')
    lines = file.readlines()
    for line in lines:
        key, value = line.strip('.\n').split(',')
        polar_scores[key] = int(value)

    return polar_scores


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
        result.append((word_list[start], end - start))
        start = end
    return result


def evaluate(comment):
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
    print(c)
    print(type(c[0]))
    print(c[0][0])
    try:
        for i in range(len(c)):
                if polar_scores[c[i][0]] != 0:
                    print(c[i][0], polar_scores[c[i][slice(0)]])
    except KeyError:
        print('Not Found')
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
count = 0
matched = 0
print('추출된 단어, 극성단어 갯수, 결과(점수), 댓글')
time.sleep(1.5)
for comment in comments:
    splited = comment.split(',')
    joined = " ".join(splited[3:])
    score = evaluate(joined)
    label = splited[3]
#기준치 : 0.4
    if score == 0:
        count = count + 1

    if score >= 0.4:
        score1 = "P"
    else:
        score1 = "N"

    if label == score1:
        print(splited[0] + ": correct", score)
        matched = matched + 1
        print(comment)
    else:
        print(splited[0] + ": incorrect", score)
        print(comment)

# 정확도 출력
print('정확도:', matched/(len(comments)))
print(count)
print(len(comments))


# Create a sliced dictionary
# dict() is used to convert the iterable result of itertools.islice() to a new dictionary
#slicedDict = dict(itertools.islice(myDictionary.items(), 1 ,3))

# print(slicedDict)
