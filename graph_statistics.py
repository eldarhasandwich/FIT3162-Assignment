import classes.AdjacencyList as AL
from collections import deque

class GraphStatistics:
    """
    Compute all the relevant graph statistics based on
    nodes and edges stored in object's adjacency list.
    """
    def __init__(self):
        self.adj_list = {}

    def import_adjacency_list(self, adjList):
        """
        Import nodes and edges from a custom adjacency list class.

        @type  adjList: AL
        @param adjList: Custom adjacency list class containing data pulled from DB.
        """
        pass
        for skey, sender in adjList.senders.items():
            self.add_data(sender)

    def add_data(self, sender):
        """
        Add data from a sender object to the adjacency list.

        @type  sender: AL.Sender
        @param sender: Sender of a file, containing the recipients they've sent to.
        """
        assert isinstance(sender, AL.Sender)
        sender_key = sender.toString()
        recipients = sender.recipients_as_list()
        if sender not in self.adj_list:
            self.adj_list[sender_key] = recipients

    def number_of_nodes(self):
        """
        Get the number of nodes in adjacency list.

        @rtype: int
        @return: the quantity of unique nodes
        """
        return len(self.adj_list)


    def number_of_edges(self):
        """
        Get the number of edges in adjacency list.

        @rtype: int
        @return: the quantity of unique edges.
        """
        c = 0
        for sender in self.adj_list:
            receivers = self.adj_list[sender]
            for v in receivers:
                if v[0] in self.adj_list:
                    c += 1
        return c

    def max_edges(self):
        """
        The maximum amount of edges, given the number of vertices.

        @rtype: int
        @return: the amount of possible edges in the graph.
        """
        vertices = self.number_of_nodes()
        return vertices * (vertices-1)

    def get_density(self):
        """
        The density of the graph.

        @rtype: float
        @return: a decimal between 0 and 1.0, representing the graph's density.
        """
        edges = self.number_of_edges()
        max_number_of_edges = self.max_edges()
        return float(edges / max_number_of_edges)

    def shortest_path_between_two_nodes(self, start, end):
        """
        Find the shortest path in a graph between a start and end
        node by implementing Breadth First Search.

        @type  start: str
        @param start: The start of the path.

        @type end: str
        @param end: The end of the path.

        @rtype: list
        @return: The shortest path available between start and end nodes.
        """
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
                else:
                    previous[vertex] = None
                if vertex in self.adj_list:
                    edges = self.adj_list[vertex]
                    for node in edges:
                        node = node[0]
                        if node in self.adj_list:
                            my_queue.append(node)
                            if node == end:
                                path_found = True
                                previous[node] = vertex
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
        """
        Get shortest paths between all nodes in the graph.

        @rtype: list
        @return: A list containing lists of paths between each node.
        """
        paths = []
        for i in self.adj_list:
            for j in self.adj_list:
                if i != j:
                    shortest_path = self.shortest_path_between_two_nodes(i, j)
                    if shortest_path:
                        paths.append((shortest_path, (i, j)))
        return paths

    def degree_centrality(self, node):
        """
        Computes the degree centrality of a given node.

        @type  node: str
        @param node: a vertex in graph

        @rtype: int
        @return: The number of ties a node has.
        """
        c = 0
        neighbours = self.adj_list[node]
        for v in neighbours:
            v = v[0]
            if v in self.adj_list: #i dont think this should be here
                c += 1
        return c


    def betweenness_centrality(self, node = None):
        """
        Computes the betweenness centrality of a given node
        if one is passed, else get for every node in graph.

        @type  node: str
        @param node: a vertex in graph

        @rtype: int
        @return: The number of ties a passed in node has.

        @rtype: list
        @return: A list of nodes in graph sorted by their betweenness centrality values.
        """
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
        """
        Computes the closeness centrality of a given node

        @type  node: str
        @param node: a vertex in graph

        @rtype: float
        @return: closeness centrality of a node
        """
        closeness = 0
        for v in self.adj_list:
            if v != node:
                path = self.shortest_path_between_two_nodes(node, v)
                if path:
                    closeness += len(path)
        return 1 / closeness

    def harmonic_centrality(self, node):
        """
        Computes the harmonic centrality of a given node.

        @type  node: str
        @param node: a vertex in graph

        @rtype: float
        @return: harmonic centrality of a node
        """
        h_centrality = 0
        for v in self.adj_list:
            if v != node:
                path = self.shortest_path_between_two_nodes(node, v)
                if path:
                    h_centrality += (1 / len(path))
        return h_centrality


    def eigenvector_centrality(self, iterations = 100):
        """
        Computes the eigenvector centrality of graph.

        @type  iterations: int
        @param iterations: number of times to loop adjacency list

        @rtype: dict
        @return: dictionary of { nodeId: e_centrality }
        """
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

    def GetAllStatisticalMethods(self):
        return [
            (self.get_density, 'Density'),
            (self.degree_centrality, 'Degree Centrality'),
            (self.betweenness_centrality, 'Betweenness Centrality'),
            (self.closeness_centrality, 'Closeness Centrality'),
            (self.harmonic_centrality, 'Harmonic Centrality'),
            (self.eigenvector_centrality, 'Eigenvector Centrality')
        ]

if __name__ == "__main__":
    adj_list = {"1": ["2", "3"], "2": ["1", "3"], "3": ["1", "2", "4"], "4":["3"]}

    graph_stats = GraphStatistics()
    graph_stats.adj_list = adj_list
    print(graph_stats.shortest_path_between_two_nodes("2", "4"))
    my_paths = graph_stats.all_shortest_paths()
    for path in my_paths:
        i = path[1][0]
        j = path[1][1]
        path = path[0]
        print("Shortest path between {0} and {1} is {2}".format(i, j, path))