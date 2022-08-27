f = open('news.csv', 'r', encoding='utf-8')
coms = f.readlines()

nounf = open('noun.txt', 'r',encoding='utf-8')
nounl = nounf.readlines()
noun = []
for i in range(len(nounl)):
    noun.append(nounl[i].strip('.\n'))

postpf = open('postPosition.txt', 'r',encoding='utf-8')
postpl = postpf.readlines()
postp = []
for i in range(len(postpl)):
    postp.append(postpl[i].strip('.\n'))
    
hadayf = open('joyolist.txt', 'r', encoding='utf-8')
hadayl = hadayf.readlines()
haday = []
for i in range(len(hadayl)):
    haday.append(hadayl[i].strip('.\n'))

def combi2(t):
    n = len(t)
    for i in range(n-1, 0, -1):
        if (t[0:i] in noun and t[i:n] in haday):
            return [t[0:i]]
        elif (t[0:i] in noun and t[i:n] in noun):
            return [t[0:i], t[i:n]]
        elif (t[0:i] in noun and t[i:n] in postp):
            return [t[0:i]]
    return []


def combi3(t):
    n = len(t)
    for i in range(1, n):
        for j in range(i+1, n):
            if (t[0:i] in noun and t[i:j] in noun and t[j:n] in postp):
                return [t[0:i], t[i:j]]
    return []

def combi4(t):
    n = len(t)
    for i in range(1, n):
        for j in range(i+1, n):
            for k in range(i+2, n):
                if (t[0:i] in noun and t[i:j] in noun and t[j:k] in haday and t[k:n] == '!' or '?' or '.'):
                    return [t[0:i], t[i:j]]
    return []

print(coms)