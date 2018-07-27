import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class tabdemo(QTabWidget):
    def __init__(self, parent = None):
        super(tabdemo, self).__init__(parent)
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
        layout = QFormLayout()
        #   layout.addRow("Name",QLineEdit())
        #   layout.addRow("Address",QLineEdit())

        listWidget = QListWidget()
        listWidget.resize(300,120)
        layout.addRow("List", listWidget)

        listWidget.addItem("Ass")
        listWidget.addItem("Ass")
        listWidget.addItem("Ass")
        listWidget.addItem("Ass")
        listWidget.addItem("Ass")
        listWidget.addItem("Ass")

        self.setTabText(0,"View Graphs")
        self.tab1.setLayout(layout)

    def tab2UI(self):
        layout = QFormLayout()
        #   sex = QHBoxLayout()
        #   sex.addWidget(QRadioButton("Male"))
        #   sex.addWidget(QRadioButton("Female"))
        #   layout.addRow(QLabel("Sex"),sex)
        #   layout.addRow("Date of Birth",QLineEdit())

        fileSelectBtn = QPushButton("Click Here to Select a File")
        submitBtn = QPushButton("Submit")

        layout.addRow(QLabel("Import New Graph"))
        layout.addRow(fileSelectBtn)
        layout.addRow(submitBtn)        

        self.setTabText(1,"Import New Graph")
        self.tab2.setLayout(layout)

    def tab3UI(self):
        layout = QFormLayout()
        #   layout.addWidget(QLabel("subjects")) 
        #   layout.addWidget(QCheckBox("Physics"))
        #   layout.addWidget(QCheckBox("Maths"))

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
    ex = tabdemo()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()