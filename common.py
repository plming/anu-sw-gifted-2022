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
    result = []
    start = 0
    end = 0
    while start < len(word_list):
        while end < len(word_list) and word_list[start] == word_list[end]:
            end = end + 1
        result.append((word_list[start], end - start))
        start = end
    return result