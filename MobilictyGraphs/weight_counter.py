__author__ = 'LEONARDO'

weights = {}
f = open('edges2.csv', 'r')
new = open('edges_weights.txt', 'w')
i = 0
for line in f:
    if i == 0:
        i+=1
        continue
    line = line.strip()
    con = line
    if con not in weights:
        weights[con] = 0
    weights[con] +=1
new.write("Source,Target,Weight\n")
f.close()
print len(weights)
for k, v in weights.items():
    new.write(k+","+str(v)+'\n')
new.close()
