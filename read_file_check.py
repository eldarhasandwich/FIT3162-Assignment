from read_files import EnronFileReader

my_reader = EnronFileReader()

def test_sender():
    senders = ["From: eric.bass", "From: raetta.zadow", "From: enron.announcements"]
    test_senders = [my_reader.remove_prefix(i) for i in senders]
    bools = [my_reader.matches_regex(i) for i in test_senders]
    assert bools == [True, True, True]

def test_receivers():
    receivers = ["To: myers.je@enron.com, heinecke.justin@enron.com, john.suarez@enron.com,",
                          "mmoore@enron.com, stanton.scott@enron.com, vaccaro.john@enron.com,",
                          "yamamura.alan@enron.com, belavielle@enron.com"]


    assert my_reader.get_all_receivers(receivers) == ['myers.je', 'heinecke.justin', 'john.suarez',
                                                     'stanton.scott', 'vaccaro.john', 'yamamura.alan']


def test_regex():
    test_strings = ['myers.je', 'heinecke.justin', 'john.suarez',
                    'stanton.scott', 'vaccaro.john', 'yamamura.alan', 'jfk*ew']
    bools = [my_reader.matches_regex(i) for i in test_strings]
    assert bools == [True, True, True, True, True, True, False]


test_sender()






