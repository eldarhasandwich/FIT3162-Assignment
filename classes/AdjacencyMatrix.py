
class AdjacencyMatrix:
    def __init__(self):
        self.keys = {}
        self.vals = {}
        self.c = 0
        self.elements = [[0 for _ in range(10000)] for _ in range(10000)]
        self.nodes = []
        self.output_file = "test.txt"


    def add(self, sender, receiver):
        if sender not in self.keys:
            self.keys[sender] = self.c
            self.vals[self.c] = sender
            self.c += 1

        if receiver not in self.keys:
            self.keys[receiver] = self.c
            self.vals[self.c] = receiver
            self.c += 1

        row = self.keys[sender]
        col = self.keys[receiver]
        try:
            self.elements[row][col] += 1
        except IndexError:
            print(row, col)

    def write_data_to_textfile(self):
        output = open(self.output_file, 'w')
        N = self.c
        for i in range(N):
            edges = []
            has_sent = False
            sender = self.vals[i]
            for j in range(N):
                if i != j:
                    recipient = self.vals[j]
                    val = self.elements[i][j]
                    if val > 0:
                        edges.append((recipient, val))
                        has_sent = True
                        output.write(str(val) + ": " + recipient)
                        output.write("\n")
            if has_sent:
                output.write("WERE SENT FROM: " + sender)
                output.write("\n")
                output.write("\n")
                sender_node = Node(sender, edges)
                self.nodes.append(sender_node)


class Node:
    def __init__(self, email, edges):
        self.email = email
        self.edges = edges

    def toString(self):
        return str(self.email)

    def edges_as_string(self):
        all_edges = ""
        for edge in self.edges:
            print(edge)
            edge_str = str(edge)[0]+": "+str(edge[1]+", ")
            all_edges += edge_str
        return all_edges
