import sys
import random
import openpyxl as xls
from PySide2 import QtCore,QtWidgets,QtGui


class Word:
    def __init__(self, index, liter, partOfSpeech, chinese, occurs, shots, flag):
        self.index   = index
        self.liter   = liter
        self.pospch  = partOfSpeech
        self.chinese = chinese
        self.occurs  = occurs
        self.shots   = shots
        self.flag    = flag

class Lexicon:
    def __init__(self, path):
        self.wb = xls.load_workbook(path)
        self.ws = self.wb.active
        self.totalWordNum = self.ws.max_row

    def getOneWord(self, row = 1):
        if row is 0:
            wordAttrs = list(self.ws.rows)[0]
        else:
            wordAttrs = list(self.ws.rows)[row - 1]

        return Word(row,
                    wordAttrs[0].value,
                    wordAttrs[1].value,
                    wordAttrs[2].value,
                    wordAttrs[3].value,
                    wordAttrs[4].value,
                    wordAttrs[5].value)
        
        
class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.lex = Lexicon('words.xlsx') 

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
        index = random.randint(1, self.lex.totalWordNum)    
        self.text.setText('<font face="verdana" color="maroon" size="60"><b>'+self.lex.getOneWord(index).liter+'</b></font>')

    
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    widget = MyWidget()
    widget.resize(800, 600)
    widget.show()
    
    sys.exit(app.exec_())
