import math, os, re, string, time

class DirectoryProcessor:
    def __init__(self):
        self.parser = Parser()
        self.file_count = 0
        self.file_limit = 25000

    def process_files(self, a_directory):
        """Iterate through a given directory and pass each directory file to the parser.

            Args:
                a_directory: a string of the directory's local location.
            Raises:
                TypeError: if a_directory is not a string.
                ValueError: if n is negative.

        """
        if os.path.exists(a_directory): #check that the directory exists locally
            file_type = "enron"
            for dir_name, subdir, file_list in os.walk(a_directory):
                if self.file_count < self.file_limit:
                    for file in file_list:
                        self.file_count += 1
                        file_location = str(dir_name + "\\" + file)
                        self.parser.process_file(file_location, file_type) #pass the file to the parser

class Parser:
    def __init__(self):
        self.email_reader = EmailReader()
        self.email_container = EmailContainer()
        self.groups = Groups()
        self.file_types = ["enron", "parser2", "parser3"]

    def process_file(self, file, file_type):
        """pass the file to the appropriate method based on its file type.

            Args:
                file: the location of the file being parsed.
                file_type: the "type" of the file as determined by the directory being checked.
            Raises:
                TypeError: if file or file_type are not strings.

        """
        if file_type in self.file_types:
            if file_type == "enron":
                self.process_enron_file(file)
            elif file_type == "parser2":
                pass
            elif file_type == "parser3":
                pass

    def process_enron_file(self, file):
        """Analyse an enron file to determine its key attributes if they exist.
           These attributes are the sender, receiver(s), message_id and groups.

            Args:
                file: the location of the file being checked
            Raises:
                TypeError: if file is not a string.

        """

        sender, receivers, msg_id = self.email_reader.get_email_attributes(file)
        if self.attributes_are_valid(sender, receivers):
            self.email_container.add_email(sender, receivers, msg_id)
            self.groups.add(sender, receivers)

    def attributes_are_valid(self, sender, receivers):
        if sender is None or len(receivers) == 0:
           return False
        else:
            return True


class EmailReader:
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
            contents = f.readlines()[:4]
            for i, line in enumerate(contents):
                line = line.rstrip('\n')
                if i == 0:
                    msg_id = self.get_msg_id(line)
                if i == 2:
                    sender = self.get_sender(line)
                if i == 3:
                    receivers = self.get_receivers(line)
                    break

        return sender, receivers, msg_id

    def get_msg_id(self, a_string):
        id_substring = "Message-ID"
        if id_substring in a_string:
            return "".join([i for i in a_string if i.isdigit()])

    def get_sender(self, a_string):
        sender_substring = "From:"
        L = len(sender_substring)
        sender = self.remove_prefix(a_string, L)
        if sender_substring in a_string:
            sender_name = self.valid_address(sender)
            if sender_name:
                return sender_name

    def get_receivers(self, receiver_str):
        """Find all recipients of an email

            Args:
                receiver_str: the fourth line of an Enron email containing the email recipients.
            Returns:
                a list of all receivers
            Raises:
                TypeError: if receiver_str is not a string.

        """
        receiver_substring = "To:"
        receivers = []
        if receiver_str.startswith(receiver_substring):
            K = len(receiver_substring)
            a_string = self.remove_prefix(receiver_str, K)
            all_receivers = a_string.split(",") #
            for receiver in all_receivers:
                receiver_name = self.valid_address(receiver)
                if receiver_name:
                    receivers.append(receiver_name)
        return receivers

    def valid_address(self, a_string):
        valid = False
        a_string = self.remove_punctuation(a_string)
        if self.is_enron_email(a_string):
            a_string = self.remove_email_address(a_string)  # self.get_email_address(receiver)
            if self.matches_regex(a_string):
                valid = True
        if valid:
            return a_string

    def is_enron_email(self, a_str):
        """Helper fucntion to checks if a string is a valid Enron address

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
        m = re.search(r"^[a-z]+([.])[a-z]+$", a_string)
        if m:
            return True
        return False

    def remove_prefix(self, a_string, N):
        return a_string.replace(" ", "")[N:]

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


class Email:
    def __init__(self, sender, receivers, message_id):
        self.sender = sender
        self.receivers = receivers
        self.message_id = message_id

    def output_string(self):
        a_str = "Email sent by {0} to ".format(self.sender)
        for r in range(0, len(self.receivers) - 1):
            receiver = self.receivers[r]
            a_str += receiver+", "
        a_str += self.receivers[-1]
        return a_str


class EmailContainer:
    def __init__(self):
        self.unique_emails = []
        self.unique_ids = {}
        self.duplicate_emails = []
        self.invalid_emails = []

    def email_is_unique(self, email_id):
        if email_id in self.unique_ids:
            return False
        return True

    def add_email(self, sender, receivers, id):
        email = Email(sender, receivers, id)
        if self.email_is_unique(id):
            self.unique_ids[id] = True
            self.unique_emails.append(email)
        else:
            self.duplicate_emails.append(email)

    def write_to_file(self, output):
        for email in self.unique_emails:
            email_string = email.output_string()
            output.write(email_string)
            output.write("\n")

#group class, stores information about communication flows between recurring clusters of employees
#currently only utilising this class for dyad/tryad counts
class Group:
    def __init__(self, sender, receivers):
        self.sorted_members = sorted([sender] + receivers)
        self.initial_sender = sender
        self.initial_receivers = receivers
        self.id_dict = self.construct_id_dict()
        self.adj_list = self.cons_adj_list()
        self.add_initial_values()

    def construct_id_dict(self):
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
        sender = ''.join(self.initial_sender)
        for index, key in enumerate(self.sorted_members):
            if key != sender:
                val = (key, 1)
                self.adj_list[sender][index] = val

    def group_exists(self, group):
        sender = group.initial_sender
        receivers = group.initial_receivers
        for receiver in receivers:
            index = self.id_dict[receiver]
            values = self.adj_list[sender]
            val = values[index]
            val_string = val[0]
            new_val_number = val[1] + 1
            new_val = (val_string, new_val_number)
            self.adj_list[sender][index] = new_val

    def write_to_file(self, output):
        output.write("Emails sent exclusively between the group of" + self.dictionary_key())
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

    def dictionary_key(self):
        my_str = " "
        for e in self.sorted_members:
            my_str += str(e) + ", "
        return my_str[:-2]


#container class for group objects
class Groups:
    def __init__(self):
        self.elements = {}
        self.sizes = {}
        self.count = 0

    #provided a list of members
    def add(self, sender, receivers):
        new_group = Group(sender, receivers)
        N = len(receivers) + 1
        if N not in self.sizes:
            self.sizes[N] = 1
        else:
            self.sizes[N] += 1
        key = new_group.dictionary_key()
        if key not in self.elements:
            self.count += 1
            self.elements[key] = new_group
        else:
            self.elements[key].group_exists(new_group)

    def groups_of_size(self, N):
        if self.sizes[N]:
            return self.sizes[N]
        else:
            return 0

    def dyad_count(self):
        return self.groups_of_size(2)

    def triad_count(self):
        return self.groups_of_size(3)

    def write_statistics_to_file(self, output):
        output.write("Dyad count: " + str(self.dyad_count()))
        output.write("\n")
        output.write("Triad count: " + str(self.triad_count()))


start = time.time()
my_directory = "C:\\Users\\Valued Customer\\Desktop\\maildir"
group_output = open("output.txt", 'w')
directory_processor = DirectoryProcessor()
directory_processor.process_files(my_directory)
parser = directory_processor.parser
emails = parser.email_container
groups = parser.groups
output = open("test_output.txt", 'w')
emails.write_to_file(output)
groups.write_statistics_to_file(output)
end = time.time()
print(end - start)







