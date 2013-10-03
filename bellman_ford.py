#!/usr/bin/pypy
import numpypy as np
import sys
import copy
import heapq

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
        return "e[%d:%d:%d:%g]"%(self.id,self.head.id,self.tail.id,self.cost)
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
    A = np.ones([n+1,n],'float')*sys.float_info.max
    A[0,source] = 0
    for i in range(1,n+1):
        for v in graph.vertices:
            a1 = A[i-1,v.id]
            a2 = sys.float_info.max
            for e in v.in_edges:
                a3 = A[i-1,e.head.id] + e.cost
                a2 = a3 if a3 < a2 else a2
            A[i,v.id] = min(a1,a2)

    has_neg_cycles = False
    for i in range(n):
        if not A[n-1,i] == A[n,i]:
            has_neg_cycles = True
            break

    return A[n-1] if not has_neg_cycles else []

def reweight(graph,values):
    for e in graph.edges:
        id1 = e.head.id
        id2 = e.tail.id
        e.cost += values[id1]-values[id2]
        assert(e.cost >= 0)

def get_next(sp,visited,n):
    minimal = sys.float_info.max
    ret = -1
    for i in range(n):
        if (sp[i] < minimal) and (not visited[i]):
            ret = i
            minimal = sp[i]
    return ret

def dijkstra(graph,source):
    n = len(graph.vertices)
    sp = np.ones([n],'float')*sys.float_info.max
    sp[source]=0
    visited = np.zeros([n],'bool')
    all_visited=False
    while (not all_visited):
        next_id = get_next(sp,visited,n)
        if next_id >= 0:
            v = graph.vertices[next_id]
            for e in v.out_edges:
                w = e.tail
                sp[w.id] = min(sp[w.id],sp[next_id]+e.cost)
            visited[next_id]=True
        else:
            all_visited = True
    return sp


def johnson(filename):
    print "Starting Johnson algorithm"
    graph = Graph(filename)
    g = Graph(filename)
    v = g.add_vertex()
    assert(len(g.vertices) == len(graph.vertices)+1)

    for i in range(len(graph.vertices)):
        g.add_edge(v,g.vertices[i],0)

    print "Running BellmanFord first"
    short_paths = bellman_ford(g,v.id)
    if 0 == len(short_paths):
        print "Current graph has negative cycles"
        return [],0
    reweight(graph,short_paths[:-1])
    sp = []
    shortest_shortest_path = sys.float_info.max
    step = int(len(graph.vertices)/100.0)+1
    for i in range(len(graph.vertices)):
        shortest_path = dijkstra(graph,i)
        for j in range(len(shortest_path)):
            shortest_path[j] += short_paths[j]-short_paths[i]
            if shortest_path[j] < shortest_shortest_path and not i == j:
                shortest_shortest_path = shortest_path[j]
            if shortest_path[j] > 1e300:
                shortest_path[j] = None
            else:
                shortest_path[j] = int(shortest_path[j])
        sp.append(shortest_path)
        if i/step*step == i:
            print "{0:d} % done..".format(int(float(i)/(len(graph.vertices)/100.0)))

    return sp,shortest_shortest_path

def main():
    sp,ssp = johnson('data/g1.txt')
    # for s in sp:
        # print ["{0:0.2f}".format(i) for i in s]

    print "SSP: ", ssp
    sp,ssp = johnson('data/g2.txt')
    print "SSP: ", ssp

    sp,ssp = johnson('data/g3.txt')
    print "SSP: ", ssp


if __name__ == '__main__':
    main()
