import os, re, string
from classes.AdjacencyMatrix import *

class FileProcessor:
    def __init__(self):
        self.directory = "C:\\Users\\Valued Customer\\Desktop\\maildir"
        self.email_reader = FileReader()
        self.adj_matrix = AdjacencyMatrix()

    def process_all_files_in_directory(self):
        file_count = 0
        file_limit = 5000
        for dir_name, subdir, file_list in os.walk(self.directory):
            #if file_count > file_limit:
                #break
            if "sent" in dir_name:
                for file_name in file_list:
                    file_count += 1
                    file_location = str(dir_name + "\\" + file_name)
                    sender, receiver = self.email_reader.get_sender_and_receiver(file_location)
                    if sender and receiver:
                        self.adj_matrix.add(sender, receiver)

        return self.adj_matrix


class FileReader:
    def __init__(self):
        self.sender_substring = "From:"
        self.receiver_substring = "To:"
        self.email_suffix = "@enron.com"

    def get_sender_and_receiver(self, email):
        sender, receiver = None, None
        with open(email, 'r') as f:
            contents = f.readlines()
            for line in contents:
                line = line.rstrip('\n')
                if self.sender_substring in line and not sender:
                    sender = self.get_email_address(line)
                elif self.receiver_substring in line and not receiver:
                    receiver = self.get_email_address(line)
                if sender and receiver:
                    break
        return sender, receiver

    def get_email_address(self, a_string):
        if a_string.endswith(self.email_suffix):
            email_str = ""
            i = len(a_string) - 1
            while a_string[i] != " " and i >= 0:
                char = a_string[i]
                email_str += char
                i -= 1
            email_str.join(email_str.split())
            start_i = len(self.email_suffix)
            if self.email_is_valid(email_str[start_i:]):
                return email_str[::-1]

    def email_is_valid(self, a_string):
        a_bool = False
        m = re.search(r"^[a-z]+([.])[a-z]+$", a_string)
        if m:
            a_bool = (m.group() == a_string)
        return a_bool






file_processor = FileProcessor()
adj_matrix = file_processor.process_all_files_in_directory()
adj_matrix.write_data_to_textfile()
for node in adj_matrix.nodes:
    print(node.toString())
    #print(node.edges_as_string())







