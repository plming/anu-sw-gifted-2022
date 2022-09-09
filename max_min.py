import common

word_group = []
result = []


def get_distance(comment):
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
    c = common.get_word_count_pair_list(noun_list)

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
                    c_count += 1

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


noun = common.load_nouns()
postp = common.load_postpositions()
haday = common.load_haday()
polar_scores = common.load_polar_scores()

with open('news.csv', 'r', encoding='utf-8') as file:
    comments = file.readlines()

matched = 0
for comment in comments:
    splited = comment.split(',')
    joined = " ".join(splited[3:])
    score = get_distance(joined)
    label = splited[3]

    THRESHOLD = 0.4
    predict = "P" if score >= THRESHOLD else "N"

    if label == predict:
        matched += 1

for word, max, min in word_group:
    if max == min:
        print("1")
    else:
        print(max-min)

# 정확도 출력
