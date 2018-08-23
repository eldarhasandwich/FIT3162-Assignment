import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import pyqtgraph as pg

import appController as AppC
import databaseController as DBC
import enron_output_to_adjlist as enron

class Application(QTabWidget):
    def __init__(self, parent = None):
        super(Application, self).__init__(parent)

        self.selectedGraphId = None
        self.loadedGraphs = {}

        self.graphList = QListWidget()
        self.graphList.itemClicked.connect(self.graphItemClicked)
        self.tab1 = QWidget()
        self.addTab(self.tab1,"Tab 1")
        self.tab1UI()
        ##--

        self.fileSelectionSelectedFileName = ""
        self.fileSelectionSelectedFile = None

        self.fileSelectionDescription = QLabel("default text")
        self.tab2 = QWidget()
        self.addTab(self.tab2,"Tab 2")
        self.tab2UI()
        ##--

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
        self.loadedGraphs[self.selectedGraphId] = adjList
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
        graph = pg.PlotWidget()
        layout.addWidget(graphLabel, 0, 1)
        layout.addWidget(graph, 1, 1)

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
            self.fileSelectionSelectedFile = open(fileName, "r")
            self.fileSelectionSelectedFileName = fileName.split('/')[-1]
            self.fileSelectionDescription.setText(self.fileSelectionSelectedFileName)

    def parseTxtFileIntoDB(self):
        adjList = enron.TxtToAdjList(self.fileSelectionSelectedFile)
        graphId = DBC.CREATE_NewGraph(self.fileSelectionSelectedFileName)
        DBC.PushAdjListToDB(graphId, adjList)
        self.fileSelectionDescription.setText("Select a file first.")
        self.refreshGraphList()

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

        dropdown = QComboBox()
        dropdown.addItems(["something", "something else", "who cares"])

        submitBtn = QPushButton("Run Analysis")

        layout.addRow(QLabel("Run Analysis on Graph"))
        layout.addRow(dropdown)
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