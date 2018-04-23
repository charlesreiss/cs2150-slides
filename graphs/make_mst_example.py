import sys
import random

class Edge():
    def __init__(self, start, end, weight, extra=''):
        self.start = start
        self.end = end
        self.weight = weight
        self.used = False
        self.considered = False
        self.extra = extra

    def graph_line(self, edge_type='->', show_weight=False):
        return r'{start} {edge_type}[edge from {start} to {end},"{weight}",{extra}] {end},'.format(
                edge_type=edge_type,
                start=self.start,
                end=self.end,
                weight=self.weight if show_weight else "",
                extra=self.extra,
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
        self.vertex_extra = {}
        self.graph_layout = 'spring layout'
        self.show_weight = True

    def set_vertex(self, v, extra):
        self.vertex_extra[v] = extra

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
            output += r'{name}[node named {name},{extra}],'.format(
                        name=vertex,
                        extra=self.vertex_extra.get(vertex, '')
            )
        for edge in self.edges:
            output += edge.graph_line('->' if self.directed else '--', show_weight=self.show_weight)
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

    def mst(self, start, which='Prim', end_only=False, omit_edge_list=False):
        def _find_next_prim():
            best_weight = float('inf')
            best_edge = None
            for edge in self.edges:
                edge.considered = False
                if not ((edge.start in self.marked_vertices and edge.end not in self.marked_vertices) or
                        (edge.end in self.marked_vertices and edge.start not in self.marked_vertices)):
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
                self.marked_vertices.add(current.start)
                self.marked_vertices.add(current.end)
            elif which == 'Kruskal':
                self._union_set(current.start, current.end)
            else:
                raise Exception("invalid MST type")
            current.used = True
            styles.append(self.generate_graph_style())
            used_edges.append(edge_history.copy())
            #print("selected ", current.start, ":", current.end)
            #print("got ", current.end in self.marked_vertices, current.start in self.marked_vertices)
            #print(list(map(lambda e: e.name(), edge_history)))
            #print(list(self.marked_vertices))
            assert(len(edge_history) < len(self.vertices))
        used_edges.append(edge_history.copy())
        styles.append(self.generate_graph_style())
        output = ''
        if end_only:
            styles = [styles[-1]]
            used_edges = []
        for i, rule in enumerate(styles):
            output += (r'''
\tikzset{
    alt=<%s>{%s}{},
}
''' % (i + 1, rule))
        output += (r'''
\matrix[my graph box] (the graph) {
\begin{scope}[my graph]
\graph[%s]{
    %s
};
\end{scope}
\\
};
''' % (self.graph_layout, self.generate_graph_lines()))
        if not omit_edge_list:
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

def distance(a, b):
    import math
    dx = a[0] - b[0]
    dy = a[1] - b[1]
    return math.sqrt(dx*dx + dy*dy)

def example_geography(which, end_only=True):
    random.seed(42)
    g = Graph()
    coords = {}
    vertices = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P','Q']
    for x in vertices:
        while True:
            coords[x] = (random.uniform(0, 12), random.uniform(0, 6))
            too_close = False
            for y in vertices:
                if x != y and y in coords:
                    if distance(coords[x], coords[y]) < 0.75:
                        too_close = True
            if not too_close:
                break
        g.set_vertex(x, 'at={{({x:.2f},{y:.2f})}}'.format(x=coords[x][0], y=coords[x][1]))
    for x in vertices:
        by_distance = sorted(vertices, key=lambda y: distance(coords[x], coords[y]))
        for y in by_distance[1:8]:
            if x < y:
                g.add_edge(x, y, distance(coords[x], coords[y]))
    g.graph_layout = 'no layout'
    g.show_weight = False
    print(g.mst('A', which, end_only=end_only, omit_edge_list=True))

def example_geography_small(which, end_only=True):
    random.seed(43)
    g = Graph()
    coords = {}
    vertices = ['A', 'B', 'C', 'D', 'E', 'F', 'G',]
    for x in vertices:
        while True:
            coords[x] = (random.uniform(0, 12), random.uniform(0, 6))
            too_close = False
            for y in vertices:
                if x != y and y in coords:
                    if distance(coords[x], coords[y]) < 0.75:
                        too_close = True
            if not too_close:
                break
        g.set_vertex(x, 'at={{({x:.2f},{y:.2f})}}'.format(x=coords[x][0], y=coords[x][1]))
    for x in vertices:
        by_distance = sorted(vertices, key=lambda y: distance(coords[x], coords[y]))
        for y in by_distance[1:8]:
            if x < y:
                g.add_edge(x, y, distance(coords[x], coords[y]))
    g.graph_layout = 'no layout'
    g.show_weight = False
    print(g.mst('A', which, end_only=end_only, omit_edge_list=True))

if __name__ == '__main__':
    which_example = sys.argv[1]
    if which_example == 'one':
        example_one(sys.argv[2])
    elif which_example == 'geography':
        example_geography(sys.argv[2], end_only=True)
    elif which_example == 'geography-small':
        example_geography_small(sys.argv[2], end_only=True)
    elif which_example == 'geography-full':
        example_geography(sys.argv[2], end_only=False)
    else:
        print("unknown example", which_example)
    
