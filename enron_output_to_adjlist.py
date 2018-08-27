import classes.AdjacencyList as AL
from graph_statistics import GraphStatistics

def LineToIndividuals(line):
    if line == ['']: return False, False
    words = line.split(" ")
    relaventWords = []
    for w in words:
        if w not in ['Email', 'sent', 'by', 'to', '']:
            if w[-1] == ',': relaventWords.append(w[:-1])
            else: relaventWords.append(w)
    
    sender = relaventWords[0]
    recipients = relaventWords[1:]
    return sender, recipients


def EnronOutputToAdjList():
    f = open("enron_output.txt", 'r')
    text = f.read()
    f.close()

    lines = text.split("\n")

    adjList = AL.AdjacencyList()
    for l in lines:
        s, r = LineToIndividuals(l)

        for recip in r:
            adjList.AddSenderRecipientPair(s, s, recip, recip)

    return adjList



if __name__ == "__main__":
    adj_list = EnronOutputToAdjList()
    graph_statistics = GraphStatistics()
    for sender in adj_list.senders:
        sender = adj_list.get_sender_as_object(sender)
        graph_statistics.add_data(sender)
        break

    print(graph_statistics.get_density())
