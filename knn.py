"""
1. 명사 분리

2. 모든 댓글에 대해 max, min 구하기
3. 댓글 2개의 거리 구하기 - 최대, 최소

"""
from math import sqrt
from common import *


def get_max_min(comments: list[dict]):
    """
    { "apple": {
        "max": 2,
        "min": 1
    }
    }
    """
    result = {}
    for comment in comments:
        for word, count in comment.items():
            if word not in result:
                result[word] = {"max": count, "min": count}
            else:
                if count > result[word]["max"]:
                    result[word]["max"] = count

                if count < result[word]["min"]:
                    result[word]["min"] = count
    return result


def get_distance(first: dict, second: dict, max_min: dict[dict]) -> float:
    sum_term = 0
    for word, value in max_min.items():
        dividend = (first.get(word, 0) - second.get(word, 0))
        divisor = value['max'] - value['min']
        divisor = 1 if divisor == 0 else divisor
        sum_term += (dividend/divisor) ** 2

    return sqrt(sum_term)


comments = get_comments()

max_min = get_max_min(comments)

for i in range(len(comments)):
    for j in range(i+1, len(comments)):
        distance = get_distance(comments[i], comments[j], max_min)
        print(f"dist between {i} and {j}: {distance}")
