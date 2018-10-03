#group class, stores information about communication flows between recurring clusters of employees
#currently only utilising this class for dyad/tryad counts
class Group:
    def __init__(self, sender, receivers, sorted_members = None):
        self.initial_sender = sender
        self.initial_receivers = receivers
        if not sorted_members:
            val = sorted([sender]+receivers)
        else:
            val = sorted_members
        self.sorted_members = val
        self.adj_list = self.initial_adj_list()

    def initial_adj_list(self):
        adj_list = {}
        for index, key in enumerate(self.sorted_members):
            adj_list[key] = []
            if key == self.initial_sender:
                val = 1
            else:
                val = 0
            for k in self.sorted_members:
                if k != key:
                    adj_list[key].append((k, val))
        return adj_list

    def add_data(self, sender):
        values = self.adj_list[sender]
        for index, val in enumerate(values):
            new_val = (val[0], val[1]+1)
            values[index] = new_val

    def write_to_file(self, output):
        output.write("Emails sent exclusively between the group of" + "".join(self.sorted_members))
        output.write("\n")
        for vertex in self.adj_list:
            vertex = vertex.strip()
            for edge in self.adj_list[vertex]:
                if edge:
                    edge_string = edge[0]
                    edge_string = edge_string.strip()
                    if vertex != edge_string:
                        edge_val = edge[1]
                        output.write(vertex +" sent " + str(edge_val) + " to " + str(edge_string))
                        output.write("\n")
        output.write("\n")

    def number_of_members(self):
        return len(list(self.adj_list))


#container class for group objects
class Groups:
    def __init__(self):
        self.elements = {}
        self.sizes = {}
        self.count = 0

    #provided a list of members
    def add(self, sender, receivers):
        N = len(receivers) + 1
        if N not in self.sizes:
            self.sizes[N] = 1
        else:
            self.sizes[N] += 1
        key = self.dictionary_key(sender, receivers)
        if key not in self.elements:
            new_group = Group(sender, receivers)
            self.count += 1
            self.elements[key] = new_group
        else:
            self.elements[key].add_data(sender)


    def dictionary_key(self, sender, receivers):
        members = sorted([sender] + receivers)
        my_str = " "
        for e in members:
            my_str += str(e) + ", "
        return my_str[:-2]

    def groups_of_size(self, N):
        if self.sizes[N]:
            return self.sizes[N]
        else:
            return 0

    def dyad_count(self):
        return self.groups_of_size(2)

    def triad_count(self):
        return self.groups_of_size(3)

    def write_all_to_file(self, output):
        for el in self.elements:
            group = self.elements[el]
            group.write_to_file(output)

    def write_statistics_to_file(self, output):
        output.write("Dyad count: " + str(self.dyad_count()))
        output.write("\n")
        output.write("Triad count: " + str(self.triad_count()))

