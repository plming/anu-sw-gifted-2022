

def load_polar_scores():
    polar_scores = {}
    file = open('dicty.txt', 'r', encoding='utf-8')
    lines = file.readlines()
    for line in lines:
        key, value = line.strip('.\n').split(',')
        polar_scores[key] = int(value)

    return polar_scores


def get_word_count_pair_list(word_list: list):
    '''
    명사 리스트를 (명사, 빈도수) 리스트로 변환
    get_word_count_pair_list(['apple', 'apple']) == [('apple', 2)] 
    '''
    word_list = sorted(word_list)
    result = {}
    start = 0
    end = 0
    while start < len(word_list):
        while end < len(word_list) and word_list[start] == word_list[end]:
            end = end + 1
        result[word_list[start]] = end - start
        start = end
    return result


def combi2(word):
    n = len(word)
    for i in range(n-1, 0, -1):
        if (word[0:i] in nouns and word[i:n] in haday):
            return [word[0:i]]
        elif (word[0:i] in nouns and word[i:n] in nouns):
            return [word[0:i], word[i:n]]
        elif (word[0:i] in nouns and word[i:n] in postpositions):
            return [word[0:i]]
    return []


def combi3(word):
    n = len(word)
    for i in range(1, n):
        for j in range(i+1, n):
            if (word[0:i] in nouns and word[i:j] in nouns and word[j:n] in postpositions):
                return [word[0:i], word[i:j]]
    return []


def get_nouns():
    nounf = open('noun.txt', 'r', encoding='utf-8')
    nounl = nounf.readlines()
    noun = []
    for i in range(len(nounl)):
        noun.append(nounl[i].strip('.\n'))
    return noun


def get_postpositions():
    postpf = open('postPosition.txt', 'r', encoding='utf-8')
    postpl = postpf.readlines()
    postpositions = []
    for i in range(len(postpl)):
        postpositions.append(postpl[i].strip('.\n'))
    return postpositions


def get_haday():
    hadayf = open('joyolist.txt', 'r', encoding='utf-8')
    hadayl = hadayf.readlines()
    haday = []
    for i in range(len(hadayl)):
        haday.append(hadayl[i].strip('.\n'))
    return haday


def get_comments() -> list[dict]:
    result = []

    nouns = get_nouns()

    file = open('news_list.csv', 'r', encoding='utf-8')
    comments = file.readlines()
    for comment in comments:
        word_list = comment.split(' ')

        # 댓글에서 명사 분리
        noun_list = []
        for i in range(len(word_list)):
            if word_list[i] in nouns:
                noun_list.append(word_list[i])
            elif combi2(word_list[i]) != []:
                t = combi2(word_list[i])
                for j in range(len(t)):
                    noun_list.append(t[j])
            elif combi3(word_list[i]) != []:
                t = combi3(word_list[i])
                for j in range(len(t)):
                    noun_list.append(t[j])

        # 댓글을 {단어: 빈도수}로 만들기
        parsed = get_word_count_pair_list(noun_list)
        result.append(parsed)

    return result


# global variables
nouns = get_nouns()
haday = get_haday()
postpositions = get_postpositions()
