
import psycopg2
from classes.AdjacencyMatrix import *
from classes.AdjacencyList import *

conn = psycopg2.connect("dbname=testsnagraphs user=eldarhasandwich")

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
    pass

# CreateNewGraph("HELLO")
# CreateNewGraph("this is a graph")
# CreateNewNode(1, "eldar")
# CreateNewEdge(1, 1, 2, 30)
# RunQuery("SELECT * FROM graphs")
# RunQuery("SELECT * FROM nodes")
# RunQuery("SELECT * FROM edges WHERE graph_ID = 1")

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



PullMatrixFromDB(1)