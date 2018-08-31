import classes.AdjacencyList as AL
from collections import deque

class GraphStatistics:
    def __init__(self):
        self.adj_list = {}


    def add_data(self, sender):
        assert isinstance(sender, AL.Sender)
        sender_key = sender.toString()
        recipients = sender.recipients_as_list()
        if sender not in self.adj_list:
            self.adj_list[sender_key] = recipients

    def print_nodes(self):
        for node in self.adj_list:
            print(node)

    def number_of_nodes(self):
        return len(self.adj_list)

    def number_of_edges(self):
        c = 0
        for sender in self.adj_list:
            receivers = self.adj_list[sender]
            for v in receivers:
                if v[0] in self.adj_list:
                    c += 1
        return c

    def max_edges(self):
        vertices = self.number_of_nodes()
        return (vertices * (vertices-1))

    def get_density(self):
        edges = self.number_of_edges()
        max_number_of_edges = self.max_edges()
        return float(edges / max_number_of_edges)


    def shortest_path_between_two_nodes(self, start, end):
        path_found = False
        visited = {i: False for i in self.adj_list}
        previous = {j: None for j in self.adj_list}
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
                        if node in self.adj_list:
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
            return None
        else:
            path = []
            next_node = end
            while previous[next_node]:
                path.append(next_node)
                next_node = previous[next_node]
            path.append(next_node)
            return path

    def all_shortest_paths(self):
        paths = []
        for i in self.adj_list:
            for j in self.adj_list:
                if i != j:
                    shortest_path = self.shortest_path_between_two_nodes(i, j)
                    if shortest_path:
                        paths.append(shortest_path)
        return paths

    def degree_centrality(self, node):
        c = 0
        neighbours = self.adj_list[node]
        for v in neighbours:
            v = v[0]
            if v in self.adj_list:
                c += 1
        return c


    def betweenness_centrality(self, node = None):
        my_nodes = {i: 0 for i in self.adj_list}
        all_paths = self.all_shortest_paths()
        for path in all_paths:
            for v in path:
                my_nodes[v] += 1
        if node:
            return my_nodes[node]
        else:
            node_list = []
            for node in my_nodes:
                val = (node, my_nodes[node])
                node_list.append(val)
            node_list.sort(key = lambda x: x[1])
            node_list.reverse()
            return node_list

    def closeness_centrality(self, node):
        closeness = 0
        for v in self.adj_list:
            if v != node:
                path = self.shortest_path_between_two_nodes(node, v)
                if path:
                    closeness += len(path)
        return 1 / closeness

    def harmonic_centrality(self, node):
        h_centrality = 0
        for v in self.adj_list:
            if v != node:
                path = self.shortest_path_between_two_nodes(node, v)
                if path:
                    h_centrality += (1 / len(path))
        return h_centrality

    # run and return a calculation of eigenvector centrality on self.adj_list
    ## Input : iterations 
    ## Output: dictionary of { nodeId: e_centrality }
    def eigenvector_centrality(self, iterations = 100):
        vectorSet = {}
        for key, value in self.adj_list.items():
            vectorSet[key] = 1 # init vectorSet of everything = 1

        for i in range(iterations):
            for sender in self.adj_list:
                for r in sender:
                    vectorSet[sender] = vectorSet[sender] + 1

        sum = 0
        for key, value in vectorSet.items():
            sum += value
        
        for key, value in vectorSet.items():
            vectorSet[key] = vectorSet[key] / sum

        return vectorSet

    def graph_as_adj_matrix(self):
        matrix_order = {}
        c = 0
        for sender in self.adj_list:
            matrix_order[sender] = c
            c += 1
        N = len(self.adj_list)
        adj_matrix = [[0 for _ in range(N)] for _ in range(N)]
        for sender in self.adj_list:
            row = matrix_order[sender]
            recipients = self.adj_list[sender]
            for recipient in recipients:
                recipient = recipient[0]
                if recipient in self.adj_list:
                    col = matrix_order[recipient]
                    adj_matrix[row][col] = 1
        return adj_matrix

if __name__ == "__main__":
    pass
    