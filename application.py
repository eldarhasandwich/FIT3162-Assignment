import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import networkx as nx

import pyqtgraph as pg

import appController as AppC
import databaseController as DBC
import enron_output_to_adjlist as enron
import graph_statistics as GS

class Application(QTabWidget):
    def __init__(self, parent = None):
        super(Application, self).__init__(parent)

        self.selectedGraphId = None
        self.loadedGraphs = {}
        self.loadedGraphsStats = {}

        self.graphList = QListWidget()
        self.graphList.itemClicked.connect(self.graphItemClicked)
        self.tab1 = QWidget()
        self.addTab(self.tab1,"Tab 1")
        self.tab1UI()
        ##--

        self.fileCanBeParsed = False
        self.fileSelectionSelectedFileName = ""
        self.fileSelectionSelectedFile = None

        self.fileSelectionDescription = QLabel("default text")
        self.tab2 = QWidget()
        self.addTab(self.tab2,"Tab 2")
        self.tab2UI()
        ##--

        self.dropdownItems = []
        self.statDropdown = QComboBox()

        self.tab3 = QWidget()
        self.addTab(self.tab3,"Tab 3")
        self.tab3UI()
        ##--

        self.setWindowTitle("FIT3162 Project - Social Network Analysis")
    ###-----

    def refreshGraphList(self):
        graphs = DBC.READ_AllGraphs()
        self.graphList.clear()
        for g in graphs:
            self.graphList.addItem(str(g[0]) + ") " + g[1])

    def graphItemClicked(self, item):
        print('clicked on graph item')
        gId = item.text().split(') ')[0]
        print("graphId =", gId)
        self.selectedGraphId = gId

    def loadSelectedGraph(self):
        if self.selectedGraphId == None: return
        adjList = DBC.PullListFromDB(self.selectedGraphId)
        graphStat = GS.GraphStatistics()
        graphStat.import_adjacency_list(adjList)

        self.loadedGraphs[self.selectedGraphId] = adjList
        self.loadedGraphsStats[self.selectedGraphId] = graphStat

        self.dropdownItems = graphStat.GetAllStatisticalMethods()
        for i in range(len(self.dropdownItems)):
            self.dropdownItems[i] = self.dropdownItems[i][1]
        self.statDropdown.clear()
        self.statDropdown.addItems(self.dropdownItems)

        print("list loading complete")

    def tab1UI(self): # graph display
        # grid is two columns, graph list and graph view
        layout = QGridLayout()
        layout.setColumnStretch(0, 25)
        layout.setColumnStretch(1, 75)

        listLabel = QLabel("Datasets in Database")
        loadBtn = QPushButton("Load Graph")
        loadBtn.clicked.connect(self.loadSelectedGraph)

        layout.addWidget(listLabel, 0, 0)
        layout.addWidget(self.graphList, 1, 0)
        layout.addWidget(loadBtn, 2, 0)

        graphLabel = QLabel("Graph")
        # graph = nx.DiGraph()
        layout.addWidget(graphLabel, 0, 1)
        # layout.addWidget(graph, 1, 1)
        toFileBtn = QPushButton("Save to Output.txt")
        toFileBtn.clicked.connect(self.adjListToOutputFile)
        layout.addWidget(toFileBtn, 1, 1)

        self.refreshGraphList()

        self.setTabText(0,"View Graphs")
        self.tab1.setLayout(layout)
    ###-----

    def openFileNameDialog(self):    
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            print(fileName)
            f = open(fileName, 'r')
            print(f)
            self.fileSelectionSelectedFile = f.read()
            f.close()
            self.fileSelectionSelectedFileName = fileName.split('/')[-1]
            msg, isValid = enron.EnronOutputIsValid(self.fileSelectionSelectedFile)
            self.fileSelectionDescription.setText(self.fileSelectionSelectedFileName + ": " + msg)
            self.fileCanBeParsed = isValid

    def parseTxtFileIntoDB(self):
        if not self.fileCanBeParsed:
            return
        adjList = enron.TxtToAdjList(self.fileSelectionSelectedFile)
        graphId = DBC.CREATE_NewGraph(self.fileSelectionSelectedFileName)
        DBC.PushAdjListToDB(graphId, adjList)
        self.fileSelectionDescription.setText("Select a file first.")
        self.refreshGraphList()
        self.fileCanBeParsed = False

    def adjListToOutputFile(self):
        if self.selectedGraphId not in self.loadedGraphs:
            return
        outputAdjlist = self.loadedGraphs[self.selectedGraphId]
        f = open('output.txt', 'w') 
        outputNodes = {}
        outputEdges = []
        for skey, sender in outputAdjlist.senders.items():
            if sender.id not in outputNodes:
                outputNodes[sender.id] = sender.emailAddress
            for rkey2, recipient in sender.recipients.items():
                
                if recipient.id in outputNodes:
                    outputEdges.append(str(sender.id) + " " + str(recipient.id) + " " + str(recipient.emailCount))
        f.write('NODES\n')
        for key, node in outputNodes.items():
            f.write(str(key) + ' ' + str(node) + '\n')
        f.write('EDGES\n')
        for line in outputEdges:
            f.write(line + '\n')
        f.close()

    def tab2UI(self): # file selection
        layout = QFormLayout()

        fileSelectBtn = QPushButton("Click Here to Select a File")
        fileSelectBtn.clicked.connect(self.openFileNameDialog)

        submitBtn = QPushButton("Submit")
        submitBtn.clicked.connect(self.parseTxtFileIntoDB)

        self.fileSelectionDescription.setText("Select a file first.")

        layout.addRow(QLabel("Import New Graph"))
        layout.addRow(fileSelectBtn)
        layout.addRow(self.fileSelectionDescription)
        layout.addRow(submitBtn)

        self.setTabText(1,"Import New Graph")
        self.tab2.setLayout(layout)
    ###-----

    def tab3UI(self): # analysis selection 
        layout = QFormLayout()

        # dropdown = QComboBox()
        # dropdown.addItems(["something", "something else", "who cares"])

        submitBtn = QPushButton("Run Analysis")

        layout.addRow(QLabel("Run Analysis on Graph"))
        layout.addRow(self.statDropdown)
        layout.addRow(QLabel("This analysis blah blah blah"))
        layout.addRow(submitBtn)  

        self.setTabText(2,"Run Analysis")
        self.tab3.setLayout(layout)
    ###-----

def main():
    app = QApplication(sys.argv)
    ex = Application()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()