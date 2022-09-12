class Tokenizer():
    def __init__(self) -> None:
        self.__noun = set[str]()
        self.__postposition = set[str]()
        self.__haday = set[str]()

        with open('noun.txt', 'r', encoding='utf-8') as file:
            lines = file.readlines()
            for line in lines:
                self.__noun.add(line.strip('.\n'))

        with open('postPosition.txt', 'r', encoding='utf-8') as file:
            lines = file.readlines()
            for line in lines:
                self.__postposition.add(line.strip('.\n'))

        with open('joyolist.txt', 'r', encoding='utf-8') as file:
            lines = file.readlines()
            for line in lines:
                self.__haday.add(line.strip('.\n'))

    def get_nouns(self, text: str) -> list[str]:
        splits = text.split(' ')
        nouns = list[str]()
        for split in splits:
            nouns += self.pick_nouns(split)
        return nouns

    def read_from_csv(self):
        pass

    def pick_nouns(self, word: str) -> list[str]:
        assert len(word.split(" ")) == 1, 'word는 하나의 단어여야만 합니다.'

        if word in self.__noun:
            return [word]

        ret = self.combi2(word)
        if len(ret) != 0:
            return ret

        ret = self.combi3(word)
        return ret

    def combi2(self, word: str) -> list[str]:
        """
        어절을 2개의 요소(명사+하다용언, 명사+명사, 명사+조사)로 분리하여 명사 추출합니다.
        분리가 가능한 경우, 명사들을 리스트에 담아 반환합니다.
        분리가 안되는 경우, 빈 리스트를 반환합니다.
        """
        for i in range(len(word)-1, 0, -1):
            front, rear = word[:i], word[i:]
            if front in self.__noun and rear in self.__haday:
                return [front]
            elif front in self.__noun and rear in self.__noun:
                return [front, rear]
            elif front in self.__noun and rear in self.__postposition:
                return [front]
        return []

    def combi3(self, word: str) -> list[str]:
        """
        어절을 3개의 요소(명사+명사+조사)로 분리하여 명사 추출합니다.
        분리가 가능한 경우, 명사들을 리스트에 담아 반환합니다.
        분리가 안되는 경우, 빈 리스트를 반환합니다.
        """
        for i in range(1, len(word)):
            for j in range(i+1, len(word)):
                front, mid, rear = word[:i], word[i:j], word[j:]
                if front in self.__noun and mid in self.__noun and rear in self.__postposition:
                    return [front, mid]
        return []
