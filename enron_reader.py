import re, string

class EnronFileReader:
    """
    Contains the logic for extracting nodes from an Enron text file.
    """
    def __init__(self):
        self.attributes = ["", "", []]
        self.invalid_strings = {"enron": True, "mail": True, "all": True, "outlook": True}

    def find_and_store_file_attributes(self, file_location):
        """
        Iterate through each line in an Enron file to find the message id,
        source node and sink nodes.

        @type  file_location: str
        @param file_location: The location of a given Enron text file.
        """
        elements = []
        with open(file_location, "r") as f:
            for i, line in enumerate(f):
                line = line.strip()
                a_string = line.replace('\t', "")
                if i == 0:
                    self.attributes[0] = a_string
                elif i == 2:
                    self.attributes[1] = self.find_source_node(a_string)
                elif i >= 3:
                    line_valid = True
                    if i == 3:
                        if not a_string.startswith('To:'):
                            line_valid = False
                        else:
                            a_string = a_string[4:]
                    if line_valid:
                        elements.append(a_string)
                    if not a_string.endswith(','):
                        self.attributes[2] = self.get_valid_sink_nodes(elements)
                        return


    def edge_is_valid(self):
        """
        Iterate through attribute variable of object to
        ensure all attributes have length > 0
        """
        for attr in self.attributes:
            if len(attr) == 0:
                return False
        return True


    def get_valid_sink_nodes(self, sink_node_list):
        """
        Iterate through each string in a passed in list.
        Look for all valid sink nodes in each string.

        @type  sink_node_list: list
        @param sink_node_list: The location of a given Enron text file.
        """
        sink_nodes = []
        for i, line in enumerate(sink_node_list):
            nodes_from_line = self.get_enron_addresses_from_line(line)
            sink_nodes += nodes_from_line
        return sink_nodes


    def find_source_node(self, a_string):
        """
        Look for an Enron source node in a given string.

        @type  a_string: str
        @param a_string: A line from Enron text file possibly containing a source node.
        """
        prefix = len("From: ")
        source_node = a_string[prefix:]
        if self.address_is_valid(source_node):
            return self.remove_email_suffix(source_node)
        else:
            return ""


    def get_enron_addresses_from_line(self, a_line):
        """
        Find all the valid enron addresses in a given string.
        Return as a list.

        @type  a_line: str
        @param a_line: A line from Enron text file possibly containing zero or more valid enron addresses.

        @rtype: list
        @return: A list of valid Enron addresses.
        """
        sink_nodes = []
        line_values = a_line.split(",") #
        for node in line_values:
            node = node.replace(" ", "")
            if self.address_is_valid(node):
                node = self.remove_email_suffix(node)
                sink_nodes.append(node)
        return sink_nodes

    def address_is_valid(self, a_string):
        """
        Check if a given string matches the valid Enron address pattern.

        @type  a_string: str
        @param a_string: An email address being checked against criteria.

        @rtype: bool
        @return: True if the string is valid, else False
        """
        is_valid = False
        strings = []
        email_suffix = "@enron.com"
        if a_string.endswith(email_suffix):
            a_string = self.remove_email_suffix(a_string)
            if '.' in a_string:
                i = a_string.find('.')
                string_before_dot = a_string[:i]
                strings.append(string_before_dot)
                j = i + 1
                string_after_dot = a_string[j:]
                strings.append(string_after_dot)

        if len(strings) == 2:
            for i, a_string in enumerate(strings):
                if a_string in self.invalid_strings or any(i.isdigit() for i in a_string):
                    return False
                if i == 1:
                    if '.' in a_string:
                        return False
            is_valid = True
        return is_valid




    def remove_email_suffix(self, a_string):
        """
        Helper function to exclude email address from
        end of a passed in string.

        @type  a_string: str
        @param a_string: An email address

        @rtype: str
        @return: The passed in string with its email identifier removed.
        """
        i = a_string.find("@")
        return a_string[:i]



