import math, os, re, string, time
from groups import Groups

class DirectoryProcessor:
    """ Processes the files of a passed in directory.

    """
    def __init__(self):
        self.parser = Parser()
        self.file_count = 0
        self.file_limit = math.inf

    def process_files(self, a_directory):
        """Iterate through a given directory and pass each directory file to the parser.

            Args:
                a_directory: a string of the directory's local location.
            Raises:
                TypeError: if a_directory is not a string.
                ValueError: if n is negative.

        """
        end_iteration = False
        if os.path.exists(a_directory): #check that the directory exists locally
            file_type = "enron"
            for dir_name, subdir, file_list in os.walk(a_directory):
                if end_iteration:
                    break
                for file in file_list:
                    if self.file_count < self.file_limit:
                        self.file_count += 1
                        file_location = str(dir_name + "\\" + file)
                        self.parser.process_file(file_location, file_type) #pass the file to the parser
                    else:
                        end_iteration = True
                        break



class Parser:
    def __init__(self):
        self.enron_parser = EnronParser()
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
                self.enron_parser.process_file(file, self.groups)
            elif file_type == "parser2":
                pass
            elif file_type == "parser3":
                pass



class EnronParser:
    def __init__(self):
        self.email_reader = EmailReader()
        self.email_container = EmailContainer()

    def process_file(self, file, groups):
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
            groups.add(sender, receivers)

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

    def get_all_receivers(self, list):
        receivers = []
        for i, line in enumerate(list):
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
        line = self.remove_symbols(line)
        line = self.remove_prefix(line)
        return line

    def remove_symbols(self, a_string):
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
        email_suffix = "@enron.com"
        if a_string.endswith(email_suffix):
            temp = self.remove_email_address(a_string)
            if self.matches_regex(temp):
                return True
        return False

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
        if re.match(r"[a-z]+.*([.])[a-z]+$", a_string):
            return True
        return False

    def remove_prefix(self, a_string):
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

    def add_email(self, sender, receivers, email_id):
        email = Email(sender, receivers, email_id)
        if self.email_is_unique(email_id):
            self.unique_ids[email_id] = True
            self.unique_emails.append(email)
        else:
            self.duplicate_emails.append(email)

    def write_to_file(self, output):
        for email in self.unique_emails:
            email_string = email.output_string()
            output.write(email_string)
            output.write("\n")



def main():
    start = time.time()
    my_directory = "C:\\Users\\Valued Customer\\Desktop\\maildir"
    group_output = open("output.txt", 'w')
    directory_processor = DirectoryProcessor()
    directory_processor.process_files(my_directory)
    parser = directory_processor.parser
    emails = parser.enron_parser.email_container
    groups = parser.groups
    output = open("test_output.txt", 'w')
    emails.write_to_file(output)
    groups.write_all_to_file(group_output)
    groups.write_statistics_to_file(output)
    end = time.time()
    print(end - start)



if __name__ == "__main__":
    main()






