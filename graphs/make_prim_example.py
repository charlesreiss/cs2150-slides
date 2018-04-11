
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

class Graph():
    def __init__(self, directed=False):
        self.directed = directed
        self.edges = []
        self.vertices = set()
        self.marked_vertices = set()

    def add_edge(self, u, v, w):
        self.edges.append(Edge(u, v, w))
        self.vertices.add(u)
        self.vertices.add(v)

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

    def prims(self, start):
        def _find_next():
            best_weight = float('inf')
            best_edge = None
            for edge in self.edges:
                edge.considered = False
                if edge.start not in self.marked_vertices:
                    continue
                if edge.end in self.marked_vertices:
                    continue
                edge.considered = True
                if edge.weight < best_weight:
                    best_edge = edge
                    best_weight = edge.weight
            return best_edge
        output = ''
        styles = []
        edge_history = []
        used_edges = []
        styles.append(self.generate_graph_style())
        used_edges.append(edge_history.copy())
        self.marked_vertices.add(start)
        styles.append(self.generate_graph_style())
        used_edges.append(edge_history.copy())
        while True:
            current = _find_next()
            if current == None:
                break
            edge_history.append(current)
            self.marked_vertices.add(current.end)
            current.used = True
            styles.append(self.generate_graph_style())
            used_edges.append(edge_history.copy())
        output = ''
        for i, rule in enumerate(styles):
            output += (r'''
\tikzset{
    alt=<%s>{%s}{},
}
''' % (i, rule))
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
''' % (i, ', '.join(map(lambda e: e.name(), edge_history))))
        return output

def example_one():
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
    print(g.prims('A'))

if __name__ == '__main__':
    example_one()
    
