import sys

class Edge():
    def __init__(self, start, end, weight):
        self.start = start
        self.end = end
        self.weight = weight
        self.used = False
        self.considered = False

    def graph_line(self, edge_type='->'):
        return r'{start} {edge_type}[edge from {start} to {end},"{weight}"] {end},'.format(
                edge_type=edge_type,
                start=self.start,
                end=self.end,
                weight=self.weight,
        )
    
    def style_line(self):
        if self.used and self.considered:
            the_style = 'just used'
        elif self.used:
            the_style = 'used'
        elif self.considered:
            the_style = 'considered'
        else:
            the_style = 'unused'
        return r"edge from {start} to {end}/.style={the_style},".format(
                start=self.start,
                end=self.end,
                the_style=the_style
        )
    
    def name(self):
        return '({start}, {end})'.format(start=self.start, end=self.end)

    def before(self, other):
        if self.start < other.start:
            return True
        elif self.start == other.start and (self.end < other.end):
            return True
        else:
            return False

class Graph():
    def __init__(self, directed=False):
        self.directed = directed
        self.edges = []
        self.vertices = set()
        self.marked_vertices = set()
        self.set_of = {}

    def add_edge(self, u, v, w):
        self.edges.append(Edge(u, v, w))
        self.vertices.add(u)
        self.vertices.add(v)
        self.set_of[u] = u
        self.set_of[v] = v

    def _find_set(self, v):
        seen = [v]
        u = v
        while self.set_of[u] != u:
            u = self.set_of[u]
            seen.append(u)
        for x in seen:
            self.set_of[x] = u
        return u

    def _union_set(self, u, v):
        old_sets = (self._find_set(u), self._find_set(v))
        new_set = min(old_sets[0], old_sets[1])
        for old_set in old_sets:
            self.set_of[old_set] = new_set

    def generate_graph_lines(self):
        output = ''
        for vertex in sorted(list(self.vertices)):
            output += r'{name}[node named {name}],'.format(name=vertex)
        for edge in self.edges:
            output += edge.graph_line('->' if self.directed else '--')
        return output

    def generate_graph_style(self):
        output = ''
        for vertex in sorted(list(self.vertices)):
            if vertex in self.marked_vertices:
                output += r'node named {name}/.style={{marked vertex}},'.format(name=vertex)
            else:
                output += r'node named {name}/.style={{unmarked vertex}},'.format(name=vertex)
        for edge in self.edges:
            output += edge.style_line()
        return output

    def mst(self, start, which='Prim'):
        def _find_next_prim():
            best_weight = float('inf')
            best_edge = None
            for edge in self.edges:
                edge.considered = False
                if edge.start not in self.marked_vertices:
                    continue
                if edge.end in self.marked_vertices:
                    continue
                edge.considered = True
                if edge.weight < best_weight or (edge.weight == best_weight and edge.before(best_edge)):
                    best_edge = edge
                    best_weight = edge.weight
            return best_edge
        def _find_next_kruskall():
            best_weight = float('inf')
            best_edge = None
            for edge in self.edges:
                edge.considered = False
                if self._find_set(edge.start) == self._find_set(edge.end):
                    continue
                edge.considered = True
                if edge.weight < best_weight or (edge.weight == best_weight and edge.before(best_edge)):
                    best_edge = edge
                    best_weight = edge.weight
            return best_edge
        _find_next = _find_next_prim if which == 'Prim' else _find_next_kruskall
        output = ''
        styles = []
        edge_history = []
        used_edges = []
        styles.append(self.generate_graph_style())
        used_edges.append(edge_history.copy())
        if which == 'Prim':
            self.marked_vertices.add(start)
        styles.append(self.generate_graph_style())
        used_edges.append(edge_history.copy())
        while True:
            current = _find_next()
            if current == None:
                break
            edge_history.append(current)
            if which == 'Prim':
                self.marked_vertices.add(current.end)
            elif which == 'Kruskal':
                self._union_set(current.start, current.end)
            else:
                raise Exception("invalid MST type")
            current.used = True
            styles.append(self.generate_graph_style())
            used_edges.append(edge_history.copy())
            assert(len(edge_history) < len(self.vertices))
        output = ''
        for i, rule in enumerate(styles):
            output += (r'''
\tikzset{
    alt=<%s>{%s}{},
}
''' % (i + 1, rule))
        output += (r'''
\matrix[my graph box] (the graph) {
\begin{scope}[my graph]
\graph[spring layout]{
    %s
};
\end{scope}
\\
};
''' % (self.generate_graph_lines()))
        for i, edge_history in enumerate(used_edges):
            output += (r'''
\begin{visibleenv}<%s>
\node[edge history] {
    %s
};
\end{visibleenv}
''' % (i + 1, ', '.join(map(lambda e: e.name(), edge_history))))
        return output

def example_one(which):
    g = Graph()
    g.add_edge('A', 'B', 2)
    g.add_edge('A', 'C', 4)
    g.add_edge('A', 'D', 1)
    g.add_edge('B', 'D', 3)
    g.add_edge('B', 'E', 10)
    g.add_edge('C', 'D', 2)
    g.add_edge('C', 'F', 5)
    g.add_edge('D', 'E', 7)
    g.add_edge('D', 'F', 8)
    g.add_edge('D', 'G', 4)
    g.add_edge('E', 'G', 6)
    g.add_edge('F', 'G', 1)
    print(g.mst('A', which))

if __name__ == '__main__':
    example_one(sys.argv[1])
    
