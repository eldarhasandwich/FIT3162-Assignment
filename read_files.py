import os, re, string

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
        self.output_file = "test.txt"



    def process_all_files_in_directory(self):
        file_count = 0
        file_limit = 5000
        for dir_name, subdir, file_list in os.walk(self.directory):
            if "sent" in dir_name:
                #if file_count > file_limit:
                    #return
                for file_name in file_list:
                    file_count += 1
                    file_location = str(dir_name + "\\" + file_name)
                    sender, receiver = self.email_reader.get_sender_and_receiver(file_location)
                    if sender and receiver:
                        self.adj_matrix.add(sender, receiver)



    def write_emails_to_textfile(self):
        output = open(self.output_file, 'w')
        line = 0
        max_count = 0
        email_count = 0
        N = self.adj_matrix.c
        for i in range(N):
            has_sent = False
            sender = self.adj_matrix.vals[i]
            for j in range(N):
                if i != j:
                    recipient = self.adj_matrix.vals[j]
                    val = self.adj_matrix.elements[i][j]
                    if val > 0:
                        has_sent = True
                        if val > max_count:
                            max_count = val
                        email_count += val
                        output.write(str(val) + " emails to " + recipient)
                        output.write("\n")
                        line += 1
            if has_sent:
                output.write("WERE SENT FROM: " + sender)
                output.write("\n")
                output.write("\n")

        output.write("There are {0} unique email addresses ending with @enron.com".format(str(N)))
        output.write("\n")
        output.write("In total, {0} emails were sent amongst these addresses".format(str(email_count)))
        output.write("\n")
        output.write("The highest number of emails sent from one address to another was {0}".format(str(max_count)))





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
        m = re.search(r"^[a-z]+([.])[a-z]+$", a_string)
        if m:
            return m.group() == a_string
        else:
            return False


email_finder = FileProcessor()
email_finder.process_all_files_in_directory()
email_finder.write_emails_to_textfile()





