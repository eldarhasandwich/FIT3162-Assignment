import classes.AdjacencyList as AL

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
        return edges / max_number_of_edges






