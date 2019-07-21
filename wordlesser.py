import re
import sys
import random
import pandas as pd
from datetime import datetime as dt
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
        self.prev_word = Word(-1, "", -1, "", 0, 0)
        self.cur_word = self.lex.get_one_word()

        self.prevWordEn = QtWidgets.QLabel(self.str2html('Ready? Go'))
        self.prevWordEn.setAlignment(QtCore.Qt.AlignCenter)
        # self.prevWordEn.setScaledContents(True)

        self.prevWordCnStdAns = QtWidgets.QLabel(self.str2html('Standard Answer:', 'Arial', 'black', 3))
        self.prevWordCnStdAns.setAlignment(QtCore.Qt.AlignLeft)

        self.prevWordCnStd = QtWidgets.QLabel()
        self.prevWordCnStd.setAlignment(QtCore.Qt.AlignCenter)
        # self.prevWordCnStd.setScaledContents(True)

        self.prevWordCnYouAns = QtWidgets.QLabel(self.str2html('Your Answer:', 'Arial', 'black', 3))
        self.prevWordCnYouAns.setAlignment(QtCore.Qt.AlignLeft)

        self.prevWordCnAns = QtWidgets.QLabel()
        self.prevWordCnAns.setAlignment(QtCore.Qt.AlignCenter)
        # self.prevWordCnAns.setScaledContents(True)

        self.negImage = QtGui.QPixmap("images/negative.png")
        self.negImage.scaledToHeight(60)
        self.negImage.scaledToWidth(60)

        self.posImage = QtGui.QPixmap("images/sam.png")
        self.posImage.scaledToHeight(60)
        self.posImage.scaledToWidth(60)

        self.prevWordCnRes = QtWidgets.QLabel()
        self.prevWordCnRes.setAlignment(QtCore.Qt.AlignCenter)

        self.countdown = QtWidgets.QLabel(self.str2html('Days in 2020 NEEP', 'Arial', 'black', 6))
        self.countdown.setAlignment(QtCore.Qt.AlignCenter)

        self.countdownLcd = QtWidgets.QLCDNumber()
        self.countdownLcd.setSegmentStyle(QtWidgets.QLCDNumber.Filled)
        self.countdownLcd.setStyleSheet("border:2px solid red;color:red;background:silver;")
        self.countdownLcd.display(self.get_countdown_to_neep())

        self.curWordEn = QtWidgets.QLabel(self.str2html(self.cur_word.liter))
        self.curWordEn.setAlignment(QtCore.Qt.AlignCenter)
        # self.curWordEn.setScaledContents(True)
        self.curWordCn = QtWidgets.QLineEdit()
        self.curWordCn.returnPressed.connect(self.magic)

        self.layout = QtWidgets.QGridLayout()
        # self.layout.setSpacing(10)
        self.layout.addWidget(self.prevWordEn, 0, 0)
        self.layout.addWidget(self.prevWordCnStdAns, 1, 0)
        self.layout.addWidget(self.prevWordCnStd, 2, 0)
        self.layout.addWidget(self.prevWordCnYouAns, 3, 0)
        self.layout.addWidget(self.prevWordCnAns, 4, 0)
        self.layout.addWidget(self.prevWordCnRes, 5, 0)

        self.layout.addWidget(self.countdown, 0, 1)
        self.layout.addWidget(self.countdownLcd, 1, 1)
        self.layout.addWidget(self.curWordEn, 3, 1)
        self.layout.addWidget(self.curWordCn, 4, 1)
        self.layout.setColumnStretch(0, 1)
        self.layout.setColumnStretch(1, 1)
        self.layout.setRowStretch(0, 1)
        self.layout.setRowStretch(1, 1)
        self.layout.setRowStretch(2, 1)
        self.layout.setRowStretch(3, 1)
        self.layout.setRowStretch(4, 1)
        self.layout.setRowStretch(5, 1)

        self.setLayout(self.layout)

    @staticmethod
    def str2html(s, font='verdana', color='maroon', sz=10):
        return '<font face=%s color=%s size=%d><b>%s</b></font>' % (font, color, sz, s)

    @staticmethod
    def get_countdown_to_neep():
        neep_date = dt.strptime('2019-12-25 00:00:00', '%Y-%m-%d %H:%M:%S')
        now = dt.now()

        return (neep_date - now).days

    def closeEvent(self, event: QtGui.QCloseEvent):
        self.lex.save()
        event.accept()

    def refresh(self, ans_res):
        self.prevWordEn.setText(self.str2html(self.prev_word.liter))
        self.prevWordCnStd.setText(self.str2html(self.prev_word.chinese, 'KaiTi'))

        if ans_res[1] is True:
            self.prevWordCnAns.setText(self.str2html(ans_res[0], 'KaiTi'))
            self.prevWordCnRes.setPixmap(self.posImage)
        else:
            self.prevWordCnAns.setText(self.str2html(ans_res[0], 'KaiTi', 'red'))
            self.prevWordCnRes.setPixmap(self.negImage)

        self.prevWordCnRes.update()

        self.curWordEn.setText(self.str2html(self.cur_word.liter))
        self.curWordCn.clear()

    def retrieve(self):
        self.cur_word = self.lex.get_one_word()
        if round(pow(2, self.cur_word.shots / self.cur_word.occurs)) is 2:
            tmp_word = self.lex.get_one_word()
            if self.cur_word == tmp_word:
                pass
            else:
                self.cur_word = self.lex.get_one_word()

    def update(self):
        res = False
        ans = self.curWordCn.text()
        if ans == '':
            self.cur_word.occurs -= 1
            self.lex.update_occurs_of_word(self.cur_word)
        elif re.search(ans, self.cur_word.chinese, re.X) is not None:
            self.cur_word.shots += 1
            self.lex.update_shots_of_word(self.cur_word)
            res = True

        self.prev_word = self.cur_word

        return ans, res

    def magic(self):
        res = self.update()
        self.retrieve()
        self.refresh(res)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    widget = MyWidget()
    widget.setWindowTitle('Warlbowo')
    widget.resize(950, 780)
    widget.show()

    sys.exit(app.exec_())
