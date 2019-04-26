# Input file
from tree import *
#from parser import variableNameParsing
from app_ui import Ui_MainWindow
from abc import ABC
from PyQt5 import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
import sys
import re
import os
from PyQt5 import QtGui

from api import create_lookup,Adapter


# program running
def variableNameParsing(txt: str):
    ret = list()
    regex = r"[A-Za-z]+"
    matches = re.finditer(regex, txt, re.MULTILINE)
    for _, match in enumerate(matches, start=1):
        ret.append(match.group())
    ret = set(ret)
    ret = list(ret)
    if len(ret) > 0:
        ret.sort()
    return ret


class Observer(ABC):
    def update(self, data):
        pass

# Observe input table


class ObservableTable(Observer):
    def __init__(self, ui: QtWidgets.QTableWidget, observer):
        self.ui = ui
        self.dict = dict()
        self.lookup = dict()
        self.observerCollection = self.initObservers(observer)

        # connect event
        self.ui.itemChanged.connect(self.updateDict)

    def initObservers(self, observer):
        collection = ObserversCollection()
        collection.registerObserver(observer)
        return collection

    def update(self, data):
        variables = variableNameParsing(data)
        self.ui.setRowCount(len(variables))
        for index, variable in enumerate(variables):
            key = QTableWidgetItem(variable)
            value = QTableWidgetItem(
                self.dict[variable] if variable in self.dict else "0")
            self.ui.setItem(index, 0, key)
            self.ui.setItem(index, 1, value)
        # self.ui.resizeColumnsToContents()
        # self.ui.resizeRowsToContents()
        self.ui.show()

    def updateDict(self, item):
        row = item.row()
        col = item.column()
        if col == 1:
            key = self.ui.item(row, 0).text()
            value = item.text()
            self.dict[key] = value
        
        l = list()
        for k in self.dict:
            l.append((k,self.dict[k]))
        self.lookup = create_lookup(l)
        
        self.observerCollection.notifyObservers(self.lookup)


# Observe treeview


class ObservableView(Observer):
    def __init__(self, ui: QtWidgets):
        self.ui = ui
        self.expr = ""
        self.lookup = dict()

    def update(self, data):
        if type(data) is str:
            self.expr = data
        else:
            self.lookup = data
        try:   
            plt = Adapter(self.expr,self.lookup).draw()
            plt.savefig("tmp.jpg")
            self.ui.setPixmap(QtGui.QPixmap(os.getcwd() + '/tmp.jpg'))
            self.ui.show()
            #fig, ax = plt.subplots()
            # self.tmp = FigureCanvas(plt)
            # lay = QtWidgets.QVBoxLayout(self.ui)  
            # lay.setContentsMargins(0, 0, 0, 0)      
            # lay.addWidget(self.tmp)
            # lay.show()
        except Exception:
            pass

class ObserversCollection:
    def __init__(self):
        self.collection = list()  # list of observer

    def registerObserver(self, obj: Observer):
        return self.collection.append(obj)

    def unregisterObserver(self, index: int):
        return self.collection.remove(index)  # not running but we assume

    def notifyObservers(self, data):  # trigger when event
        for observer in self.collection:
            observer.update(data)
        return


class Application:
    def __init__(self, tree: Tensor):
        # can recompile this without changing the code. Can apply Adapter
        self.app = QtWidgets.QApplication(sys.argv)
        self.MainWindow = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.MainWindow)

        # Setup data
        self.observerCollection = self.initObservers()
        self.tree = tree

        # setup connect
        self.ui.textEdit.textChanged.connect(self.inputChange)
        #self.ui.pushButton.clicked.connect(self.plot)

    def initObservers(self):
        collection = ObserversCollection()
        view = ObservableView(self.ui.label_4)
        collection.registerObserver(ObservableTable(self.ui.tableWidget, view))
        collection.registerObserver(view)
        return collection

    def inputChange(self, *args):  # trigger when textinput data changed
        # parse new Tree
        # self.tree = "abc"
        # notify
        self.tree = self.ui.textEdit.toPlainText()
        self.observerCollection.notifyObservers(self.tree)

    def display(self):
        self.MainWindow.show()
        sys.exit(self.app.exec_())

    def plot(self,*args):
        pass

# class PrettyWidget(QtGui.QWidget):

#     def __init__(self, parent=None):
#         QtGui.QWidget.__init__(self, parent=parent)
#         self.initUI()

#     def initUI(self):
#         self.resize(1000,600)
#         self.center()
#         self.setWindowTitle('Browser')

#         self.lb = QtGui.QLabel(self)
#         pixmap = QtGui.QPixmap("tmp.jpg")
#         height_of_label = 100
#         self.lb.resize(self.width(), height_of_label)
#         self.lb.setPixmap(pixmap.scaled(self.lb.size(), QtCore.Qt.IgnoreAspectRatio))
#         self.show()    

#     def resizeEvent(self, event):
#         self.lb.resize(self.width(), self.lb.height())
#         self.lb.setPixmap(self.lb.pixmap().scaled(self.lb.size(), QtCore.Qt.IgnoreAspectRatio))
#         QtGui.QWidget.resizeEvent(self, event)


#     def center(self):
#         qr = self.frameGeometry()
#         cp = QtGui.QDesktopWidget().availableGeometry().center()
#         qr.moveCenter(cp)
#         self.move(qr.topLeft())

if __name__ == "__main__":
    # Setup UI
    App = Application("")
    App.display()
