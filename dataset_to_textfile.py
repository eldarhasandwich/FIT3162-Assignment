import math, io, os, re, string, time
from enron_reader import EnronFileReader
from clusters import Clusters

class EnronParser:
    def __init__(self, a_directory):
        """
        Parse all the files in a given (valid)
        Enron directory.

        @type  a_directory: str
        @param a_directory: The location of an (existing) Enron file directory.
        """
        self.directory = a_directory
        self.enron_file_reader = EnronFileReader()
        self.edge_container = EdgeContainer()
        self.file_count = 0
        self.file_limit = math.inf
        self.message_ids = {}

    def process_directory(self):
        """
        Iterate each file in a valid Enron directory
        and pass to process_file.
        """
        end_iteration = False
        for dir_name, subdir, file_list in os.walk(self.directory): #iterate through every file in directory
            if end_iteration:
                break
            for file in file_list:
                if self.file_count < self.file_limit:
                    self.file_count += 1
                    file_location = str(dir_name + "\\" + file)
                    self.process_file(file_location)
                else:
                    end_iteration = True
                    break

    def process_file(self, file):
        """
        Pass file to enron_file_reader to get the source
        and sink nodes.

        If these nodes are found, add the
        edge to the edge container.

        @type  file: str
        @param file: The location of an Enron file.
        """
        file_reader = self.enron_file_reader
        attributes = file_reader.find_attributes(file)
        if len(attributes) == 3:
            message_id = attributes[0]
            if message_id not in self.message_ids: #check message_id to safeguard duplicate emails
                self.message_ids[message_id] = True
                source_node = attributes[1]
                sink_nodes = attributes[2]
                self.edge_container.add_edge(source_node, sink_nodes)
            else:
                self.message_ids[message_id] = True

class WikiVoteParser:
    """
    Parse all the lines in a given (valid)
    Wiki-Vote text file.

    @type  file: str
    @param file: The location of an (existing) Wiki-Vote text file.
    """
    def __init__(self, file):
        self.file = file
        self.edge_container = EdgeContainer()

    def process_wiki_vote_file(self):
        """
        Iterate over each line in a wiki-vote text file passed
        to the constructor.

        Get the source and sink nodes of each line and add
        to the edge container.
        """
        with open(self.file, 'r') as f:
            for i, line in enumerate(f):
                if i >= 4:
                    i = line.find('\t')
                    j = i + 1
                    k = line.find('\n')
                    source_node = line[:i]
                    sink_node = [line[j:k]]
                    self.edge_container.add_edge(source_node, sink_node)


class WikiRFAParser:
    """
    Parse all the lines in a given (valid)
    Wiki-RfA text file.

    @type  file: str
    @param file: The location of an (existing) Wiki-RfA text file.
    """
    def __init__(self, file):
        self.file = file
        self.edge_container = EdgeContainer()

    def process_wiki_rfa_file(self):
        """
        Iterate over each line in a wiki-RfA text file passed
        to the constructor.

        Get the source and sink nodes of each line and add
        to the edge container.
        """
        source_node_index = 0
        sink_node_index = 1
        i = 0
        nodes = []
        f = open(self.file, encoding = "utf8")
        for line in f:
            j = i+1
            line = line.rstrip()
            if i == source_node_index:
                if line.startswith("SRC:"):
                    source_node = line[4:]
                    nodes.append(source_node)
                    source_node_index += 8

            if j == sink_node_index:
                if line.startswith("TGT:"):
                    sink_node = line[4:]
                    nodes.append(sink_node)
                    sink_node_index += 8

            if len(nodes) == 2:
                source_node = nodes[0]
                sink_node = [nodes[1]]
                self.edge_container.add_edge(source_node, sink_node)
                nodes = []
            i += 1


class Edge:
    """
    Object to store the source and sink nodes of a given directed
    edge.

    @type  source_node: str
    @param source_node: A string representing the source node of a directed edge.
    @type sink_nodes: list
    @param sink_nodes: A list containing strings of each sink node.
    """
    def __init__(self, source_node, sink_nodes):
        self.source_node = source_node
        self.sink_nodes = sink_nodes


    def output_string(self):
        """
        Generate a string containing the source and sink node(s)
        of the file. This string will be written into a text file.

        @rtype:   str
        @return:  A string in the form of
                  {source_node} to {sink_node_one}, {sink_node_two}...
        """
        a_str = "{0} to ".format(self.source_node)
        for r in range(0, len(self.sink_nodes) - 1):
            a_sink_node = self.sink_nodes[r]
            a_str += a_sink_node+", "
        a_str += self.sink_nodes[-1]
        return a_str


class EdgeContainer:
    """
    Container class for Edge objects.
    """
    def __init__(self):
        self.elements = []
        self.clusters = Clusters()

    def add_edge(self, source_node, sink_nodes):
        """
        Create and store a new Edge object for the given source
        and sink nodes.

        @type  source_node: str
        @param source_node: A string representing the source node of a directed edge.
        @type sink_nodes: list
        @param sink_nodes: A list containing strings of each sink node.
        """
        self.clusters.add(source_node, sink_nodes)
        edge = Edge(source_node, sink_nodes)
        self.elements.append(edge)

    def write_to_file(self, output):
        """
        Write the output string of each file to
        the given text file.

        @type  output: file
        @param output: An open text file to write file strings to.
        """
        for edge in self.elements:
            edge_string = edge.output_string()
            output.write(edge_string)
            output.write("\n")
        self.clusters.write_statistics_to_file(output)


def main():
    """
    Generate the text_file based on the chosen data set.
    Path to data set must exist locally and be stored
    in the relevant variable prior to calling the function.
    """
    parser = None
    enron_path = "C:\\Users\\Valued Customer\\Desktop\\maildir"
    wiki_vote_path = "wiki-vote.txt"
    wiki_rfa_path = "C:\\Users\\Valued Customer\\Desktop\\wiki-RfA.txt"
    user_input = str(input('Select data set by typing the number matching desired data set: \n' 
                           '1. Enron \n' 
                           '2. Wiki-Vote \n' 
                           '3. Wiki-RfA \n'))
    if user_input == '1':
        location = enron_path
        if os.path.exists(location):
            parser = EnronParser(enron_path)
            parser.process_directory()
    elif user_input == '2':
        location = wiki_vote_path
        if os.path.exists(location):
            parser = WikiVoteParser(wiki_vote_path)
            parser.process_wiki_vote_file()
    elif user_input == '3':
        location = wiki_rfa_path
        if os.path.exists(location):
            parser = WikiRFAParser(wiki_rfa_path)
            parser.process_wiki_rfa_file()
    else:
        print("Invalid input. Please select a number from 1-3.")
        return
    edges = parser.edge_container
    graph_input = "C:\\Users\\Valued Customer\\Desktop\\enron_output.txt" ######
    with io.open(graph_input, "w", encoding="utf-8") as f:
        edges.write_to_file(f)


if __name__ == "__main__":
    main()






