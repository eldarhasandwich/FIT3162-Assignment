import re, string

class EnronFileReader:
    """
    Contains the logic for extracting nodes from an Enron text file.
    """
    def __init__(self):
        self.invalid_strings = {"enron": True, "mail": True, "all": True, "outlook": True}

    def find_attributes(self, file_location):
        """
        Iterate through each line in an Enron file to find the message id,
        source node and sink nodes.

        @type  file_location: str
        @param file_location: The location of a given Enron text file.
        """
        line_valid = True
        attributes = []
        elements = []
        with open(file_location, "r") as f:
            for i, line in enumerate(f):
                line = line.strip()
                a_string = line.replace('\t', "")
                if i == 0:
                    attributes.append(a_string)
                elif i == 2:
                    source_node = self.find_source_node(a_string)
                    if source_node:
                        attributes.append(source_node)
                elif i >= 3:
                    if line_valid:
                        if i == 3:
                            if a_string.startswith('To: '): #check first line is valid
                                elements.append(a_string[4:])
                            else:
                                line_valid = False
                        else:
                            elements.append(a_string)
                            if not a_string.endswith(','):
                                sink_nodes = self.get_valid_sink_nodes(elements)
                                if len(sink_nodes) > 0:
                                    attributes.append(sink_nodes)
                                line_valid = False
                    else:
                        break
        return attributes

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
            if len(nodes_from_line) > 0:
                sink_nodes += nodes_from_line
        return sink_nodes


    def find_source_node(self, a_string):
        """
        Look for an Enron source node in a given string.

        @type  a_string: str
        @param a_string: A line from Enron text file possibly containing a source node.

        @rtype: str
        @return: An Enron address if it is valid, else an empty string.
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



