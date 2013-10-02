#!/usr/bin/pypy
import numpypy as np
import sys
import copy

class Vertex:
    def __init__(self,id):
        self.id = id
        self.out_edges=[]
        self.in_edges=[]

class Edge:
    def __init__(self,v1,v2,id,cost=0):
        self.id=id
        self.head = v1
        self.tail = v2
        self.cost = cost
    def __str__(self):
        return "[%d:%d:%d:%g]"%(self.id,self.head.id,self.tail.id,self.cost)
    def __repr__(self):
        return self.__str__()

class Graph:
    def __init__(self,filename):
        self.edges = []
        self.vertices = []

        file = open(filename)
        (vertecesNumber, edgesNumber) = [int(x) for x in file.readline().split()]
        print "vertecesNumber=",vertecesNumber,"; edgesNumber=",edgesNumber
        for i in range(vertecesNumber):
            self.vertices.append(Vertex(i))
        assert(len(self.vertices) == vertecesNumber)
        ecount = 0
        for line in file.readlines():
            (id1,id2,cost) = [int(x) for x in line.split()]
            v1 = self.vertices[id1-1]
            v2 = self.vertices[id2-1]
            e=Edge(v1,v2,ecount,cost)
            v1.out_edges.append(e)
            v2.in_edges.append(e)
            ecount+=1
            self.edges.append(e)
        assert(len(self.edges) == edgesNumber)

    def add_vertex(self):
        id=len(self.vertices)
        v=Vertex(id)
        self.vertices.append(v)
        return v


    def add_edge(self,v1,v2,cost=0):
        id=len(self.edges)
        e = Edge(v1,v2,id,cost)
        v1.out_edges.append(e)
        v2.in_edges.append(e)
        self.edges.append(e)
        return e

def bellman_ford(graph,source):
    n = len(graph.vertices)
    A = np.ones([n,n],'float')*sys.float_info.max
    A[0,source] = 0
    for i in range(1,n):
        for v in graph.vertices:
            a1 = A[i-1,v.id]
            a2 = sys.float_info.max
            for e in v.in_edges:
                a3 = A[i-1,e.head.id] + e.cost
                a2 = a3 if a3 < a2 else a2
            A[i,v.id] = min(a1,a2)
    return A[n-1]

def reweight(graph,values):
    for e in graph.edges:
        id1 = e.head.id
        id2 = e.tail.id
        e.cost += values[id1]-values[id2]
        assert(e.cost >= 0)


def dijkstra(graph,source):
    n = len(graph.vertices)
    sp = np.ones([1,n],'float')*sys.float_info.max
    sp[source.id]=0
    visited = np.zeros([1,n],'bool')
    current = source

def johnson(graph):
    g = copy.deepcopy(graph)
    v = g.add_vertex()
    for i in range(len(graph.vertices)):
        g.add_edge(v,g.vertices[i],0)
    short_paths = bellman_ford(g,v.id)
    reweight(graph,short_paths[:-1])

    for v in graph.vertices:
        v.out_edges = sorted(v.out_edges,key=lambda e: e.cost)

    return 0

def main():
    g = Graph('data/clustering_test.txt')
    answ = johnson(g)

if __name__ == '__main__':
    main()
