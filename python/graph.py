import itertools
from collections import defaultdict

class Graph:
    def __init__(self, v, edges=None):
        self.v = v
        if not edges:
            self.edges = set()
        else:
            self.edges = edges

    def add_edge(self, a, b):
        self.edges.add(frozenset({a, b}))

    def degree(self, vertex):
        return sum(vertex in edge for edge in self.edges)

    def degree_count(self):
        degree_count = defaultdict(int)
        for v in range(self.v):
            degree_count[self.degree(v)] += 1
        return rank_count

    def vertices_of_degree(self, degree):
        for v in range(self.v):
            if self.degree(v) == degree:
                yield v

    def isomorphic_to(self, other):
        if self.v != other.v:
            return False        # edge length differs
        if len(self.edges) != len(self.edges):
            return False        # number of edges differ

        dc = self.degree_count()
        odc = other.degree_count()

        if dc != odc:          # different degree counts
            return False

        # try to find isomorphism
        mapping = {}
        remaining = set(range(self.v))
        other_remaining = set(range(self.v))

        # first map everything w/ the same degree right away
        for degree, count in dc.items():
            if count == 1:
                vod = list(self.vertices_of_degree(degree))
                vod_other = list(self.vertices_of_degree(degree))
                assert len(vod) == len(vod_other) == 1
                mapping[vod[0]] = vod_other[0]
                remaining.remove(vod[0])
                other_remaining.remove(vod_other[0])

    def __str__(self):
        return '{} vertices\n{}'.format(self.v, self.edges)


def complete(v):
    g = Graph(v)
    for a in range(v):
        for b in range(a+1, v):
            g.add_edge(a, b)
    return g


def complement(g):
    return Graph(g.v, complete(g.v).edges - g.edges)


def all_graphs(v):
    edges = list(itertools.combinations(range(v), 2))
    for n_edges in range((v * v+1) // 2):
        for elist in itertools.combinations(edges, n_edges):
            g = Graph(v)
            for e in elist:
                if e:
                    g.add_edge(*e)
            yield g
