import math, os, re, string, time
from groups import Groups


class Parser:
    def __init__(self):
        self.file_container = FileContainer()
        self.groups = Groups()
        self.file_types = ["enron", "wiki-vote", "wiki-rfa"]

    def process_data_set(self, data_file, file_type):
        if file_type in self.file_types:
            if file_type == "enron":
                enron_parser = EnronParser(data_file)
                enron_parser.process_directory()
                files = enron_parser.file_container
            elif file_type == "wiki-vote":
                wiki_vote_parser = WikiVoteParser(data_file)
                wiki_vote_parser.process_wiki_vote_file()
                files = wiki_vote_parser.file_container
            else:
                wiki_rfa_parser = WikiRFAParser(data_file)
                wiki_rfa_parser.process_wiki_rfa_file()
                files = wiki_rfa_parser.file_container

            graph_input = open("graph_input.txt", 'w')
            files.write_to_file(graph_input)

class EnronParser:
    def __init__(self, a_directory):
        self.directory = a_directory
        self.enron_file_reader = EnronFileReader()
        self.file_container = FileContainer()
        self.file_count = 0
        self.file_limit = 5000

    def process_directory(self):
        end_iteration = False
        for dir_name, subdir, file_list in os.walk(self.directory):
            if end_iteration:
                break
            for file in file_list:
                if self.file_count < self.file_limit:
                    self.file_count += 1
                    file_location = str(dir_name + "\\" + file)
                    self.process_file(file_location)  # pass the file to the parser
                else:
                    end_iteration = True
                    break

    def process_file(self, file):
        sender, receivers, msg_id = self.enron_file_reader.get_email_attributes(file)
        if self.attributes_are_valid(sender, receivers):
            self.file_container.add_file(sender, receivers, msg_id)

        return sender, receivers

    def attributes_are_valid(self, sender, receivers):
        """checks if the sender and receiver objects are valid

            Args:
                sender: a string (or None) representing the sender of an email
                receivers: a list of strings (representing receivers) containing 0 or more
            Returns:
                True if the attributes are valid else returns False

        """
        if sender is None or len(receivers) == 0:
            return False
        else:
            return True


class WikiVoteParser:
    def __init__(self, file):
        self.file = file
        self.file_container = FileContainer()

    def process_wiki_vote_file(self):
        c = 0
        with open(self.file, 'r') as f:
            for i, line in enumerate(f):
                if i >= 4:
                    sender, receiver = self.get_sender_and_receiver(line)
                    receiver = [receiver]
                    self.file_container.add_file(sender, receiver, c)
                c += 1

    def get_sender_and_receiver(self, line):
        i = line.find('\t')
        j = i + 1
        k = line.find('\n')
        return line[:i], line[j:k]

class WikiRFAParser:
    def __init__(self, file):
        self.file = file
        self.file_container = FileContainer()

    def process_wiki_rfa_file(self):
        c = 0
        sender, receiver = None, None
        sender_index = 0
        receiver_index = 1
        f = open(self.file, encoding = "utf8")
        for i, line in enumerate(f):
            line = line.rstrip()
            if i == sender_index:
                if line.startswith("SRC:"):
                    sender = line[4:]
                    sender_index += 8
            elif i == receiver_index:
                if line.startswith("TGT:"):
                    receiver = line[4:]
                    receiver_index += 8
            else:
                pass
            if sender and receiver:
                receiver = [receiver]
                self.file_container.add_file(sender, receiver, c)
                sender, receiver = None, None
            c += 1








class EnronFileReader:
    def __init__(self):
        self.placeholder = False

    def get_email_attributes(self, email):
        """Search for the essential attributes of an Enron email.

            Args:
                email: the file within Enron directory.
            Returns:
                sender, receiver(s) and msg_id which are strings (if they are found, else these are None)
                group_members, a list of all enron employees
            Raises:
                TypeError: if n is not a number.
                ValueError: if n is negative.

        """
        sender, receivers, msg_id = None, None, None
        with open(email, 'r') as f:
            contents = f.readlines()
            for i, line in enumerate(contents):
                line = self.clean_line(line)
                if i == 0:
                    msg_id = self.get_msg_id(line)
                elif i == 1:
                    pass
                elif i == 2:
                    sender = self.get_sender(line)
                else:
                    receivers = self.get_all_receivers(contents[3:])
                    break
        return sender, receivers, msg_id

    def get_all_receivers(self, a_list):
        """get all receivers of an email

            Args:
                list: a list of strings from the email being checked, from the fourth line onwards.
        	Returns:
                a list of strings containing all receiver strings
            Raises:
                TypeError: if list is not a list

        """
        receivers = []
        for i, line in enumerate(a_list):
            if i == 0:
                line = self.clean_line(line)
            else:
                line = self.remove_symbols(line)
                line = line.lstrip()
            if self.is_more_receiver_lines(line):
                end = False
                line = line[:-1]
            else:
                end = True
            line_receivers = self.get_receivers_from_line(line)
            receivers += line_receivers
            if end:
                return receivers


    def clean_line(self, line):
        """Helper function to remove invalid characters from the string by calling other methods

            Args:
                line: a string representing a single line from email
        	Returns:
                the passed in string excluding the unwanted characters
            Raises:
                TypeError: if line is not a string

        """
        line = self.remove_symbols(line)
        line = self.remove_prefix(line)
        return line

    def remove_symbols(self, a_string):
        """Helper function to remove symbol characters from the start and end of line

            Args:
                a_string: line from an email
            Returns:
                the passed in string excluding the unwanted symbols
            Raises:
                TypeError: if line is not a string

        """
        a_string = a_string.rstrip('\n')
        a_string = a_string.strip('\t')
        return a_string

    def is_more_receiver_lines(self, line):
        return line.endswith(",")

    def get_msg_id(self, a_string):
        return "".join([i for i in a_string if i.isdigit()])

    def get_sender(self, a_string):
        if self.address_is_valid(a_string):
            return self.remove_email_address(a_string)


    def get_receivers_from_line(self, receiver_str):
        """Find all recipients of an email

            Args:
                receiver_str: the fourth line of an Enron email containing the email recipients.
            Returns:
                a list of all receivers
            Raises:
                TypeError: if receiver_str is not a string.

        """
        receivers = []
        all_receivers = receiver_str.split(",") #
        for receiver in all_receivers:
            receiver = receiver.replace(" ", "")
            if self.address_is_valid(receiver):
                receiver = self.remove_email_address(receiver)
                receivers.append(receiver)
        return receivers

    def address_is_valid(self, a_string):
        """Check if an email address is a valid enron address
            Args:
                a_string: a string representing a potentially valid email address
            Returns:
                True if the address matches the criteria, else False
            Raises:
                TypeError: if a_string is not a string

        """
        email_suffix = "@enron.com"
        if a_string.endswith(email_suffix):
            temp = self.remove_email_address(a_string)
            if self.matches_regex(temp):
                return True
        return False

    def is_enron_email(self, a_str):
        """Helper fucntion to checks if a string ends with Enron address suffix

            Args:
                a_str: the string being checked
            Returns:
                True if string ends with suffix, else False
            Raises:
                TypeError: if a_str is not a string.
        """
        email_suffix = "@enron.com"
        return a_str.endswith(email_suffix)


    def matches_regex(self, a_string):
        """Checks if string matches the given regular expression

            Args:
                a_string: the string being checked against regex
            Returns:
                True if the string matches, else False
            Raises:
                TypeError: if a_string is not a string

        """
        if re.match(r"[a-z]+.*([.])[a-z]+$", a_string):
            return True
        return False

    def remove_prefix(self, a_string):
        """Helper function to remove whitespace from the beginning of string

            Args:
                a_string: a string representing a single line from email
            Returns:
                the passed in string excluding the unwanted characters
            Raises:
                TypeError: if line is not a string

        """
        for i, char in enumerate(a_string):
            if char == " ":
                return a_string.replace(" ", "")[i:]


    def remove_punctuation(self, a_string):
        """Helper function to remove punctuation from string

            Args:
                a_string: the string being checked
            Returns:
                the passed in string without punctuation
            Raises:
                TypeError: if n is not a number.
                ValueError: if n is negative.

        """
        return a_string.translate(string.punctuation)


    def remove_email_address(self, a_string):
        i = a_string.find("@")
        return a_string[:i]


class File:
    def __init__(self, sender, receivers, file_id):
        self.sender = sender
        self.receivers = receivers
        self.file_id = file_id

    def output_string(self):
        a_str = "{0} to ".format(self.sender)
        for r in range(0, len(self.receivers) - 1):
            receiver = self.receivers[r]
            a_str += receiver+", "
        a_str += self.receivers[-1]
        return a_str


class FileContainer:
    def __init__(self):
        self.unique_files = []
        self.unique_ids = {}
        self.duplicate_files = []
        self.invalid_files = []

    def file_is_unique(self, file_id):
        if file_id in self.unique_ids:
            return False
        return True

    def add_file(self, sender, receivers, file_id):
        file = File(sender, receivers, file_id)
        if self.file_is_unique(file_id):
            self.unique_ids[file_id] = True
            self.unique_files.append(file)
        else:
            self.duplicate_files.append(file)

    def write_to_file(self, output):
        for file in self.unique_files:
            file_string = file.output_string()
            try:
                output.write(file_string)
                output.write("\n")
            except:
                pass

def main():
    enron_path = "C:\\Users\\Valued Customer\\Desktop\\maildir"
    wiki_vote_path = "wiki-vote.txt"
    wiki_rfa_path = "C:\\Users\\Valued Customer\\Desktop\\wiki-RfA.txt"
    user_input = str(input('Select data set: \n'
                           '1. Enron \n'
                           '2. Wiki-Vote \n'
                           '3. Wiki-RfA \n'))
    if user_input == '1':
        location = enron_path
        file_type = "enron"
    elif user_input == '2':
        location = wiki_vote_path
        file_type = "wiki-vote"
    else:
        location = wiki_rfa_path
        file_type = "wiki-rfa"
    if os.path.exists(location):
        parser = Parser()
        parser.process_data_set(location, file_type)
    else:
        print("No file found for {0} data set.".format(file_type))

if __name__ == "__main__":
    main()






