#!/usr/bin/python


class Vertex:
    """ Vertex of a graph """
    idCounter = 0
    storage = []
    def __init__(self):
        self.id = Vertex.idCounter
        Vertex.idCounter += 1
        self.root = self.id
        self.rank = 0
    def findRoot(self):
        if self.root == self.id:
            return self.id
        else:
            root = Vertex.storage[self.root].findRoot()
            self.root = root
            return root
    @staticmethod
    def union(v1,v2):
        if v1.rank < v2.rank:
            v1,v2 = v2,v1
        v2.root = v1.id
        Vertex.idCounter -= 1
        if v1.rank == v2.rank:
            v1.rank += 1

    def __str__(self):
        return "Vertex={id %d, root %d, rank %d}" % (
            self.id, self.root,self.rank)
    def __repr__(self):
        return self.__str__()

class Edge:
    """ Edge of a graph """
    storage = []
    def __init__(self,v1,v2,cost):
        self.v1 = v1
        self.v2 = v2
        self.cost = cost
    def inSingleCluster(self):
        return self.v1.findRoot() == self.v2.findRoot()
    def __str__(self):
        return "Edge={%d:%d:%d}"%(self.v1.id,self.v2.id,self.cost)
    def __repr__(self):
        return self.__str__()



def sanityCheck(K_num):
    roots = {}
    for v in Vertex.storage:
        r = v.findRoot()
        if not r in roots:
            roots[r] = 1

    if not len(roots) == K_num:
        print "Sanity check failed"
    else:
        print "Sanity check passed"

def Clusterize(K_num):
    Edge.storage = sorted(Edge.storage,
                          key = lambda e: e.cost)
    while (Vertex.idCounter > K_num and len(Edge.storage) > 0):
        e = Edge.storage.pop(0)
        if not e.inSingleCluster():
            r1 = Vertex.storage[e.v1.findRoot()]
            r2 = Vertex.storage[e.v2.findRoot()]
            Vertex.union(r1,r2)

    sanityCheck(K_num)
    print "Number of edges left", len(Edge.storage)

def main():
    f = open('clustering1.txt')
    num_of_vertices = int(f.readline())
    for i in range(num_of_vertices):
        v = Vertex()
        Vertex.storage.append(v)

    for line in f.readlines():
        values = [int (x) for x in line.split()]
        e = Edge(Vertex.storage[values[0]-1],
                 Vertex.storage[values[1]-1],
                 values[2])
        Edge.storage.append(e)

    print "Total number of vertices:",len(Vertex.storage)
    print "Total number of edges:",len(Edge.storage)

    Clusterize(4)
    print "Spacing:", Edge.storage.pop(0).cost

if __name__ == '__main__':
    main()
