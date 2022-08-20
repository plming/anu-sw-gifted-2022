f1 = open('news(1).csv', 'r')
coms1 = f1.readlines()

f2 = open('news(2).csv', 'r')
coms2 = f2.readlines()

f3 = open('news(3).csv', 'r')
coms3 = f3.readlines()

f4 = open('news(4).csv', 'r')
coms4 = f4.readlines()


def spl(a):
    final = ['']
    for i in range(len(a)):
        final[i] = a[i].split('\t')
        if i + 1 != len(a):
            final = final + ['']
    return final

def comb(a):
    final = ['']
    for i in range(len(a)):
        final[i] = a[i][:3] + [','.join(a[i][3:])]
        if i+1 != len(a):
            final = final + ['']
    return final


ce1 = comb(spl(coms1))
ce2 = comb(spl(coms2))
ce3 = comb(spl(coms3))
ce4 = comb(spl(coms4))

k = 0
res = []

for i in range(len(ce1)):
    if ce1[i][3] == ce2[i][3] == ce3[i][3] == ce4[i][3]:
        k = k + 1
    else:
        res = res + [ce1[i]]

import csv

with open('tes.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(res)
        




