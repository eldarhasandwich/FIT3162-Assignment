import os, re, string

class FileProcessor:
    def __init__(self):
        self.directory = "C:\\Users\\Valued Customer\\Desktop\\maildir"
        self.email_reader = FileReader()


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
                    sender, receivers = self.email_reader.get_sender_and_receiver(file_location)

class FileReader:
    def __init__(self):
        self.sender_substring = "From:"
        self.receiver_substring = "To:"
        self.email_suffix = "@enron.com"
        self.output = open("output.txt", 'w')

    def get_sender_and_receiver(self, email):
        sender, receivers = None, None
        with open(email, 'r') as f:
            contents = f.readlines()
            for line in contents:
                line = line.rstrip('\n')
                if self.sender_substring in line and not sender:
                    sender = self.get_email_address(line)
                elif line.startswith(self.receiver_substring) and not receivers:
                    receivers = self.get_all_receivers(line)
                if sender and receivers:
                    self.output.write("Email sent by "+str(sender)+" to "+', '.join(receivers))
                    self.output.write("\n")
                    break
        return sender, receivers

    def get_all_receivers(self, a_string):
        stored_receivers = []
        a_string = a_string.replace(" ", "")
        a_string = a_string[3:]
        all_receivers = a_string.split(",")
        for receiver in all_receivers:
            valid_receiver = receiver.translate(string.punctuation)
            val = self.get_email_address(valid_receiver)
            if val:
                if self.email_is_valid(val):
                    stored_receivers.append(val)
        if len(stored_receivers) > 0:
            return stored_receivers




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
            email_str = email_str[start_i:][::-1]
            return email_str

    def email_is_valid(self, a_string):
        m = re.search(r"^[a-z]+([.])[a-z]+$", a_string)
        if m:
            return True
        return False


#create email object with email text file - get below attributes in class
#store all emails as objects in a emailDict class to look for duplicates
class Email:
    def __init__(self, sender, receiver, id, date, time):
        self.sender = sender
        self.receiver = receiver
        self.id = id
        self.date = date
        self.time = time

file_processor = FileProcessor()
file_processor.process_all_files_in_directory()








