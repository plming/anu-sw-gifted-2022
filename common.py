from typing import Dict, List, Set, Tuple
import csv


def read_from_csv(file_name: str) -> List[Tuple[str, str]]:
    """
    csv 파일에서 댓글, 레이블을 가져옵니다.
    """
    result: List[Tuple[str, str]] = []

    with open(file_name, newline='', encoding='utf-8') as csv_file:
        rows = csv.reader(csv_file)
        for row in rows:
            assert len(row) == 2, '컬럼 갯수가 맞지 않습니다'
            assert row[0] in ['P', 'N'], '레이블은 P 또는 N이여야만 합니다'
            result.append((row[0], row[1]))
            
    return result


def load_polar_scores() -> Dict[str, int]:
    """
    극성점수 불러오기
    """
    WORST_SCORE = 1
    BEST_SCORE = 5

    polar_scores: Dict[str, int] = dict()
    with open('dicty.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()
        for line in lines:
            word, score = line.strip('.\n').split(',')
            assert word not in polar_scores, f"중복된 단어: {word}"

            polar_scores[word] = int(score)
            assert polar_scores[word] >= WORST_SCORE \
                and polar_scores[word] <= BEST_SCORE, f"점수가 범위를 벗어남: {word}"

    return polar_scores


def get_word_count_pair(word_list: List[str]) -> Dict[str, int]:
    """
    명사 리스트를 {명사: 빈도수, ...}로 변환
    ex. get_word_count_pair_list(['apple', 'apple']) == {'apple': 2} 
    """
    word_list = sorted(word_list)
    result: Dict[str, int] = dict()
    start = 0
    end = 0
    while start < len(word_list):
        while end < len(word_list) and word_list[start] == word_list[end]:
            end = end + 1
        result[word_list[start]] = end - start
        start = end
    return result


def combi2(word: str) -> List[str]:
    """
    * 어절을 2개의 요소(명사+하다용언, 명사+명사, 명사+조사)로 분리하여 명사 추출
    * 분리가 가능한 경우, 명사들을 리스트에 담아 반환
    * 분리가 안되는 경우, 빈 리스트 반환
    """
    for i in range(len(word)-1, 0, -1):
        front, rear = word[:i], word[i:]
        if front in nouns and rear in haday:
            return [front]
        elif front in nouns and rear in nouns:
            return [front, rear]
        elif front in nouns and rear in postpositions:
            return [front]
    return []


def combi3(word: str) -> List[str]:
    """
    * 어절을 3개의 요소(명사+명사+조사)로 분리하여 명사 추출
    * 분리가 가능한 경우, 명사들을 리스트에 담아 반환
    * 분리가 안되는 경우, 빈 리스트 반환
    """
    for i in range(1, len(word)):
        for j in range(i+1, len(word)):
            front, mid, rear = word[:i], word[i:j], word[j:]
            if front in nouns and mid in nouns and rear in postpositions:
                return [front, mid]
    return []


def load_nouns() -> Set[str]:
    """
    명사 집합 불러오기
    """
    noun: Set[str] = set()
    with open('noun.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()
        for line in lines:
            noun.add(line.strip('.\n'))
    return noun


def load_postpositions() -> Set[str]:
    """
    조사 집합 불러오기
    """
    postpositions: Set[str] = set()
    with open('postPosition.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()
        for line in lines:
            postpositions.add(line.strip('.\n'))
    return postpositions


def load_haday() -> Set[str]:
    """
    하다 용언 집합 불러오기
    """
    haday: Set[str] = set()
    with open('joyolist.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()
        for line in lines:
            haday.add(line.strip('.\n'))
    return haday


def get_comments() -> List[Dict[str, int]]:
    with open('news.csv', 'r', encoding='utf-8') as file:
        comments = file.readlines()

    result: List[Dict[str, int]] = list()
    nouns = load_nouns()
    for comment in comments:
        # 댓글을 어절로 분리
        word_list = comment.split(' ')

        # 어절에서 명사 분리
        noun_list = List[str]()
        for word in word_list:
            if word in nouns:
                noun_list.append(word)
                continue

            ret = combi2(word)
            if len(ret) != 0:
                noun_list += ret
                continue

            ret = combi3(word)
            noun_list += ret

        # 댓글을 {단어: 빈도수}로 만들기
        parsed = get_word_count_pair(noun_list)
        result.append(parsed)

    return result


# global variables
nouns = load_nouns()
haday = load_haday()
postpositions = load_postpositions()
