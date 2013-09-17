#!/usr/bin/python
from bitarray import bitarray

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
        self.key = bitarray()
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
    def setKey(self,key):
        self.key = bitarray(key)
        Vertex.storage_map[self.key] = self

def buildVariants(key):
    variants=[]
    for i in range(24):
        k = key[:]
        k[i] = not k[i]
        variants.append(k)

    for i in range(24):
        k = key[:]
        k[i] = not k[i]
        for j in range(i+1,24):
            k2 = k[:]
            k2[j]  = not k2[j]
            variants.append(k2)
    return variants

def findClosest():
    v1 = None
    v2 = None
    distance = 0
    for v in Vertex.storage:
        v1 = v
        key = v.key
        key_variants = buildVariants(key)
        d = 0
        for kv in key_variants[:24]:
            if kv in Vertex.storage_map:
                v2 = kv
                d = 1
                break
        if 0 == d:
            for kv in key_variants[24:]:
                if kv in Vertex.storage_map:
                    v2 = kv
                    d = 2
                    break
        if d > 0:
            distance = d
            break
    return v1,v2,distance


def Clusterize():
    distance = 1
    counter=0
    while (distance > 0):
        v1,v2,distance = findClosest()
        if (v1.findRoot() != v2.findRoot() and distance > 0):
            r1 = Vertex.storage[v1.findRoot()]
            r2 = Vertex.storage[v2.findRoot()]
            Vertex.union(r1,r2)
            counter+=1
        if 100 == counter:
            print "Vertex.idCounter:",Vertex.idCounter,"dist:",distance
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
#    Clusterize()
    key = Vertex.storage[0].key
#    v1,v2,distance = findClosest()
#    print v1,v2,distance
    print key in Vertex.storage_map
    print "Clusters:",Vertex.idCounter

if __name__ == '__main__':
    main()
