
import psycopg2

conn = psycopg2.connect("dbname=snagraphs user=eldarhasandwich")

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
    cur.execute("INSERT INTO nodes (email, graph_ID) VALUES ('%s', %s)", (data, graphID))
    conn.commit()
    cur.close()
    
def CreateNewEdge (senderID, recipientID, data):
    pass

def UpdateEdgeData (edgeID, data):
    pass


CreateNewGraph("HELLO")
CreateNewGraph("this is a graph")
RunQuery("SELECT * FROM graphs")