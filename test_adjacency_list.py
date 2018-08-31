
import classes.AdjacencyList as AL

def init_adjlist(adjList = None):
    if not adjList:
        adjList = AL.AdjacencyList()
    
    # instansiate an adjlist from file
    f = open('plaintexts/adjlist_test.txt')
    data = f.readlines()
    f.close
    for line in data:
        a = line.split(' ')
        adjList.AddSenderRecipientPair(a[0], a[1], a[2], a[3][:-1])

    return adjList

def test_sender_number_of_recipients():
    adjList = init_adjlist()
    
    assert adjList.senders['1'].number_of_recipients() == 2
    assert adjList.senders['2'].number_of_recipients() == 2
    assert adjList.senders['3'].number_of_recipients() == 3
    assert adjList.senders['4'].number_of_recipients() == 1


def test_sender_to_string():
    adjList = init_adjlist()

    assert adjList.senders['1'].toString() == '1'
    assert adjList.senders['2'].toString() == '2'
    assert adjList.senders['3'].toString() == '3'

def test_sender_emailAddress():
    adjList = init_adjlist()

    assert adjList.senders['1'].emailAddress == 'bob'
    assert adjList.senders['2'].emailAddress == 'jim'
    assert adjList.senders['3'].emailAddress == 'greg'

def test_recipients_as_list():
    adjList = init_adjlist()

    bobList = adjList.senders['1'].recipients_as_list()
    jimList = adjList.senders['2'].recipients_as_list()
    gregList = adjList.senders['3'].recipients_as_list()

    assert bobList == [('2', 5), ('3', 6)]
    assert jimList == [('3', 2), ('1', 1)]
    assert gregList == [('2', 3), ('1', 7), ('4', 3)]

def test_adding_pairs():
    adjList = init_adjlist()

    assert adjList.senders['1'].recipients['2'].emailCount == 5
    assert adjList.senders['1'].recipients['3'].emailCount == 6
    assert adjList.senders['2'].recipients['1'].emailCount == 1
    assert adjList.senders['2'].recipients['3'].emailCount == 2
    assert adjList.senders['3'].recipients['1'].emailCount == 7
    assert adjList.senders['3'].recipients['2'].emailCount == 3

    adjList = init_adjlist(adjList) # we just double the pairs

    assert adjList.senders['1'].recipients['2'].emailCount == 10
    assert adjList.senders['1'].recipients['3'].emailCount == 12
    assert adjList.senders['2'].recipients['1'].emailCount == 2
    assert adjList.senders['2'].recipients['3'].emailCount == 4
    assert adjList.senders['3'].recipients['1'].emailCount == 14
    assert adjList.senders['3'].recipients['2'].emailCount == 6

if __name__ == "__main__":
    pass