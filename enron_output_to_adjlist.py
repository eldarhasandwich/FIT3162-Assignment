
import classes.AdjacencyList as AL

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
    f = open("plaintexts/enron_output.txt", 'r')
    text = f.read()
    f.close()

    uniqueActorIDs = {}
    nextID = 1
    lines = text.split("\n")
    for l in lines:
        s, r = LineToIndividuals(l)

        if s not in uniqueActorIDs:
            uniqueActorIDs[s] = str(nextID)
            nextID += 1

        for recip in r:
            if recip not in uniqueActorIDs:
                uniqueActorIDs[s] = str(nextID)
                nextID += 1

    adjList = AL.AdjacencyList()
    for l in lines:
        s, r = LineToIndividuals(l)

        for recip in r:
            adjList.AddSenderRecipientPair(uniqueActorIDs[s], s, uniqueActorIDs[recip], recip)



if __name__ == "__main__":
    print(EnronOutputToAdjList())
