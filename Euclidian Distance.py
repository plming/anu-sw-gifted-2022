nounf = open('noun.txt', 'r')
nounl = nounf.readlines()
noun = []
for i in range(len(nounl)):
    noun.append(nounl[i].strip('.\n'))

postpf = open('postPosition.txt', 'r')
postpl = postpf.readlines()
postp = []
for i in range(len(postpl)):
    postp.append(postpl[i].strip('.\n'))
    
hadayf = open('joyolist.txt', 'r')
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

def coun(a):
    b = []
    n = len(a)
    st= 0
    end = 0
    while st < n :
        while end < n and a[st] == a[end]:
            end = end + 1
        b.append((a[st], end-st))
        st = end
    return b

f = open('newss.csv', 'r', )
a = f.readlines()
n = len(a)
b = []

for i in range(n):
    t = a[i].strip('.\n')
    b = b + t.split()
h = []

for i in range(len(b)):
    if b[i] in noun:
        h.append(b[i])
    elif combi2(b[i]) != []:
         t = combi2(b[i])
         for j in range(len(t)):
             h.append(t[j])
    elif combi3(b[i]) != []:
        t = combi3(b[i])
        for j in range(len(t)):
            h.append(t[j])
h.sort()
c1 = coun(h)
print(c1)

'''f = open('input2.txt', 'r', encoding='utf-8')
a = f.readlines()
n = len(a)
b = []

for i in range(n):
    t = a[i].strip('.\n')
    b = b + t.split()
print(b)
e = []

for i in range(len(b)):
    if b[i] in noun:
        e.append(b[i])
    elif combi2(b[i]) != []:
         t = combi2(b[i])
         for j in range(len(t)):
             e.append(t[j])
    elif combi3(b[i]) != []:
        t = combi3(b[i])
        for j in range(len(t)):
            e.append(t[j])
            
e.sort()
c2 = coun(e)
print(c2)

s=0
cp1=0
cp2=0

while True :
    
    if (c1[cp1][0] > c2[cp2][0]) :
        s=s+(c2[cp2][1])**2
        if cp2 <len(c2)-1 :
            cp2=cp2+1
    elif (c1[cp1][0]<c2[cp2][0]) :
        s=s+(c1[cp1][1])**2
        if cp1 <len(c1)-1 :
            cp1=cp1+1
    elif (c1[cp1][0]==c2[cp2][0]) :
        s=s+ (c1[cp1][1]-c2[cp2][1])**2
        if cp1 <len(c1)-1 :
            cp1=cp1+1
        if cp2 <len(c2)-1 :
            cp2=cp2+1
    if (cp1==len(c1)-1 and cp2==len(c2)-1) :
         break

print(s)'''
