import re, string

class EnronFileReader:
    def __init__(self):
        self.placeholder = False

    def get_email_attributes(self, email_location):
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
        elements = []
        i = 0
        with open(email_location, "r") as f:
            for line in f:
                line = line.lstrip()
                line = line.rstrip('\n')
                if i == 0:
                    msg_id = self.get_msg_id(line)
                elif i == 1:
                    pass
                elif i == 2:
                    sender = self.get_sender(line)
                elif i >= 3:
                    elements.append(line)
                    if line.endswith(','):
                        pass
                    else:
                        receivers = self.get_all_receivers(elements)
                        break
                i += 1

        return sender, receivers, msg_id


    def get_all_receivers(self, receiver_list):
        receivers = []
        for i, line in enumerate(receiver_list):
            if i == 0:
                line = line[4:]
            line_receivers = self.get_receivers_from_line(line)
            receivers += line_receivers

        return receivers

    def get_msg_id(self, a_string):
        return "".join([i for i in a_string if i.isdigit()])

    def get_sender(self, a_string):
        prefix = len("From: ")
        sender = a_string[prefix:]
        if self.address_is_valid(sender):
            return self.remove_email_address(sender)


    def get_receivers_from_line(self, receiver_str):
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