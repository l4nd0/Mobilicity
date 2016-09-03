__author__ = 'LEONARDO'

f = open("nodes.txt", 'r')
i=0
nodos = []
for line in f:
    line = line.strip()
    if i == 0:
        i+=1
        continue
    nodos.append(line.split(",")[0][1:-1])
f.close()
print("Finished")
f = open("edges.txt", "r")
i=0
ejes = []
for line in f:
    line = line.strip()
    if i == 0:
        i+=1
        continue
    info = line.split(",")
    if info[0][1:-1] not in nodos or info[0][1:-1] not in nodos:
        print ("En la linea ", i, " no existe un nodo")
    i+=1
f.close()