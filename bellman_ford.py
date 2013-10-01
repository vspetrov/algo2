#!/usr/bin/pypy

class Vertex:
    idCounter=0
    all = []
    def __init__(self):
        self.id = Vertex.idCounter
        Vertex.idCounter+=1
        Vertex.all.append(self)

class Edge:
    idCounter=0
    all=[]
    def __init__(self,v1,v2):
        self.id=Edges.idCounter
        Edge.idCounter+=1
        self.head = v1
        self.tail = v2
        Edge.all.append(self)



def bellman_ford(fname):
    pass

def main():
    fname = 'data/g1.txt'
    file = open(fname)
    (vertecesNumber, edgesNumber) = [int(x) for x in file.readline().split()]
    print "vertecesNumber=",vertecesNumber,"; edgesNumber=",edgesNumber

    for i in range(vertecesNumber):
        Vertex()

    assert(len(Vertex.all) == vertecesNumber)

if __name__ == '__main__':
    main()
