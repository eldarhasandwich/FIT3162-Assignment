import math, os, re, string, time


#Processes the files of a provided directory
class DirectoryProcessor:
    def __init__(self, a_directory):
        self.directory = a_directory
        self.parser = Parser()
        self.email_reader = EmailReader()
        self.file_count = 0
        self.file_limit = math.inf

    #iterate through the files in directory
    #and give to parser class
    def process_files(self):
        file_type = "enron"
        for dir_name, subdir, file_list in os.walk(self.directory):
            if self.file_count < self.file_limit:
                for file in file_list:
                    self.file_count += 1
                    file_location = self.concatenate_file_location(dir_name, file)
                    self.parser.process_file(file_location, file_type)




    #helper function for creating path strings
    def concatenate_file_location(self, dir_name, file_name):
        return str(dir_name + "\\" + file_name)


#added some basic abstraction for the parser
#will make life a lot easier for implementing other parsers

class Parser:
    def __init__(self):
        self.email_reader = EmailReader()
        self.email_container = EmailContainer()
        self.groups = Groups()
        self.file_types = ["enron", "foo", "bar"]

    def process_file(self, file, file_type):
        if file_type in self.file_types:
            if file_type == "enron":
                self.process_enron_file(file)
            elif file_type == "foo":
                pass
                #logic for second parser
            elif file_type == "bar":
                pass
                #logic for third parser

    def process_enron_file(self, file):
        sender, receivers, id, group_members = self.email_reader.get_email_attributes(file)
        if sender and receivers and id:
            self.email_container.add_email(sender, receivers, id)
        if group_members:
            self.groups.add(group_members)

class EmailReader:
    def __init__(self):
        self.email_read = False

    def get_email_attributes(self, email):
        sender, receivers, id, group_members = None, None, None, None
        line_count = 0
        line_limit = 10
        with open(email, 'r') as f:
            contents = f.readlines()
            for line in contents:
                if line_count == line_limit:
                    break #exit early for efficiency
                line_count += 1
                line = line.rstrip('\n')
                if not id:
                    id = self.get_id(line)
                if not sender:
                    sender = self.get_sender(line)
                if not receivers:
                    receivers = self.get_receivers(line)
                if sender and receivers and id:
                    if len(receivers) > 0:
                        group_members = self.create_group(sender, receivers)
                    break
        return sender, receivers, id, group_members

    def create_group(self, sender, receivers):
        a_group = [sender]
        for i in receivers:
            a_group.append(i)
        return a_group


    def get_receivers(self, a_string):
        receiver_substring = "To:"
        if a_string.startswith(receiver_substring):
            receivers = []
            a_string = a_string.replace(" ", "")[3:]
            all_receivers = a_string.split(",")
            for receiver in all_receivers:
                cleaned_receiver = self.remove_punctuation(receiver)
                receiver_name = self.get_email_address(cleaned_receiver)
                if self.address_is_valid(receiver_name):
                    receivers.append(receiver_name)
            if len(receivers) > 0:
                return receivers

    def address_is_valid(self, a_string):
        m = re.search(r"^[a-z]+([.])[a-z]+$", a_string)
        if m:
            return True
        return False

    def remove_punctuation(self, a_string):
        return a_string.translate(string.punctuation)

    def get_id(self, a_string):
        id_substring = "Message-ID"
        if id_substring in a_string:
            return "".join([i for i in a_string if i.isdigit()])

    def get_sender(self, a_string):
        sender_substring = "From:"
        if sender_substring in a_string:
            return self.get_email_address(a_string)

    def get_email_address(self, a_string):
        email_suffix = "@enron.com"
        email_str = ""
        if a_string.endswith(email_suffix):
            i = len(a_string) - 1
            while a_string[i] != " " and i >= 0:
                char = a_string[i]
                email_str += char
                i -= 1
            email_str.join(email_str.split())
            j = len(email_suffix)
            email_str = email_str[j:][::-1]
        return email_str


#object storing attributes of all emails that matched
class Email:
    def __init__(self, sender, receivers, message_id):
        self.sender = sender
        self.receivers = receivers
        self.message_id = message_id

    def identifier_string(self, sender, receivers, message_id):
        return str(sender + " " + ', '.join(receivers) + ' {0}'.format(message_id))

#stores all email objects and removes duplicates
class EmailContainer:
    def __init__(self):
        self.unique_emails = []

    def email_is_unique(self, id):
        for email in self.unique_emails:
            email_id = email.message_id
            if email_id == id: #matching ids, must be duplicate
                return False
        return True

    def add_email(self, sender, receivers, id):
        if self.email_is_unique(id):
            self.unique_emails.append(Email(sender, receivers, id))


#group class, stores information about communication flows between recurring clusters of employees
#currently only utilising this class for dyad/tryad counts
class Group:
    def __init__(self, sorted_members, sender, receivers, key):
        self.sorted_members = sorted_members
        self.original_sender = sender
        self.original_receivers = receivers
        self.key = key
        self.max_communications = 1
        self.id_dict = self.cons_id_dict()
        self.adj_list = self.cons_adj_list()
        self.add_initial_values()

    def get_size(self):
        return len(self.sorted_members)

    def cons_id_dict(self):
        a_dict = {}
        for i, member in enumerate(self.sorted_members):
            a_dict[member] = i
        return a_dict

    def cons_adj_list(self):
        adj_list = {}
        for i in self.sorted_members:
            adj_list[i] = []
            for j in self.sorted_members:
                adj_list[i].append((j, 0))
        return adj_list

    def add_initial_values(self):
        for index, key in enumerate(self.sorted_members):
            if key != self.original_sender:
                val = (key, 1)
                self.adj_list[self.original_sender][index] = val

    def add_email(self, sender, receivers):
        for receiver in receivers:
            index = self.id_dict[receiver]
            values = self.adj_list[sender]
            val = values[index]
            val_string = val[0]
            new_val_number = val[1] + 1
            new_val = (val_string, new_val_number)
            if new_val_number > self.max_communications:
                self.max_communications = new_val_number
            self.adj_list[sender][index] = new_val

    def write_to_file(self, output):
        minimum_communications = 10
        if self.max_communications >= minimum_communications:
            output.write("Emails sent exclusively between the group of" + self.key)
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
        self.c = 0

    #provided a list of members
    def add(self, members):
        assert isinstance(members, list)
        members = list(set(members))
        N = len(members)
        if N >= 2:
            if N not in self.sizes:
                self.sizes[N] = 1
            else:
                self.sizes[N] += 1
            sender = members[0]
            receivers = members[1:]
            members.sort() #sort the members in a group
            key = self.create_dict_key(members) #generate the dictionary key
            if key not in self.elements: #if group doesnt exist
                self.c += 1
                self.elements[key] = Group(members, sender, receivers, key) #create
            else:
                self.elements[key].add_email(sender, receivers) #add email data to existing group instance

    def create_dict_key(self, members):
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



start = time.time()
my_directory = "C:\\Users\\Valued Customer\\Desktop\\maildir"
group_output = open("output.txt", 'w')
directory_processor = DirectoryProcessor(my_directory)
end = time.time()





