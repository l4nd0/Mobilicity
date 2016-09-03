from collections import Counter

__author__ = 'LEONARDO'

import networkx as nx
import matplotlib.pyplot as plt
import community
from mpl_toolkits.basemap import Basemap as Basemap

nyc_net = nx.read_edgelist('edges2.csv', delimiter = ",", create_using=nx.DiGraph(), nodetype=str)
N, K = nx.number_of_nodes(nyc_net), nx.number_of_edges(nyc_net)
print(N)
avg_deg = K/float(N)

b = Counter(nyc_net.out_degree())
print("Bases Evento")
for k, v in b.most_common(5):
    print '%s: %i' % (k, v)

cb = Counter(nyc_net.in_degree())
print("Bases Evento")
for k, v in cb.most_common(5):
    print '%s: %i' % (k, v)

'''
in_values = list(set(nyc_net.in_degree().values()))
out_values = list(set(nyc_net.out_degree().values()))
in_values.sort()
out_values.sort()
in_hist = [0]*len(in_values)
out_hist = [0]*len(out_values)

for k, v in nyc_net.in_degree().items():
    index = in_values.index(v)
    in_hist[index] += 1

for k2, v2 in nyc_net.out_degree().items():
    index = out_values.index(v2)
    out_hist[index] += 1

nyc_net_ud = nyc_net.to_undirected()
nyc_net_components = list(nx.connected_component_subgraphs(nyc_net_ud))
nyc_net_mc = nyc_net_components[0]

N_mc, K_mc = nx.number_of_nodes(nyc_net_mc), nx.number_of_edges(nyc_net_mc)
avg_deg_mc = float(2*K_mc)/N_mc
avg_clust = nx.average_clustering(nyc_net_mc)

part = community.best_partition(nyc_net_mc)
values = [part.get(node) for node in nyc_net_mc.nodes()]
'''
m = Basemap(
        projection='merc',
        llcrnrlon=-82.139826,
        llcrnrlat=-4.1558195,
        urcrnrlon=-75.6029607,
        urcrnrlat=0.4218267,
        lat_ts=0,
        resolution='i',
        suppress_ticks=True)

posDict = {}
lats = []
long = []
g = open("nodes.csv", 'r')
i = 0
for line in g:
    if i == 0:
        i+=1
        continue
    meta_data = line.split(",")
    posDict[(meta_data[0][1:-1])] = (float(meta_data[1][1:-1]), float(meta_data[2][1:-1]))
    lats.append(float(meta_data[1][1:-1]))
    long.append(float(meta_data[2][1:-1]))
mx, my = m(long, lats)

i = 0
for elem in my:
    posDict[i] = (mx[i], elem)
    i +=1
print(posDict)
nx.draw_networkx(nyc_net, cmap = plt.get_cmap('jet'), pos=posDict, node_size=25, with_labels=False, width = 0.10)


m.drawcountries()
m.drawstates()
m.bluemarble()
m.drawcoastlines()
#m.drawmapboundary(fill_color='aqua')
#m.fillcontinents(color='coral',lake_color='aqua')
'''
mod = community.modularity(part, nyc_net_mc)
print("modularity:", mod)
betweeness_top10 = []
betweeness_cent = nx.betweenness_centrality(nyc_net_mc)
betweeness_cent_avg = sum(betweeness_cent.values())/N_mc
#Saco los valores del betweeness centrality en una lista, y la ordeno descendientemente
values = betweeness_cent.values()
values.sort()
values.reverse()
#Encuentro a que nodos pertenecen los 10 mayores valores
for elem in values:
    for key, v in betweeness_cent.items():
        if v == elem:
            betweeness_top10.append(key)
            break
    if len(betweeness_top10) == 10:
        break

#Mismo proceso para el eigen vector centrality
eigenvector_top10 = []
eigenvector_cent = nx.eigenvector_centrality(nyc_net_mc)
eigenvector_cent_avg = sum(eigenvector_cent.values())/N_mc
valuesE = eigenvector_cent.values()
valuesE.sort()
valuesE.reverse()
for elem in valuesE:
    for key, v in eigenvector_cent.items():
        if v == elem:
            eigenvector_top10.append(key)
            break
    if len(eigenvector_top10) == 10:
        break

#Luego, busco estos nodos en mi archivo que contiene el metadata, para obtener el lugar. Que sera
#almacenado en una lista de top 10 lugares
bet_top10_places = []
eig_top10_places = []
for elem in betweeness_top10:
    f = open("foursquare_nyc.csv", "r")
    for line in f:
        meta_data = line.split(",")
        if str(elem) == meta_data[0]:
            bet_top10_places.append(meta_data[1])
            break
    f.close()

for elem in eigenvector_top10:
    f = open("foursquare_nyc.csv", "r")
    for line in f:
        meta_data = line.split(",")
        if str(elem) == meta_data[0]:
            eig_top10_places.append(meta_data[1])
            break
    f.close()

print
print "Betweeness Centrality Top 10 Places: "
for elem in bet_top10_places:
    print elem

print "Eigen Vector Centrality Top 10 Places: "
for elem in eig_top10_places:
    print elem


print "Graph Betweeness Centrality", betweeness_cent_avg
print "Graph Eigen Vector Centrality", eigenvector_cent_avg

print "Average Clustering Coefficient NON - Random Giant: ", avg_clust

p = float(K_mc)/(N_mc*(N_mc-1)/2)
G = nx.erdos_renyi_graph(N_mc, p)
G_un = G.to_undirected()
G_components = list(nx.connected_component_subgraphs(G_un))
G_mc = G_components[0]
GN_mc, GK_mc = nx.number_of_nodes(G_mc), nx.number_of_edges(G_mc)
avg_deg_Gmc = float(2*GK_mc)/GN_mc
avg_clust_random = nx.average_clustering(G_mc)
print "Average Clustering Coefficient Random: ", avg_clust_random

plt.figure(figsize=(10, 10))
nx.draw(G)

plt.axis("tight")

plt.figure()
plt.loglog(in_values,in_hist,'ro-')
plt.loglog(out_values,out_hist,'bv-')
plt.legend(['In-degree','Out-degree'])
plt.xlabel('Degree')
plt.ylabel('Number of nodes')
plt.title('Network of places in New York')
plt.grid(True)
'''
plt.show()
