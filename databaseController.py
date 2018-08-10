
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

def CreateNewGraph (newName):
    cur = conn.cursor()
    cur.execute("INSERT INTO graphs (name) VALUES ('" + newName + "');")
    # print(cur.fetchall())
    conn.commit()
    cur.close()

def CreateNewNode (graphID, data):
    cur = conn.cursor()
    cur.execute("INSERT INTO nodes (email, graph_ID) VALUES (%s, %s)", (data, graphID))
    conn.commit()
    cur.close()
    
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

def PullMatrixFromDB (graphID):
    graphID = str(graphID) #Typeerror without this line
    cur = conn.cursor()
    cur.execute("SELECT * FROM nodes WHERE graph_ID = %s", (graphID))
    nodes = cur.fetchall()
    cur.execute("SELECT * FROM edges WHERE graph_ID = %s", (graphID))
    edges = cur.fetchall()
    cur.close()

    print("Nodes:")
    for n in nodes: print(n)
    print("Edges:")
    for e in edges: print(e)

    matrix = AdjacencyMatrix()
    for e in edges: # this is why python is an abomination
        sender = filter(lambda x : x[0] == e[1], nodes)[0][1]
        receiver = filter(lambda x : x[0] == e[2], nodes)[0][1]

        matrix.add(sender, receiver)
        print(sender, receiver)
    matrix.write_data_to_textfile()        

def PullListFromDB (graphID):
    graphID = str(graphID) #Typeerror without this line
    cur = conn.cursor()
    cur.execute("SELECT * FROM nodes WHERE graph_ID = %s", (graphID))
    nodes = cur.fetchall()
    cur.execute("SELECT * FROM edges WHERE graph_ID = %s", (graphID))
    edges = cur.fetchall()
    cur.close()

    print("Nodes:")
    for n in nodes: print(n)
    print("Edges:")
    for e in edges: print(e)

    adjList = AdjacencyList()
    for e in edges:
        sender = filter(lambda x : x[0] == e[1], nodes)[0]
        receiver = filter(lambda x : x[0] == e[2], nodes)[0]

        adjList.AddSenderRecipientPair(e[1], sender[1], e[2], receiver[1])

def PushListToDB (graphID, _AdjacencyList):
    nodeList = {}
    edgeList = {}

    for key, sender in self.senders.items():
        if key not in nodeList:
            nodeList[key] = sender
        else: pass
        for key, recipient in sender.recipients.items():
            if key not in nodeList:
                nodeList[key] = recipient
            else: pass

# CreateNewGraph("HELLO")
# CreateNewGraph("this is a graph")
# CreateNewNode(1, "eldar")
# CreateNewEdge(1, 1, 2, 30)
# RunQuery("SELECT * FROM graphs")
# RunQuery("SELECT * FROM nodes")
# RunQuery("SELECT * FROM edges WHERE graph_ID = 1")
# PullMatrixFromDB(1)
PullListFromDB(1)

# UpdateEdgeData(3, 20)

# PullListFromDB(1)
