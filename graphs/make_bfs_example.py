import math

def _format_number(x):
    if x == float('inf'):
        return '$\infty$'
    else:
        return x

class Node():
    def __init__(self, label):
        self.label = label
        self.visited = False
        self.visiting = False
        self.updating = False
        self.distance = float('inf')
        self.previous = None
        self.distance_changed = False
        self.path = None
        self.edges = []

    def table_line(self):
        visited_style = "visited" if self.visited else "unvisited"
        if self.updating:
            visited_style = "updating"
        elif self.distance_changed:
            visited_style = "changed"
        return (
            (r"|[my label {visited}]| {label} \& |[my distance {visited}]| {distance}" + 
             r"\& |[my previous {visited}]| {previous} "
             r"\& |[my path {visited}]| {path}").format(
                visited=visited_style,
                label=self.label,
                distance=_format_number(self.distance),
                changed="changed" if self.distance_changed else "unchanged",
                previous="---" if self.previous == None else self.previous,
                path=r'$\rightarrow$'.join(self.path) if self.path != None else '---',
            )
        )

    def graph_rules(self):
        if self.updating:
            return (
                r"graph at {}/.style={{hilite}},edges from {}/.style={{hilite}},".format(self.label, self.label)
            )
        elif self.visited:
            return (
                r"graph at {}/.style={{hidden}},".format(self.label)
            )
        else:
            return ""

    def graph_rules_init(self):
        return (
            r"graph at {}/.style={{}},edges from {}/.style={{}},".format(self.label, self.label)
        )

    def graph_line(self, edge_type='->'):
        output = ""
        for out_vertex, out_weight in self.edges:
            output += '{label}[graph at {label}] {edge_type}[edges from {label},"{out_weight}"] {out_vertex},\n'.format(
                label=self.label,
                out_vertex=out_vertex,
                out_weight=out_weight,
                edge_type=edge_type,
            )
        return output


class Graph():
    nodes = {}

    def add_node(self, k, v):
        self.nodes[k] = Node(k)
        self.nodes[k].edges = v

    def reflect_edges(self):
        for k in self.nodes.keys():
            for e in self.nodes[k].edges:
                target = e[0]
                new_edge = (k, e[1])
                if new_edge not in self.nodes[target].edges:
                    self.nodes[target].edges.append(new_edge)


    def generate_table(self):
        output = []
        for key in sorted(self.nodes.keys()):
            output.append(self.nodes[key].table_line())
        return (r'\\' + '\n').join(output) + r'\\'

    def generate_graph_rules(self):
        output = []
        for key in sorted(self.nodes.keys()):
            output.append(self.nodes[key].graph_rules())
        return ''.join(output)

    def best_first_search(self, start, edge_type='->'):
        tables = []
        rules = []
        self.nodes[start].distance = 0
        self.nodes[start].path = [start]
        def _find_next():
            best_distance = float('inf')
            best_node = None
            for node_key in sorted(self.nodes.keys()):
                node = self.nodes[node_key]
                if node.visited:
                    continue
                if node.distance < best_distance:
                    best_node = node
                    best_distance = node.distance
            return best_node
        tables.append(self.generate_table())
        rules.append(self.generate_graph_rules())
        while True:
            current = _find_next()
            if current == None:
                break
            current.updating = True
            for out_key, weight in current.edges:
                out = self.nodes[out_key]
                new_distance = current.distance + weight
                if new_distance < out.distance:
                    out.distance = new_distance
                    out.previous = current.label
                    out.path = current.path + [out.label]
                    out.distance_changed = True
            tables.append(self.generate_table())
            rules.append(self.generate_graph_rules())
            for node in self.nodes.values():
                node.distance_changed = False
            current.updating = False
            current.visited = True
        graph_rules_init = list(map(lambda k: self.nodes[k].graph_rules_init(), sorted(self.nodes.keys())))
        output = r'''
\tikzset{%s}
''' % ('\n'.join(graph_rules_init))
        for i, rule in enumerate(rules):
            output += (r'''
\tikzset{
    alt=<%s>{%s}{},
}
''' % (i + 1 , rule))
        graph_lines = list(map(lambda k: self.nodes[k].graph_line(), sorted(self.nodes.keys())))
        output += r'''
\matrix[my graph box] (the graph) {
\begin{scope}[my graph]
\graph[spring layout]{
    %s
};
\end{scope}
\\
};
''' % ('\n'.join(graph_lines))
        for i, table in enumerate(tables):
            output += (r'''
\begin{onlyenv}<%s>
\matrix[
    my algorithm table,
    ] (the table) {
~ \& dist \& prev \& path \\
%s
};
\end{onlyenv}
            ''' % (i + 1, table))
        return output

def example_one():
    g = Graph()
    g.add_node('A', [('C', 2), ('D', 1)])
    g.add_node('B', [('A', 2)])
    g.add_node('C', [('D', 1), ('F', 2)])
    g.add_node('D', [('B', 5), ('E', 1), ('F', 6), ('G', 5)])
    g.add_node('E', [('B', 1)])
    g.add_node('F', [('G', 10)])
    g.add_node('G', [('E', 3)])
    print(g.best_first_search('A'))

def example_two():
    g = Graph()
    g.add_node('A', [('B', 7), ('C', 9), ('G', 14)])
    g.add_node('B', [('C', 10), ('D', 15)])
    g.add_node('C', [('D', 11), ('G', 2)])
    g.add_node('D', [('E', 6)])
    g.add_node('E', [('G', 9)])
    g.add_node('G', [])

    g.reflect_edges()
    print(g.best_first_search('A', '--'))

if __name__ == '__main__':
    example_two()
