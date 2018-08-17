import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import pyqtgraph as pg

import appController as AppC
import databaseController as DBC

class Application(QTabWidget):
    def __init__(self, parent = None):
        super(Application, self).__init__(parent)
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()

        self.addTab(self.tab1,"Tab 1")
        self.addTab(self.tab2,"Tab 2")
        self.addTab(self.tab3,"Tab 3")
        self.tab1UI()
        self.tab2UI()
        self.tab3UI()
        self.setWindowTitle("FIT3162 Project - Social Network Analysis")

    def tab1UI(self):
        # grid is two columns, graph list and graph view
        layout = QGridLayout()
        layout.setColumnStretch(0, 25)
        layout.setColumnStretch(1, 75)

        listLabel = QLabel("Datasets in Database")
        listWidget = QListWidget()
        loadBtn = QPushButton("Load Graph")
        layout.addWidget(listLabel, 0, 0)
        layout.addWidget(listWidget, 1, 0)
        layout.addWidget(loadBtn, 2, 0)

        graphLabel = QLabel("Graph")
        graph = pg.PlotWidget()
        layout.addWidget(graphLabel, 0, 1)
        layout.addWidget(graph, 1, 1)

        graphs = READ_AllGraphs()
        for g in graphs:
            listWidget.addItem(g[1])

        self.setTabText(0,"View Graphs")
        self.tab1.setLayout(layout)


    def tab2UI(self):
        layout = QFormLayout()

        fileSelectBtn = QPushButton("Click Here to Select a File")
        submitBtn = QPushButton("Submit")

        layout.addRow(QLabel("Import New Graph"))
        layout.addRow(fileSelectBtn)
        layout.addRow(submitBtn)        

        self.setTabText(1,"Import New Graph")
        self.tab2.setLayout(layout)

    def tab3UI(self):
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

def main():
    app = QApplication(sys.argv)
    ex = Application()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()