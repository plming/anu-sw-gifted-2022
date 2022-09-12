from label import Label
from tokenizer import Tokenizer


class Comment:
    # static variable
    __tokenizer = Tokenizer()

    def __init__(self, text: str, label: Label) -> None:
        self.text = text
        self.label = label
        # 단어 빈도수 캐시
        self.word_count = dict[str, int]()

        # 문장에서 명사 추출
        nouns = Comment.__tokenizer.get_nouns(text)

        # 각 명사별 빈도수 캐싱
        for noun in nouns:
            self.word_count[noun] = self.word_count.get(noun, 0) + 1

    def count(self, word: str) -> int:
        """
        댓글 내 단어의 빈도수를 반환합니다. 해당 단어가 댓글에 없을 경우 0을 반환합니다.
        """
        return self.word_count.get(word, 0)

    def get_words(self) -> set[str]:
        """
        댓글의 단어 집합을 반환합니다.
        """
        return set(self.word_count.keys())

    def __str__(self) -> str:
        return f'label={self.label}, text={self.text}'

    def __repr__(self) -> str:
        return self.__str__()


def read_from_csv(file_name: str) -> list[Comment]:
    """
    csv 파일로부터 댓글을 불러옵니다.
    csv파일의 컬럼은 id, username, datetime, label, text입니다.
    """
    LABEL_COLUMN_INDEX = 3
    TEXT_COLUMN_INDEX = 4

    comments = list[Comment]()
    with open(file_name, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    for line in lines:
        strips = line.split(',')

        if strips[LABEL_COLUMN_INDEX] == 'P':
            label = Label.POSITIVE
        elif strips[LABEL_COLUMN_INDEX] == 'N':
            label = Label.NEGATIVE
        else:
            assert False, "label must be P or N"

        text = "".join(strips[TEXT_COLUMN_INDEX:])
        comment = Comment(text, label)
        comments.append(comment)

    return comments
