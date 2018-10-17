class Cluster:
    """
    Object for grouping data for a unique combination
    of nodes and edges.

    @type  source_node: str
    @param source_node: The string representing the source node for
                        a given combination of nodes and directed edges.
    @type sink_nodes: list
    @param sink_nodes: A list containing strings of the sink nodes for
                       a given combination of nodes and directed edges.

    """
    def __init__(self, source_node, sink_nodes):
        self.sorted_nodes = sorted([source_node] + sink_nodes)
        self.adj_list = self.initial_adj_list(source_node)
        self.size = len(self.sorted_nodes)
        self.occurrences = 0


    def initial_adj_list(self, source_node):
        """
        Construct the initial adjacency list for the cluster based
        on the source and sink nodes.

        @type  source_node: str
        @param source_node: The string representing the source node for
                            a given combination of nodes and directed edges.

        @rtype: dict
        @return: A dictionary representing the cluster's adjacency list.
        """
        adj_list = {}
        for index, key in enumerate(self.sorted_nodes):
            adj_list[key] = []
            if key == source_node:
                val = 1
            else:
                val = 0
            for k in self.sorted_nodes:
                if k != key:
                    adj_list[key].append((k, val))
        return adj_list

    def add_data(self, source_node):
        """
        Increment the edge weight for the node
        in adjacency list

        @type  source_node: str
        @param source_node: The string representing the source node for
                            a given combination of nodes and directed edges.
        """
        values = self.adj_list[source_node]
        for index, val in enumerate(values):
            new_val = (val[0], val[1]+1)
            values[index] = new_val
        self.occurrences += 1

    def number_of_members(self):
        """
        @rtype: int
        @return: Number of nodes in the list.
        """
        return len(list(self.adj_list))



class Clusters:
    """
    Container class for cluster objects.
    """
    def __init__(self):
        self.elements = {}
        self.sizes = {}
        self.max_size = 0

    def add(self, source_node, sink_nodes):
        """
        Construct the initial adjacency list for the cluster based
        on the source and sink nodes.

        @type  source_node: str
        @param source_node: The string representing the source node for
                            a given combination of nodes and directed edges.
        @type sink_nodes: list
        @param sink_nodes: A list containing strings of the sink nodes for
                           a given combination of nodes and directed edges.
        """
        size = len(sink_nodes) + 1
        if size not in self.sizes:
            self.max_size = max(size, self.max_size)
            self.sizes[size] = []
        key = self.dictionary_key(source_node, sink_nodes)
        if key not in self.elements:
            new_group = Cluster(source_node, sink_nodes)
            self.elements[key] = new_group
            self.sizes[size].append(new_group)
        else:
            self.elements[key].add_data(source_node)

    def dictionary_key(self, source_node, sink_nodes):
        """
        Generate a dictionary key to check if the cluster
        already exists.

        @type  source_node: str
        @param source_node: The string representing the source node for
                            a given combination of nodes and directed edges.
        @type sink_nodes: list
        @param sink_nodes: A list containing strings of the sink nodes for
                           a given combination of nodes and directed edges.
        @rtype: str
        @return: A string where each substring is an ordered node in the cluster.
        """
        members = sorted([source_node] + sink_nodes)
        my_str = " "
        for e in members:
            my_str += str(e) + ", "
        return my_str[:-2]

    def elements_of_size(self, size):
        """
        Returns a list of groups that match the passed in size.

        @type  size: int
        @param size: Desired group size.
        @rtype: list
        @return: A list containing all groups that match the passed in size.
        """
        if size in self.sizes:
            return self.sizes[size]
        else:
            return []

    def dyad_count(self):
        """
        Returns the number of dyads, which are clusters of size 2.

        @rtype: int
        @return: The number of dyads stored in container.
        """
        return len(self.elements_of_size(2))

    def triad_count(self):
        """
        Returns the number of triads, which are clusters of size 3.

        @rtype: int
        @return: The number of triads stored in container.
        """
        return len(self.elements_of_size(3))

    def largest_clusters(self):
        """
        Returns the largest clusters in container.

        @rtype: list
        @return: A list of cluster objects equal to maximum size in container.
        """
        elements = []
        for i in self.elements_of_size(self.max_size):
            elements.append(i)
        return elements

    def number_of_duplicates(self):
        c = 0
        for key in self.elements:
            val = self.elements[key]
            c += val.occurrences
        return c


    def write_statistics_to_file(self, output):
        """
        Write the dyad and triad counts to file.

        @type  output: file
        @param output: An open text file which will be added to
                       the database.
        """
        output.write("Dyad count: " + str(self.dyad_count()))
        output.write("\n")
        output.write("Triad count: " + str(self.triad_count()))


