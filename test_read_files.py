from read_files import Parser, EmailContainer, EmailReader, Groups

test_parser = Parser()
test_reader = EmailReader()
test_email_container = EmailContainer()



def test_message_id():
    message_id = "Message-ID: <29242476.1075840325974.JavaMail.evans@thyme>"
    assert test_reader.get_id(message_id) == "292424761075840325974"


def test_sender():
    sender = "From: eric.bass@enron.com"
    assert test_reader.get_sender(sender) == "eric.bass"


def test_receiver():
    test_string = "lwbthemarine@bigplanet.com"
    assert test_reader.get_email_address(test_string) == None


def test_enron_address():
    test_string = "eric.bass"
    assert test_reader.address_is_valid(test_string)


def test_regex_1():
    test_string = "123.abc"
    assert not test_reader.address_is_valid(test_string)


def test_regex_2():
    test_string = "eric.bass"
    assert test_reader.address_is_valid(test_string)


def test_regex_3():
    a_string = "timothy.blanchard@enron.com"
    test_string = test_reader.get_email_address(a_string)
    assert test_string == "timothy.blanchard"
    assert test_reader.address_is_valid(test_string)

def test_duplicate_emails():
    sender = "sender"
    receiver = ["receiver"]
    id = "1"
    test_email_container.add_email(sender, receiver, id)
    assert not test_email_container.email_is_unique(id)

def test_group_1():
    test_groups = Groups()
    group_1 = ["a", "b", "c"]
    group_2 = ["a", "c", "b"]
    test_groups.add(group_1)
    test_groups.add(group_2)
    assert test_groups.count == 1

def test_group_2():
    test_groups = Groups()
    group_1 = ["a", "b", "c"]
    group_2 = ["a", "b", "d"]
    test_groups.add(group_1)
    test_groups.add(group_2)
    assert test_groups.count == 2

