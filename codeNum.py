from Lex import Lex

L = Lex()
Dic = {}
L.coding()
print(len(L.bianma))
#print(L.bianma.values())
bianMa = []
bianMaNew = []
print(L.bianma)
i = 1
for tmp in L.bianma:
    #print(tmp)
    bianMa.append(tmp)
#print(bianMa[0])
print(len(bianMa))
for i in range(66):
    for j in range(66):
        if L.bianma[bianMa[i]] > L.bianma[bianMa[j]]:
            tmp = bianMa[i]
            bianMa[i] = bianMa[j]
            bianMa[j] = tmp
index = 0
with open('bianma.txt','w') as f:
    for i in range(0,32):
        if index%5 == 0:
            f.write('\n')
        f.write('('+str(L.bianma[bianMa[i]])+','+bianMa[i]+')')
        f.write('  ')
        index+= 1