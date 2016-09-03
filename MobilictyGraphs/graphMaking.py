__author__ = 'LEONARDO'
'''
nodes = open("nodes.txt",'r')
libraryNodes = open("lnodes.txt", 'w')
libraryNodes.write('"nodes":[\n')
i = 0
for line in nodes:
    line = line.strip()
    if i ==0:
        i+=1
        continue
    info = line.split(",")
    y = info[1][1:-1]
    x = info[2][1:-1]
    id = info[0][1:-1]
    label = info[3][1:-1]
    if label.isdigit():
        label = info[4][1:-1]
    libraryNodes.write('{"y":' + y + ',"x":' + x + ',"id":"' + id + '","label":"' + label + '"},\n')
libraryNodes.write(']}')
libraryNodes.close()
'''

libraryEdges = open("ledges.txt", 'w')
edges = open("edges.txt", "r")
libraryEdges.write('{"edges":[\n')
i = 0
for line in edges:
    line = line.strip()
    if i == 0:
        i+=1
        continue
    info = line.split(",")
    origin = info[0][1:-1]
    destiny = info[1][1:-1]
    if destiny == "?":
        continue
    libraryEdges.write('{"source":"' + origin + '", "target":"' + destiny + '"},\n')
libraryEdges.write("],\n")