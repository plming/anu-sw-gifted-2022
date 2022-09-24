from math import sqrt
from typing import List, Dict, Tuple
import common


def get_nounlist(comment: str) -> List[str]:
    """
    주어진 댓글에서 명사들을 추출해 리스트에 담아 반환합니다.
    명사는 리스트 내 중복될 수 있습니다.
    """
    noun_list: List[str] = []

    for split in comment.split(' '):
        if split in noun:
            noun_list += [split]
        elif common.combi2(split) != []:
            noun_list += common.combi2(split)
        elif common.combi3(split) != []:
            noun_list += common.combi3(split)

    return noun_list


def get_distance(x: Dict[str, int], y: Dict[str, int], max_frequency: Dict[str, int], min_frequency: Dict[str, int]) -> float:
    sum_term = 0

    all_words = set(x.keys()).union(y.keys())

    DEFAULT_VAL = 0
    for word in all_words:
        # TODO: 분모가 0일 경우 기본값이 1인가?
        dividend = x.get(word, DEFAULT_VAL) - y.get(word, DEFAULT_VAL)
        divisor = max_frequency.get(word, DEFAULT_VAL) \
            - min_frequency.get(word, DEFAULT_VAL)
        divisor = 1 if divisor == 0 else divisor

        sum_term += (dividend / divisor) ** 2

    return sqrt(sum_term)


def parse(text: str) -> Dict[str, int]:
    nouns = get_nounlist(text)
    return common.get_word_count_pair(nouns)


noun = common.load_nouns()
postp = common.load_postpositions()
haday = common.load_haday()

# train 댓글을 가져오기
train_data = common.read_from_csv("train.csv")

# 모든 댓글에 대해 max, min 찾고
max_frequency_cache: Dict[str, int] = {}
min_frequency_cache: Dict[str, int] = {}

for comment in train_data:
    label, text = comment
    extracted_nouns = get_nounlist(text)
    word_count = common.get_word_count_pair(extracted_nouns)

    for word, count in word_count.items():
        if word not in max_frequency_cache \
                or max_frequency_cache[word] < count:
            max_frequency_cache[word] = count

        if word not in min_frequency_cache:
            min_frequency_cache[word] = 0
        elif min_frequency_cache[word] > count:
            min_frequency_cache[word] = count

    assert len(max_frequency_cache) == len(min_frequency_cache)

# 검증용 댓글 불러오기
test_data = common.read_from_csv("test.csv")

LABEL_COLUMN_INDICE = 0
TEXT_COLUMN_INDICE = 1
num_matched = 0
for test in test_data:
    # 훈련 데이터와의 거리-인덱스 쌍을 담는 리스트
    distance_index_pairs: List[Tuple[float, int]] = []

    # 훈련 데이터와 거리 계산하기
    for i in range(len(train_data)):
        distance = get_distance(x=parse(train_data[i][TEXT_COLUMN_INDICE]),
                                y=parse(test[TEXT_COLUMN_INDICE]),
                                max_frequency=max_frequency_cache,
                                min_frequency=min_frequency_cache)
        pair = (distance, i)
        distance_index_pairs.append(pair)

    # 거리를 key로 오름차순 정렬
    distance_index_pairs.sort()

    # 가장 가까운 댓글들을 찾아 레이블 예측하기
    NUM_NEAREST_NEIGHBORS = 3
    num_positive_comments = 0
    for i in range(NUM_NEAREST_NEIGHBORS):
        distance, index = distance_index_pairs[i]
        if train_data[index][LABEL_COLUMN_INDICE] == "P":
            num_positive_comments += 1

    if num_positive_comments > NUM_NEAREST_NEIGHBORS // 2:
        predict = "P"
    else:
        predict = "N"

    # 레이블이 실제와 예측하는지 확인
    if predict == test[LABEL_COLUMN_INDICE]:
        num_matched += 1

print(f"정확도(%): {num_matched / len(test_data) * 100}")
