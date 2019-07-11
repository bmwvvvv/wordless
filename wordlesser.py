import sys
import random
import openpyxl as xls
from PySide2 import QtCore,QtWidgets,QtGui

class Words:
    def __init__(self, path):
        self.wb = xls.load_workbook(path)
        self.ws = self.wb.active

    def getCol(self, col):
        return list(map(lambda cell: cell.value, self.ws[col]))
        
        
class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.words = Words('words.xlsx') 

        self.hello = ["aaa", "bbb", "ccc", "ddd"]

        self.button = QtWidgets.QPushButton("Click me!")

        self.text = QtWidgets.QLabel("Hello World")
        self.text.setAlignment(QtCore.Qt.AlignCenter)
        self.text.setWordWrap(True)

        self.chinese = QtWidgets.QLineEdit("guess what")

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.chinese)
        self.layout.addWidget(self.button)
        self.setLayout(self.layout)

        self.button.clicked.connect(self.magic)

    def magic(self):
        self.text.setText('<font face="verdana" color="maroon" size="60"><b>'+random.choice(self.words.getCol('A'))+'</b></font>')

    
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    widget = MyWidget()
    widget.resize(800, 600)
    widget.show()
    
    sys.exit(app.exec_())
