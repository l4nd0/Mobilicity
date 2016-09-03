from collections import Counter

__author__ = 'LEONARDO'


basesEventos = {}
basesHogar = {}

f = open("C:\\Users\\LEONARDO\\Downloads\\BID\\BID\\EventosManabi.txt", 'r')
print(f.readline())
i = 0
for line in f:
    if i == 0:
        i+= 1
        continue
    line = line.strip()
    info = line.split("\t")
    hogar = info[3][1:-1]
    evento = info[10][1:-1]
    if hogar not in basesHogar:
        basesHogar[hogar] = 0
    if evento not in basesEventos:
        basesEventos[evento] = 0
    basesHogar[hogar] +=1
    basesEventos[evento]+=1
    if i %10000 == 0:
        print("x")
    i+=1
bh = Counter(basesHogar)
be = Counter(basesEventos)
print("Bases Hogar")
for k, v in bh.most_common(20):
    print '%s: %i' % (k, v)

print("Bases Evento")
for k, v in be.most_common(20):
    print '%s: %i' % (k, v)

exit()
#for line in f:

