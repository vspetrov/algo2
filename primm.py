#!/usr/bin/python

class Edge:
    """The class describes an edge of a graph"""
    global_counter = 0
    max_cost=0
    Vertices = []
    def __init__(self, _vertices, _cost):
        self.id = Edge.global_counter
        Edge.global_counter += 1
        self.my_vertices=_vertices
        self.cost=_cost
    def __str__(self):
        return "Edge: {id=%d, vertices=[%d:%d], cost=%d}" % (self.id,self.my_vertices[0],self.my_vertices[1],self.cost)


class Vertex:
    """The class decsribes a vertex of a graph"""
    global_counter = 0
    Edges = []
    def __init__(self):
        self.id = Vertex.global_counter
        Vertex.global_counter += 1
        self.my_edges=[]
        self.Edges = []
        self.in_mst=False
    def add_edge(self,edge):
        self.my_edges.append(edge)
    def __str__(self):
        str="Vertex: {id=%d, edges=[" % (self.id)
        for edge in self.my_edges[:-1]:
            str+="%d," % edge.id
        str+="%d]}" % self.my_edges[-1].id
        return str


def getCheapest(edges):
    min_cost = Edge.max_cost
    counter=0
    pos = 0
    for edge in edges:
        if (Edge.Vertices[edge.my_vertices[0]].in_mst != Edge.Vertices[edge.my_vertices[1]].in_mst):
            if edge.cost < min_cost:
                min_cost = edge.cost
                pos = counter
        counter+=1
    return edges.pop(pos)

def runPrimm(vertices,edges):
    mst_e = []
    Edge.Vertices[0].in_mst=True
    for i in range(len(vertices)-1):
        mst_e.append(getCheapest(edges))
        new_v = mst_e[-1].my_vertices[0] if not Edge.Vertices[mst_e[-1].my_vertices[0]].in_mst else \
        mst_e[-1].my_vertices[1]
        Edge.Vertices[new_v].in_mst=True
    return mst_e

def main():
    edges = []
    vn, en  = [int (x) for x in open('edges2.txt').readline().split()]
    for line in open('edges2.txt').readlines()[1:]:
        l = [int(x) for x in  line.split()]
        l[0] -= 1
        l[1] -= 1
        edges.append(Edge(l[:2],l[2]))

    vertices = []
    for i in range(vn):
        vertices.append(Vertex())

    Edge.max_cost = edges[0].cost
    for edge in edges:
        vertices[edge.my_vertices[0]].add_edge(edge)
        vertices[edge.my_vertices[1]].add_edge(edge)
        if edge.cost > Edge.max_cost:
            Edge.max_cost = edge.cost

    Vertex.Edges = edges[:]
    Edge.Vertices = vertices[:]
    mst = runPrimm(vertices,edges)
    sum = 0
    for edge in mst:
        sum+= edge.cost
    print "MST cost: ", sum
#    for edge in mst:
        # print edge

if __name__ == "__main__":
    main()
