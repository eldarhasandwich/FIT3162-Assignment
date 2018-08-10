
import psycopg2
# from classes.AdjacencyMatrix import *
# from classes.AdjacencyList import *
import classes.AdjacencyList as AL
import enron_output_to_adjlist as enron

conn = psycopg2.connect("dbname=testsnagraphs user=eldar")

# CREATE
# READ
# UPDATE
# DELETE

"""
Some notes about psycopg, its trash.
Details: There does not seem to be safe built in error catching for very simple exception scenarios,
such as foreign key violations, meaning that these will need to be caught with try/except clauses
because the whole program crashes if the database is not happy with you 
"""

def RunQuery (qString):
    cur = conn.cursor()
    cur.execute(qString)
    print(cur.fetchall())
    cur.close()

# create new graph
# params: graph name
# returns: new graph ID
def CREATE_NewGraph (newName):
    cur = conn.cursor()
    cur.execute("INSERT INTO graphs (name) VALUES ('" + newName + "') RETURNING id;")
    newID = cur.fetchall()[0]
    conn.commit()
    cur.close()
    return newID

# create new node
# params: graphID, data (node emailAddr)
# returns: new nodeID
def CREATE_NewNode (graphID, data):
    cur = conn.cursor()
    cur.execute("INSERT INTO nodes (email, graph_ID) VALUES (%s, %s) RETURNING id;", (data, graphID))
    newID = cur.fetchall()[0]
    conn.commit()
    cur.close()
    return newID

# create new edge
# params: graphID, senderID, recipID, data (emailcount)
# returns: new edgeID
def CREATE_NewEdge (graphID, senderID, recipientID, data):
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO edges (graph_ID, sender_ID, recipient_ID, email_count) VALUES (%s, %s, %s, %s) RETURNING id", 
        (graphID, senderID, recipientID, data)
    )
    newID = cur.fetchall()[0]
    conn.commit()
    cur.close()
    return newID

# returns array of all graphObjects
def READ_AllGraphs ():
    cur = conn.cursor()
    cur.execute("SELECT * FROM graphs")
    value = cur.fetchall()
    cur.close()
    return value

# returns array of all nodes in a given graph
def READ_NodesInGraph (graphID):
    cur = conn.cursor()
    cur.execute("SELECT * FROM nodes WHERE graph_ID = %s", (graphID))
    value = cur.fetchall()
    cur.close()
    return value

# returns array of all edges in a given graph
def READ_EdgesInGraph (graphID):
    cur = conn.cursor()
    cur.execute("SELECT * FROM edges WHERE graph_ID = %s", (graphID))
    value = cur.fetchall()
    cur.close()
    return value

# update edge data
# params: edgeID, data (emailcount)
def UPDATE_EdgeData (edgeID, data):
    cur = conn.cursor()
    cur.execute("UPDATE edges SET email_count = %s WHERE id = %s", (data, edgeID))
    conn.commit()
    cur.close()   

def PullListFromDB (graphID):
    graphID = str(graphID) #Typeerror without this line
    nodes = READ_NodesInGraph(graphID)
    edges = READ_EdgesInGraph(graphID)

    adjList = AL.AdjacencyList()
    for e in edges:
        senderID = e[1]
        receiverID = e[2]
        emailCount = e[4]
        shouldIncrement = False

        senderFilter = filter(lambda n : n[0] == senderID, nodes) # TODO: these filters are a bit ineffificient, change sometime
        receiverFilter = filter(lambda n : n[0] == receiverID, nodes)

        senderEmail = list(senderFilter)[0][1]
        receiverEmail = list(receiverFilter)[0][1]

        adjList.AddSenderRecipientPair(senderID, senderEmail, receiverID, receiverEmail, emailCount, shouldIncrement)

    return adjList

def PushListToDB (graphID, _AdjacencyList):
    nodeDict = {}
    nodeArr = []
    edgeArr = []

    for key, sender in _AdjacencyList.senders.items():
        if key not in nodeDict:
            nodeDict[key] = {"key": key, "address": sender.emailAddress, "graphID": graphID}
        else: pass
        for key, recipient in sender.recipients.items():
            if key not in nodeDict:
                nodeDict[key] = {"key": key, "address": sender.emailAddress, "graphID": graphID}
            else: pass

            edgeArr.append({"sender": sender.id, "recip": recipient.id, "count": recipient.emailCount, "graphID": graphID})

    for key, node in nodeDict.items():
        nodeArr.append(node)

    print("DB nodes: (graph#" + str(graphID) + ")")
    for n in nodeArr: print(n)
    print("DB edges: (graph#" + str(graphID) + ")")
    for e in edgeArr: print(e)


if __name__ == "__main__":
    adjList = enron.EnronOutputToAdjList()
    PushListToDB(1, adjList)
