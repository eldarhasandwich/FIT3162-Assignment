import math, io, os, re, string, time
from enron_reader import EnronFileReader
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

            groups = files.groups
            graph_input = "graph_input.txt"
            with io.open(graph_input, "w", encoding = "utf-8") as f:
                files.write_to_file(f)
                groups.write_statistics_to_file(f)

class EnronParser:
    def __init__(self, a_directory):
        self.directory = a_directory
        self.enron_file_reader = EnronFileReader()
        self.file_container = FileContainer()
        self.file_count = 0
        self.file_limit = math.inf
        self.msg_ids = {}

    def process_directory(self):
        end_iteration = False
        for dir_name, subdir, file_list in os.walk(self.directory):
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
        sender, receivers, msg_id = self.enron_file_reader.get_email_attributes(file)
        if msg_id not in self.msg_ids:
            if self.attributes_are_valid(sender, receivers):
                self.file_container.add_file(sender, receivers)

        return sender, receivers

    def attributes_are_valid(self, sender, receivers):
        if sender is None or len(receivers) == 0:
            return False
        else:
            return True


class WikiVoteParser:
    def __init__(self, file):
        self.file = file
        self.file_container = FileContainer()

    def process_wiki_vote_file(self):
        with open(self.file, 'r') as f:
            for i, line in enumerate(f):
                if i >= 4:
                    sender, receiver = self.get_sender_and_receiver(line)
                    receiver = [receiver]
                    self.file_container.add_file(sender, receiver)


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
                self.file_container.add_file(sender, receiver)
                sender, receiver = None, None

class File:
    def __init__(self, sender, receivers):
        self.sender = sender
        self.receivers = receivers


    def output_string(self):
        a_str = "{0} to ".format(self.sender)
        for r in range(0, len(self.receivers) - 1):
            receiver = self.receivers[r]
            a_str += receiver+", "
        a_str += self.receivers[-1]
        return a_str


class FileContainer:
    def __init__(self):
        self.elements = []
        self.groups = Groups()

    def add_file(self, sender, receivers):
        self.groups.add(sender, receivers)
        file = File(sender, receivers)
        self.elements.append(file)

    def write_to_file(self, output):
        for file in self.elements:
            file_string = file.output_string()
            output.write(file_string)
            output.write("\n")


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






