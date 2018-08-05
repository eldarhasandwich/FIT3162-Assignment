
import psycopg2

conn = psycopg2.connect("dbname=testsnagraphs user=eldarhasandwich")

def RunQuery (qString):
    cur = conn.cursor()
    cur.execute(qString)
    print(cur.fetchall())
    cur.close()

def CreateNewGraph (newName):
    cur = conn.cursor()
    cur.execute("INSERT INTO graphs (name) VALUES ('" + newName + "');")
    conn.commit()
    cur.close()

def CreateNewNode (graphID, data):
    cur = conn.cursor()
    cur.execute("INSERT INTO nodes (email, graph_ID) VALUES (%s, %s)", (data, graphID))
    conn.commit()
    cur.close()
    
def CreateNewEdge (senderID, recipientID, data):
    cur = conn.cursor()
    cur.execute("INSERT INTO edges (sender_ID, recipient_ID, email_count) VALUES (%s, %s)", (senderID, recipientID, data))
    conn.commit()
    cur.close()

def UpdateEdgeData (edgeID, data):
    pass


CreateNewGraph("HELLO")
CreateNewGraph("this is a graph")
CreateNewNode(1, "eldar")
RunQuery("SELECT * FROM graphs")
RunQuery("SELECT * FROM nodes")
RunQuery("SELECT * FROM edges")