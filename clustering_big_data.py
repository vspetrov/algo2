#!/usr/bin/python
import cProfile
class Vertex:
    """ Vertex of a graph """
    idCounter = 0
    storage = []
    storage_map = {}
    def __init__(self):
        self.id = Vertex.idCounter
        Vertex.idCounter += 1
        self.root = self.id
        self.rank = 0
        self.key = 0
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
        return "Vertex={id %d, root %d, rank %d, key %d}" % (
            self.id, self.root,self.rank, self.key)
    def __repr__(self):
        return self.__str__()
    def setKey(self,key):
        self.key = 0
        for i in range(24):
            self.key += int(key[-(i+1)])*(2**i)
        if self.key in Vertex.storage_map:
            Vertex.storage_map[self.key].append(self)
        else:
            Vertex.storage_map[self.key] = [self]


no_0_dist=False
no_1_dist=False
no_2_dist=False

def findClosest():
    v1 = None
    v2 = None
    global no_0_dist
    global no_1_dist
    global no_2_dist

    if not no_0_dist:
        for v in Vertex.storage:
            v1 = v
            for vv in Vertex.storage_map[v1.key]:
                if not vv == v:
                    v2 = vv
                    if not v1.findRoot() == v2.findRoot():
                        return v1,v2
    if not no_0_dist:
        no_0_dist = True
        print "No more 0 dist"

    if not no_1_dist:
        for v in Vertex.storage:
            v1 = v
            for i in range(24):
                key = v1.key
                key |= 1<<i
                if key in Vertex.storage_map:
                    for vv in Vertex.storage_map[key]:
                        v2 = vv
                        if not v1.findRoot() == v2.findRoot():
                            return v1,v2
    if not no_1_dist:
        no_1_dist = True
        print "No more 1 dist"

    if not no_2_dist:
       for v in Vertex.storage:
           v1 = v
           for i in range(24):
               key = v1.key | 1<<i
               for j in range(i,24):
                   key |= 1<<j
                   if key in Vertex.storage_map:
                       for vv in Vertex.storage_map[key]:
                           v2 = vv
                           if not v1.findRoot() == v2.findRoot():
                               return v1,v2
    return v1,v2


def Clusterize():
    go_on=True
    counter=0
    while (go_on):
        v1,v2 = findClosest()
        if ((not None == v1) and (not None == v2)):
            r1 = Vertex.storage[v1.findRoot()]
            r2 = Vertex.storage[v2.findRoot()]
            Vertex.union(r1,r2)
            counter+=1
        else:
            go_on = False
        if 100 == counter:
            print "Vertex.idCounter:",Vertex.idCounter
            counter=0



def main():
    f = open('data/clustering_big.txt')
    num_of_vertices = int(f.readline().split()[0])
    for i in range(num_of_vertices):
        v = Vertex()
        Vertex.storage.append(v)

    counter=0
    for line in f.readlines():
        key=''.join(line.split())
        Vertex.storage[counter].setKey(key)
        counter+=1

    print "Number of different keys:", len(Vertex.storage_map)
    Clusterize()

    print "Clusters:",Vertex.idCounter

if __name__ == '__main__':
    main()
