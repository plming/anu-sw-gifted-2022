f = open('news.csv', 'r', encoding='utf-8')
coms = f.readlines()

import random

samples = random.sample(range(len(coms)), 20)

train = open('train.csv', 'w', encoding='utf-8')
test = open('test.csv', 'w', encoding='utf-8')


for i in range(len(coms)):
    if i in samples:
        test.write(coms[i])
    else:
        train.write(coms[i])
