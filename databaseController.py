
import psycopg2
from classes.AdjacencyMatrix import *
from classes.AdjacencyList import *

conn = psycopg2.connect("dbname=testsnagraphs user=eldar")

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
# returns: TODO: return graph ID
def CreateNewGraph (newName):
    cur = conn.cursor()
    cur.execute("INSERT INTO graphs (name) VALUES ('" + newName + "');")
    # print(cur.fetchall())
    conn.commit()
    cur.close()

# create new node
# params: graphID, data (node emailAddr)
# returns: TODO: return nodeID
def CreateNewNode (graphID, data):
    cur = conn.cursor()
    cur.execute("INSERT INTO nodes (email, graph_ID) VALUES (%s, %s)", (data, graphID))
    conn.commit()
    cur.close()

# create new edge
# params: graphID, senderID, recipID, data (emailcount)
# returns: TODO: return edgeID
def CreateNewEdge (graphID, senderID, recipientID, data):
    cur = conn.cursor()
    cur.execute("INSERT INTO edges (graph_ID, sender_ID, recipient_ID, email_count) VALUES (%s, %s, %s, %s)", (graphID, senderID, recipientID, data))
    conn.commit()
    cur.close()

def UpdateEdgeData (edgeID, data):
    cur = conn.cursor()
    cur.execute("UPDATE edges SET email_count = %s WHERE id = %s", (data, edgeID))
    conn.commit()
    cur.close()

# def PullMatrixFromDB (graphID):
#     graphID = str(graphID) #Typeerror without this line
#     cur = conn.cursor()
#     cur.execute("SELECT * FROM nodes WHERE graph_ID = %s", (graphID))
#     nodes = cur.fetchall()
#     cur.execute("SELECT * FROM edges WHERE graph_ID = %s", (graphID))
#     edges = cur.fetchall()
#     cur.close()

#     print("Nodes:")
#     for n in nodes: print(n)
#     print("Edges:")
#     for e in edges: print(e)

#     matrix = AdjacencyMatrix()
#     for e in edges: # this is why python is an abomination
#         sender = filter(lambda x : x[0] == e[1], nodes)[0][1]
#         receiver = filter(lambda x : x[0] == e[2], nodes)[0][1]

#         matrix.add(sender, receiver)
#         print(sender, receiver)
#     matrix.write_data_to_textfile()        

def PullListFromDB (graphID):
    graphID = str(graphID) #Typeerror without this line
    cur = conn.cursor()
    cur.execute("SELECT * FROM nodes WHERE graph_ID = %s", (graphID))
    nodes = cur.fetchall()
    cur.execute("SELECT * FROM edges WHERE graph_ID = %s", (graphID))
    edges = cur.fetchall()
    cur.close()

    # print("Nodes:")
    # for n in nodes: print(n)
    # print("Edges:")
    # for e in edges: print(e)

    adjList = AdjacencyList()
    for e in edges:
        senderID = e[1]
        receiverID = e[2]
        senderEmail = filter(lambda n : n[0] == senderID, nodes)[0][1]
        receiverEmail = filter(lambda n : n[0] == receiverID, nodes)[0][1]
        emailCount = e[4]
        shouldIncrement = False

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
            # print("r_key", key)
            # print("r_obj", recipient.emailAddress)
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

    

adjList = PullListFromDB(1)
PushListToDB(1, adjList)