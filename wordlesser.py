import re
import sys
import random
import pandas as pd
from PySide2 import QtCore, QtWidgets, QtGui


class Word:
    def __init__(self, index, liter, part_of_speech, chinese, occurs, shots):
        self.index = index
        self.liter = liter
        self.pos = part_of_speech
        self.chinese = chinese
        self.occurs = occurs
        self.shots = shots


class Lexicon:
    def __init__(self, path):
        self.filename = path
        self.df = pd.read_csv(path)
        self.totalWordNum = self.df.shape[0]
        self.header = ["word", "part_of_speech", "chinese", "occurs", "shots"]

    def save(self):
        self.df.to_csv(self.filename, header=self.header, index=False)

    def update_occurs_of_word(self, word):
        self.df.iloc[word.index, 3] = word.occurs

    def update_shots_of_word(self, word):
        self.df.iloc[word.index, 4] = word.shots

    def get_one_word(self):
        row = random.randint(0, self.totalWordNum - 1)

        word = Word(row,
                    self.df.iloc[row, 0],  # literal
                    self.df.iloc[row, 1],  # part of speech
                    self.df.iloc[row, 2],  # Chinese
                    self.df.iloc[row, 3],  # occurs
                    self.df.iloc[row, 4])  # shots

        word.occurs += 1
        self.update_occurs_of_word(word)  # guarantee the consistency of data

        return word


class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.lex = Lexicon("C:\\Users\\lulu\\PycharmProjects\\wordless\\word.csv")
        self.word = self.lex.get_one_word()

        self.init_ui()

    def closeEvent(self, event: QtGui.QCloseEvent):
        self.lex.save()
        event.accept()

    def init_ui(self):
        self.button = QtWidgets.QPushButton("Click me!")

        self.curWord = QtWidgets.QLabel(
            '<font face="verdana" color="maroon" size="10"><b>' + self.word.liter + '</b></font>')
        self.curWord.setAlignment(QtCore.Qt.AlignCenter)
        self.curWord.setScaledContents(True)

        self.prevWord = QtWidgets.QLabel(self.word.liter + "\n" + self.word.chinese)
        self.prevWord.setAlignment(QtCore.Qt.AlignCenter)
        self.prevWord.setScaledContents(True)

        self.negImage = QtGui.QPixmap("Images/negative.png")
        self.negImage.scaledToHeight(60)
        self.negImage.scaledToWidth(60)

        self.posImage = QtGui.QPixmap("Images/sam.png")
        self.posImage.scaledToHeight(60)
        self.posImage.scaledToWidth(60)

        self.hintImage = QtWidgets.QLabel()
        self.hintImage.setAlignment(QtCore.Qt.AlignCenter)
        self.hintImage.setPixmap(self.negImage)

        self.chinese = QtWidgets.QLineEdit()
        self.chinese.returnPressed.connect(self.magic)

        self.layout = QtWidgets.QGridLayout()
        self.layout.setSpacing(5)
        self.layout.addWidget(self.prevWord, 0, 0, 1, 1)
        self.layout.addWidget(self.curWord, 1, 1, 1, 1)
        self.layout.addWidget(self.hintImage, 2, 1, 1, 1)
        self.layout.addWidget(self.chinese, 3, 1, 1, 1)
        self.layout.addWidget(self.button, 4, 1, 1, 1)
        self.layout.setColumnStretch(0, 1)
        self.layout.setColumnStretch(1, 2)
        self.layout.setColumnStretch(2, 1)
        self.layout.setRowStretch(0, 1)
        self.layout.setRowStretch(1, 2)
        self.layout.setRowStretch(2, 1)
        self.layout.setRowStretch(3, 1)

        self.setLayout(self.layout)

        self.button.clicked.connect(self.magic)

    def refreshPrevWord(self):
        self.prevWord.setText("<font face=verdana size=20><b>" + self.word.liter + "<br /></b></font>"
                              + "<font face=verdana size=20><b>" + self.word.chinese + "</b></font>")

    def retrieveWord(self):
        self.word = self.lex.get_one_word()
        if round(pow(2, self.word.shots / self.word.occurs)) is 2:
            tmp_word = self.lex.get_one_word()
            if self.word == tmp_word:
                pass
            else:
                self.word = self.lex.get_one_word()

        self.curWord.setText(
            '<h6><font face="verdana" color="maroon" size="10"><b>' + self.word.liter + '</b></font></h6>')
        self.hintImage.setPixmap(self.negImage)
        self.hintImage.update()

    def update_word(self):
        self.refreshPrevWord()

        chineseStr = self.chinese.text()
        if chineseStr == '':
            self.word.occurs -= 1
            self.lex.update_occurs_of_word(self.word)
            return

        if re.search(chineseStr, self.word.chinese, re.X) is not None:
            self.word.shots += 1
            self.lex.update_shots_of_word(self.word)
            self.hintImage.setPixmap(self.posImage)
            self.hintImage.update()

        self.chinese.clear()

    def magic(self):
        self.update_word()
        self.retrieveWord()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    widget = MyWidget()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec_())
