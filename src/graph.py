import networkx as nx

class Graph:
    nx_graph = None
    pos = None
    nodes = []
    edges = []
    properties = {}

    def __init__(self, nx_graph):
        self.nx_graph = nx_graph
        self.pos = nx.spring_layout(nx_graph)
        for node in nx_graph.nodes():
            self.nodes.append(Node(node, self.pos[node][0], self.pos[node][1]))
        for edge in nx_graph.edges():
            self.edges.append(Edge(self.get_node(edge[0]), self.get_node(edge[1])))

    def get_node(self, name):
        for node in self.nodes:
            if node.name == name:
                return node
        return None
    
    def get_edge(self, node1, node2):
        for edge in self.edges:
            if (edge.node1 == node1 and edge.node2 == node2) or (edge.node1 == node2 and edge.node2 == node1):
                return edge
        return None
    
    def spring_layout(self):
        self.pos = nx.spring_layout(self.nx_graph)
        for node in self.nodes:
            node.x = self.pos[node.name][0]
            node.y = self.pos[node.name][1]

    def draw(self, window):
        for edge in self.edges:
            edge.draw(window)
        for node in self.nodes:
            node.draw(window)


class Node:
    name = ""
    x = 0
    y = 0

    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y

    def draw(self, window, radius=20):
        canvas_x, canvas_y = window.unitcircle_to_canvas_coords(self.x, self.y)
        window.canvas.create_oval(canvas_x-radius, canvas_y-radius, canvas_x+radius, canvas_y+radius, fill="white")



class Edge:
    node1 = None
    node2 = None
    weight = None

    def __init__(self, node1, node2, weight=0):
        self.node1 = node1
        self.node2 = node2
        self.weight = weight

    def draw(self, window):
        canvas_x1, canvas_y1 = window.unitcircle_to_canvas_coords(self.node1.x, self.node1.y)
        canvas_x2, canvas_y2 = window.unitcircle_to_canvas_coords(self.node2.x, self.node2.y)
        window.canvas.create_line(canvas_x1, canvas_y1, canvas_x2, canvas_y2)