from read_files import EmailReader

my_reader = EmailReader()

def check_receivers():
    receivers = ["To: myers.je@enron.com, heinecke.justin@enron.com, john.suarez@enron.com,",
                          "mmoore@enron.com, stanton.scott@enron.com, vaccaro.john@enron.com,",
                          "yamamura.alan@enron.com, belavielle@enron.com"]


    assert my_reader.get_all_receivers(receivers) == ['myers.je', 'heinecke.justin', 'john.suarez',
                                                     'stanton.scott', 'vaccaro.john', 'yamamura.alan']


check_receivers()




