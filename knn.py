from dataclasses import dataclass, field
from math import sqrt
from queue import PriorityQueue

from comment import Comment
from label import Label


class KNN:
    def __init__(self, comments: list[Comment]) -> None:
        """
        K-NN 모델을 생성합니다. comments는 모델의 훈련에 쓰이며, 댓글의 label은 긍정 또는 부정이어야만 합니다.
        """
        self.__max_cache = dict[str, int]()
        self.__min_cache = dict[str, int]()

        for comment in comments:
            assert comment.label != Label.UNKNOWN, '학습에 쓰일 댓글의 label은 긍정 또는 부정이어야만 합니다'

        self.comments = comments
        for comment in comments:
            for word in comment.get_words():
                freq = comment.count(word)

                if word not in self.__max_cache:
                    # 캐시 추가
                    self.__max_cache[word] = freq
                    self.__min_cache[word] = freq
                else:
                    # 캐시 갱신
                    if freq > self.__max_cache[word]:
                        self.__max_cache[word] = freq

                    if freq < self.__min_cache[word]:
                        self.__min_cache[word] = freq

        assert len(self.__min_cache) == len(self.__max_cache),\
            '최소값 캐시와 최대값 캐시의 갯수가 불일치합니다.'

    def predict(self, x: Comment) -> Label:
        """
        새로운 댓글 x의 긍부정 여부를 예측합니다.
        """
        K = 3

        # 최소 거리의 댓글을 빠르게 찾기 위한 (거리, 댓글)의 우선 순위 큐 생성
        @dataclass(order=True)
        class DistanceCommentPair:
            distance: float
            comment: Comment = field(compare=False)  # 댓글 간 비교 금지
        heap = PriorityQueue[DistanceCommentPair](maxsize=len(self.comments))

        # x와 기존 댓글 간 거리 계산
        for comment in self.comments:
            sum_term = 0
            for word in self.__max_cache.keys():
                dividend = x.count(word) - comment.count(word)

                divisor = self.__max_cache[word] - self.__min_cache[word]
                divisor = 1 if divisor == 0 else divisor

                sum_term += (dividend/divisor) ** 2

            distance = sqrt(sum_term)
            heap.put(DistanceCommentPair(distance, comment))

        # 가장 가까운 댓글 k개 가져오기
        num_positive_comments = 0
        for _ in range(K):
            if heap.get().comment.label == Label.POSITIVE:
                num_positive_comments += 1

        if num_positive_comments > K // 2:
            return Label.POSITIVE
        else:
            return Label.NEGATIVE
