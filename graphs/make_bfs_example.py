import math

def _format_number(x):
    if x == math.inf:
        return '$\infty$'
    else:
        return x

class Node():

    def __init__(self, label):
        self.label = label
        self.visited = False
        self.visiting = False
        self.updating = False
        self.distance = math.inf
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
                r"edges from {}/.append style={{hilite}},".format(self.label)
            )
        elif self.visited:
            return (
                r"graph at {}/.append style={{hidden}},".format(self.label)
            )
        else:
            return ""


class Graph():
    nodes = {}

    def add_node(self, k, v):
        self.nodes[k] = Node(k)
        self.nodes[k].edges = v

    def generate_table(self):
        output = []
        for key in sorted(self.nodes.keys()):
            output.append(self.nodes[key].table_line())
        return (r'\\' + '\n').join(output) + r'\\'

    def generate_graph_rules(self):
        output = []
        for key in sorted(self.nodes.keys()):
            output.append(self.nodes[key].graph_rules())
        return r'\tikzset{' + ('\n'.join(output)) + '}\n'

    def best_first_search(self, start):
        tables = []
        rules = []
        self.nodes[start].distance = 0
        self.nodes[start].path = [start]
        def _find_next():
            best_distance = math.inf
            best_node = None
            for node_key in sorted(self.nodes.keys()):
                node = self.nodes[node_key]
                if node.visited:
                    continue
                if node.distance < best_distance:
                    best_node = node
                    best_distance = node.distance
            return best_node
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
        output = r'''

'''
        for i, table in enumerate(tables):
            output += (r'''
\begin{visibleenv}<%s>
\matrix[
    my algorithm table,
    ] (the table) {
~ \& dist \& prev \& path \\
%s
};
\end{visibleenv}
            ''' % (i + 1, table))
        return output

if __name__ == '__main__':
    g = Graph()
    g.add_node('A', [('C', 2), ('D', 1)])
    g.add_node('B', [('A', 2)])
    g.add_node('C', [('D', 1), ('F', 2)])
    g.add_node('D', [('B', 5), ('E', 1), ('F', 6), ('G', 5)])
    g.add_node('E', [('B', 1)])
    g.add_node('F', [('G', 10)])
    g.add_node('G', [('E', 3)])
    print(g.best_first_search('A'))
