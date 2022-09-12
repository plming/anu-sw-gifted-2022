from comment import Comment, read_from_csv
from knn import KNN
from label import Label
from time import time

if __name__ == '__main__' :
    TEST_TEXT = '정말 좋습니다'

    start = time()
    train_data = read_from_csv('news.csv')
    test_data = Comment(TEST_TEXT, Label.UNKNOWN)

    model = KNN(train_data)
    is_positive = model.predict(test_data)
    print(f'예측 결과: {is_positive}')

    print(f'수행시간(s): {time() - start}')
