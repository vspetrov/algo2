#!/usr/bin/pypy

import numpypy as np

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
    def __init__(self,filename,just_edges=True):
        self.edges = []
        self.vertices = []

        file = open(filename)
        lines = file.readlines()
        vertecesNumber=0
        edgesNumber=0
        if not just_edges:
            (vertecesNumber, edgesNumber) = [int(x) for x in file.readline().split()]
        else:
            edgesNumber=len(lines)
            for line in lines:
                (u,v) = [int(x)-1 for x in line.split()]
                if max(u,v)+1 > vertecesNumber:
                    vertecesNumber = max(u,v)+1

        print "vertecesNumber=",vertecesNumber,"; edgesNumber=",edgesNumber
        for i in range(vertecesNumber):
            self.vertices.append(Vertex(i))
        assert(len(self.vertices) == vertecesNumber)
        ecount = 0
        for line in lines:

            (id1,id2) = [int(x) for x in line.split()]
            v1 = self.vertices[id1-1]
            v2 = self.vertices[id2-1]
            e=Edge(v1,v2,ecount)
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


def DFS(edges,visited,i,ft,counter):
    visited[i]=True

def get_finishing_times(edges, num_of_nodes):
    visited = np.zeros(num_of_nodes,bool)
    ft = np.zeros(num_of_nodes,int)
    counter=0
    for i in range(num_of_nodes):
        DFS(edges,visited,i,ft,counter)

def main():
    filename = 'data/scc_test.txt'
    G = Graph(filename)

if __name__ == '__main__':
    main()
