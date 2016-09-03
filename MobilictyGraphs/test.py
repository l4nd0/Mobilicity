__author__ = 'LEONARDO'
f = open("C:\\Users\\LEONARDO\\Downloads\\BID\\BID\\ResidentesManabi.txt", 'r')
import pandas as pd
from pandas import Series, DataFrame
import matplotlib.pyplot as plt
import matplotlib.style
import numpy as np
matplotlib.style.use('ggplot')

class Base():
    def __init__(self, key, latitud, longitud, nombre, provincia, canton, ciudad, parroquia):
        self.key = key
        self.latitud = latitud
        self.longitud = longitud
        self.nombre = nombre
        self.provincia = provincia
        self.canton = canton
        self.ciudad = ciudad
        self.parroquia = parroquia

    def __eq__(self, other):
        return self.key == other.key

    def mostrar(self):
        print self.key
        print self.latitud
        print self.longitud
        print self.nombre
        print self.provincia
        print self.canton
        print self.ciudad
        print self.parroquia


#data = pd.read_csv("C:\\Users\\LEONARDO\\Downloads\\BID\\BID\\EventosManabi.txt", separator="\t")
nodes = open("nodes.txt", "w")
nodes.write("Key,Latitud,Longitud,Nombre,Canton,Ciudad,Parroquia,Provincia\n")
edges = open("edges.txt", "w")
edges.write("Origen,Destino\n")
nodos = []
i = 0
for line in f:
    i+=1
    if i == 1:
        continue
    line = line.strip()
    info = line.split("\t")
    baseHogar = Base(info[3], info[8], info[9], info[3], info[4], info[5], info[6], info[7])
    baseEvento = Base(info[10], info[16], info[17], info[11], info[12], info[13], info[14], info[15])
    edges.write(baseHogar.key+","+baseEvento.key+"\n")
    if baseHogar.key not in nodos:
        nodos.append(baseHogar.key)
        nodes.write(baseHogar.key +","+ baseHogar.latitud+","+baseHogar.longitud+","+baseHogar.nombre+","+baseHogar.canton+","+baseHogar.ciudad
                + "," + baseHogar.parroquia + ","+ baseHogar.provincia +"\n")
    if baseEvento.key not in nodos and baseEvento.key != "?":
        nodos.append(baseEvento.key)
        nodes.write(baseEvento.key +","+ baseEvento.latitud+","+baseEvento.longitud+","+baseEvento.nombre+","+baseEvento.canton+","+baseEvento.ciudad
                + "," + baseEvento.parroquia + ","+ baseEvento.provincia +"\n")
    if i%10000 == 0:
        print('Big Iteration Completed')
edges.close()
nodes.close()

























