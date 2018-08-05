import os

class AdjacencyMatrix:
    def __init__(self):
        self.keys = {}
        self.vals = {}
        self.c = 0
        self.elements = [[0 for _ in range(10000)] for _ in range(10000)]


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

class FileProcessor:
    def __init__(self):
        self.directory = "C:\\Users\\Valued Customer\\Desktop\\maildir"
        self.email_reader = FileReader()
        self.adj_matrix = AdjacencyMatrix()
        self.output = open("test.txt", 'w')


    def process_all_files_in_directory(self):
        for dir_name, subdir, file_list in os.walk(self.directory):
            if "sent" in dir_name:
                for file_name in file_list:
                    file_location = str(dir_name + "\\" + file_name)
                    sender, receiver = self.email_reader.get_sender_and_receiver(file_location)
                    if sender and receiver:
                        self.adj_matrix.add(sender, receiver)



    def write_emails_to_textfile(self):
        max_count = 0
        email_count = 0
        N = self.adj_matrix.c
        for i in range(N):
            sender = self.adj_matrix.vals[i]
            self.output.write(sender + " has sent:")
            self.output.write("\n")
            for j in range(N):
                if i != j:
                    recipient = self.adj_matrix.vals[j]
                    val = self.adj_matrix.elements[i][j]
                    if val > 0:
                        if val > max_count:
                            max_count = val
                        email_count += val
                        self.output.write(str(val) + " emails to " + recipient)
                        self.output.write("\n")
            self.output.write("\n")
        self.output.write("There are {0} unique email addresses ending with @enron.com".format(str(N)))
        self.output.write("\n")
        self.output.write("In total, {0} emails were sent amongst these addresses".format(str(email_count)))
        self.output.write("\n")
        self.output.write("The highest number of emails sent from one address to another was {0}".format(str(max_count)))





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
                email_str += a_string[i]
                i -= 1
            email_str.join(email_str.split())
            return email_str[::-1]



email_finder = FileProcessor()
email_finder.process_all_files_in_directory()
email_finder.write_emails_to_textfile()