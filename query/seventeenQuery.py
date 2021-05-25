from PyQt5.QtGui import QFont
from PyQt5.QtSql import QSqlQuery, QSqlQueryModel
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from tables.atc.atcChangeDialog import ChangeDialog
from tables.atc.atcInsertDialog import RefactorDialog
from tables.atc.atcLookDialog import LookDialog
from generaton import Generation


class SeventeenWidget(QWidget):
    customerAddedSignal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.query = QSqlQuery()
        self.centralwidget = QWidget()
        self.centralwidget.setObjectName(u"centralwidget")
        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(441, 212, 173, 154))
        self.layout = QVBoxLayout()
        self.gridlayout = QGridLayout()
        self.attempt = QSqlQueryModel(self)

        self.view = QTableView()
        self.view.resizeColumnsToContents()
        self.view.setFixedWidth(1400)

        self.label2 = QLabel("Выбрать АТС:")

        self.box1 = QComboBox()
        box1 = ['По городу в целом']
        self.query.exec("""SELECT caption FROM atc""")
        while self.query.next():
            box1.append(self.query.value(0))
        self.box1.addItems(box1)

        self.label1 = QLabel("Среднее время разговора по каждой АТС: ")
        self.btn = QPushButton("Вывести")
        self.btn.setFixedWidth(100)
        font = QFont()
        font.setPointSize(12)

        self.label_res = QLabel()
        self.label1.setFont(font)
        self.label_res.setFont(font)

        self.gridlayout.addWidget(self.label1, 0, 0, 1, 8)

        self.gridlayout.addWidget(self.label2, 2, 0)
        self.gridlayout.addWidget(self.box1, 2, 1)

        self.gridlayout.addWidget(self.btn, 3, 1, 1, 3)
        # self.gridlayout.addWidget(self.view, 3, 0, 1, 8)

        self.layout.setGeometry(QRect(441, 212, 173, 154))
        self.layout.addLayout(self.gridlayout)
        self.setLayout(self.layout)
        self.layout.setAlignment(Qt.AlignTop)

        self.btn.clicked.connect(self.update)

    def update(self):
        geograph = self.box1.currentText()
        self.count = 0
        if geograph == 'По городу в целом':
            self.query.exec_("""select avg(calls.duration) from calls
            join abonents on calls.id_abonent = abonents.id
            join atc on abonents.id_atc = atc.id_atc""")
            while self.query.next():
                self.count = self.query.value(0)
        else:
            self.query.prepare("""select avg(calls.duration) from calls
                        join abonents on calls.id_abonent = abonents.id
                        join atc on abonents.id_atc = atc.id_atc
                        where atc.caption = ?""")
            self.query.addBindValue(geograph)
            self.query.exec_()
            while self.query.next():
                self.count = self.query.value(0)
        self.label_res.setText("Среднее время разговора: " + str(self.count))
        self.gridlayout.addWidget(self.label_res, 4, 0, 1, 4)











