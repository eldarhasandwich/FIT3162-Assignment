import classes.AdjacencyList as AL
from collections import deque

class GraphStatistics:
    def __init__(self):
        self.adj_list = {}
        self.nodes = {}


    def add_data(self, sender):
        assert isinstance(sender, AL.Sender)
        sender_key = sender.toString()
        recipients = sender.recipients_as_list()
        self.adj_list[sender_key] = recipients
        if sender_key not in self.nodes:
            self.nodes[sender_key] = True

        for recipient in recipients:
            recipient_str = recipient[0]
            if recipient_str not in self.nodes:
                self.nodes[recipient_str] = True

    def print_nodes(self):
        for node in self.nodes:
            print(node)

    def number_of_nodes(self):
        return len(self.nodes)

    def number_of_edges(self):
        c = 0
        for sender in self.adj_list:
            c += len(self.adj_list[sender])
        return c

    def max_edges(self):
        vertices = self.number_of_nodes()
        return (vertices * (vertices-1))

    def get_density(self):
        edges = self.number_of_edges()
        max_number_of_edges = self.max_edges()
        return float(edges / max_number_of_edges)

    #No need to use Dijkstra's here because graph is unweighted, instead use BFS
    def shortest_path_between_two_nodes(self, start, end):
        path_found = False
        visited = {i: False for i in self.nodes}
        previous = {j: None for j in self.nodes}
        prev_node = None
        my_queue = deque()
        my_queue.append(start)

        while my_queue:
            vertex = my_queue.pop()
            if visited[vertex] is False:
                visited[vertex] = True
                if prev_node:
                    previous[vertex] = prev_node
                if vertex in self.adj_list:
                    edges = self.adj_list[vertex]
                    for node in edges:
                        node = node[0]
                        my_queue.append(node)
                        if node == end:
                            path_found = True
                            if not prev_node:
                                prev_node = vertex
                            previous[node] = prev_node
                            break

                prev_node = vertex
                if path_found:
                    break


        if not path_found:
            return "No path"
        else:
            c = 0
            next_node = end
            while previous[next_node]:
                c += 1
                next_node = previous[next_node]
        return c
