#!/usr/bin/pypy

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
        return "Vertex=[id {0:06}, root {1:06}, rank {2:03}, key {3:024b}]".format(
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

cheap_edges=[]
no_0_dist=False
no_1_dist=False
no_2_dist=False
import copy
def findClosest():
    v1 = None
    v2 = None
    global no_0_dist
    global no_1_dist
    global no_2_dist
    global cheap_edges


    storage_map = copy.deepcopy(Vertex.storage_map)
    for v in Vertex.storage:
        v1 = v
        self_pos=0
        cc = 0
        for vv in storage_map[v1.key]:
            if not vv.id == v1.id:
                cheap_edges.append((Vertex.storage[v1.id],
                                    Vertex.storage[vv.id]))
            else:
                self_pos = cc
            cc += 1
        del storage_map[v1.key][self_pos]

    print "No more 0 dist", len(cheap_edges)

    storage_map = copy.deepcopy(Vertex.storage_map)
    for v in Vertex.storage:
        v1 = v
        for i in range(24):
            key = v1.key ^ 1<<i
            if key in storage_map:
                for vv in storage_map[key]:
                    cheap_edges.append((Vertex.storage[v1.id],
                                        Vertex.storage[vv.id]))

        self_pos = 0
        for i in range(len(storage_map[v1.key])):
            if storage_map[v1.key][i].id  == v1.id:
                self_pos = i
                break
        del  storage_map[v1.key][self_pos]

    print "No more 1 dist",len(cheap_edges)

    storage_map = copy.deepcopy(Vertex.storage_map)
    for v in Vertex.storage:
        v1 = v
        for i in range(24):
            key1 = v1.key ^ 1<<i
            for j in range(i+1,24):
                key = key1 ^ 1<<j
                if key in storage_map:
                    for vv in storage_map[key]:
                        cheap_edges.append((Vertex.storage[v1.id],
                                            Vertex.storage[vv.id]))
        self_pos = 0
        for i in range(len(storage_map[v1.key])):
            if storage_map[v1.key][i].id  == v1.id:
                self_pos = i
                break
        del  storage_map[v1.key][self_pos]

    return cheap_edges


def Clusterize(cheapest):
    # step=int(len(cheapest)/100.0)
    counter=0
    while (len(cheapest) > 0):
        (v1,v2) = cheapest.pop(0)
        r1 = Vertex.storage[v1.findRoot()]
        r2 = Vertex.storage[v2.findRoot()]
        if r1.id != r2.id:
            Vertex.union(r1,r2)
        counter+=1
        # if  counter/step*step == counter:
            # print "{0}% done..".format(counter/step)


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

    cheapest = findClosest()
    print len(cheapest)
    # print cheapest[0][0],'\n',cheapest[0][1]
    # print cheapest[20000][0],'\n',cheapest[20000][1]
    # print cheapest[300000][0],'\n',cheapest[300000][1]

    Clusterize(cheapest)
    # for cheap in cheapest:
    #     print cheap[0],'\n',cheap[1],'\n',"Dist: {0:024b}".format(cheap[0].key^cheap[1].key)
    #     print '-----------------------------------------------------------------------'
    print "Clusters:",Vertex.idCounter

if __name__ == '__main__':
    main()
