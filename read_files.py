import os, re, string, time

class FileProcessor:
    def __init__(self, directory):
        self.directory = directory
        self.email_reader = EmailReader()
        self.email_container = EmailContainer()
        self.groups = Groups()
        self.file_count = 0
        self.file_limit = 500000000

    def process_directory_files(self):
        file_type = "sent"
        my_emails = []
        for dir_name, subdir, file_list in os.walk(self.directory):
            if self.file_count < self.file_limit:
                for file_name in file_list:
                    self.file_count += 1
                    file_location = self.concatenate_file_location(dir_name, file_name)
                    sender, receivers, id, group_members = self.email_reader.get_email_attributes(file_location)
                    if sender and receivers and id:
                        if self.email_container.email_is_unique(sender, receivers, id):
                            self.email_container.add_email(sender, receivers, id)

                    if group_members:
                        self.groups.add(group_members)

        return my_emails

    def concatenate_file_location(self, dir_name, file_name):
        return str(dir_name + "\\" + file_name)

class EmailReader:
    def __init__(self):
        self.email_read = False

    def get_email_attributes(self, email):
        sender, receivers, id, group_members = None, None, None, None
        with open(email, 'r') as f:
            contents = f.readlines()
            for line in contents:
                line = line.rstrip('\n')
                if not id:
                    id = self.get_id(line)
                if not sender:
                    sender = self.get_sender(line)
                if not receivers:
                    receivers = self.get_receivers(line)
                if sender and receivers and id:
                    if len(receivers) > 1:
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
        return self.email_structure_is_correct(a_string)

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

    def email_structure_is_correct(self, a_string):
        m = re.search(r"^[a-z]+([.])[a-z]+$", a_string)
        if m:
            return True
        return False

class Email:
    def __init__(self, sender, receivers, message_id):
        self.sender = sender
        self.receivers = receivers
        self.message_id = message_id

    @staticmethod
    def static_identifier_string(sender, receivers, message_id):
        return str(sender + " " + ', '.join(receivers) + ' {0}'.format(message_id))

    def identifier_string(self):
        return str(self.sender + " " + ', '.join(self.receivers) + ' {0}'.format(self.message_id))

class EmailContainer:
    def __init__(self):
        self.email_identifiers = {}
        self.unique_emails = []

    def email_is_unique(self, sender, receivers, id):
        return Email.static_identifier_string(sender, receivers, id) not in self.email_identifiers

    def add_email(self, sender, receivers, id):
        self.email_identifiers[Email.static_identifier_string(sender, receivers, id)] = True
        self.unique_emails.append(Email(sender, receivers, id))

    def get_emails(self):
        return self.unique_emails

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


class Groups:
    def __init__(self):
        self.elements = {}
        self.c = 0

    def add(self, members):
        assert isinstance(members, list)
        assert len(members) > 2
        sender = members[0]
        receivers = members[1:]
        members.sort()
        key = self.create_dict_key(members)
        if key not in self.elements:
            print(key)
            self.c += 1
            self.elements[key] = Group(members, sender, receivers, key)
        else:
            self.elements[key].add_email(sender, receivers)

    def create_dict_key(self, members):
        my_str = " "
        for e in members:
            my_str += str(e) + ", "
        return my_str[:-2]

    def write_groups_to_file(self, output):
        all_groups = self.elements
        for key in all_groups:
            all_groups[key].write_to_file(output)
        output.write("{0} total groups.".format(self.c))


def main():
    start = time.time()
    my_directory = "C:\\Users\\Valued Customer\\Desktop\\maildir"
    group_output = open("output.txt", 'w')
    file_processor = FileProcessor(my_directory)
    all_emails = file_processor.process_directory_files()
    file_processor.groups.write_groups_to_file(group_output)
    total_files = file_processor.file_count
    end = time.time()
    print("{0} files read in {1}".format(total_files, end - start))

if __name__ == "__main__":
    main()


