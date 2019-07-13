import re
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
        self.filename = path
        self.wb = xls.load_workbook(path)
        self.ws = self.wb.active
        self.totalWordNum = self.ws.max_row

    def updateOccursOfWord(self, word):
       self.ws.cell(column=4, row=word.index, value=word.occurs)

    def updateShotsOfWord(self, word):
       self.ws.cell(column=5, row=word.index, value=word.shots)

    def getOneWord(self, row = 1):
        if row is 0:
            wordAttrs = list(self.ws.rows)[0]
        else:
            wordAttrs = list(self.ws.rows)[row - 1]

        word = Word(row,
                    wordAttrs[0].value,     # literal
                    wordAttrs[1].value,     # part of speech
                    wordAttrs[2].value,     # Chinese
                    wordAttrs[3].value,     # occurs
                    wordAttrs[4].value,     # shots
                    wordAttrs[5].value)     # flag

        word.occurs += 1
        self.updateOccursOfWord(word)    # guarantee the consistency of data

        return word
        
class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.lex = Lexicon('words.xlsx') 
        self.wordInd = random.randint(1, self.lex.totalWordNum)
        self.word = self.lex.getOneWord(self.wordInd)

        self.button = QtWidgets.QPushButton("Click me!")

        self.text = QtWidgets.QLabel('<font face="verdana" color="maroon" size="60"><b>'+self.word.liter+'</b></font>')
        self.text.setAlignment(QtCore.Qt.AlignCenter)
        self.text.setWordWrap(True)

        self.chinese = QtWidgets.QLineEdit()
        self.chinese.returnPressed.connect(self.magic)

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.chinese)
        self.layout.addWidget(self.button)
        self.setLayout(self.layout)

        self.button.clicked.connect(self.magic)

    def retrieveWord(self):
        self.wordInd = random.randint(1, self.lex.totalWordNum)    
        self.word = self.lex.getOneWord(self.wordInd)
        self.text.setText('<font face="verdana" color="maroon" size="60"><b>'+self.word.liter+'</b></font>')

    def updateWord(self):
        chineseStr = self.chinese.text()
        if chineseStr == '':
            self.word.occurs -= 1
            self.lex.updateOccursOfWord(self.word)
            return

        if re.search(chineseStr, self.word.chinese, re.X) is not None:
            self.word.shots += 1
            self.lex.updateShotsOfWord(self.word)
            
        self.chinese.clear()

    def magic(self):
        self.updateWord()
        self.lex.wb.save(self.lex.filename)
        self.retrieveWord()

    
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    widget = MyWidget()
    widget.resize(800, 600)
    widget.show()
    
    sys.exit(app.exec_())
