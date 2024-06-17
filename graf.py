

class Graph:

    def __init__(self) -> None:
        self.graph_dict = {}

    def add_edge(self, edge):
        start = edge[0]
        end = edge[1]
        if start in self.graph_dict:
            self.graph_dict[start].append(end)
        else:
            self.graph_dict[start] = [end]

    def at(self, vertex):   
        if vertex in self.graph_dict.keys():
            return self.graph_dict[vertex]
        return []

