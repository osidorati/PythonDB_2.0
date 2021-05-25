from PyQt5.QtGui import QFont
from PyQt5.QtSql import QSqlQuery, QSqlQueryModel
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from tables.atc.atcChangeDialog import ChangeDialog
from tables.atc.atcInsertDialog import RefactorDialog
from tables.atc.atcLookDialog import LookDialog
from generaton import Generation


class EighteenWidget(QWidget):
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

        self.label1 = QLabel("Социальная категория, которая чаще пользуется услугами АТС: ")
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
            self.query.exec_("""select position.type_positon,
                sum((select count(abonents.id) from abonents where  abonents.id_position = position.id)) as our_count
                from position
                group by position.type_positon
                order by our_count desc limit 1""")
            while self.query.next():
                self.name = self.query.value(0)
                self.count = self.query.value(1)
        else:
            self.query.prepare("""select position.type_positon,
                    (select count(abonents.id) from abonents where abonents.id_atc = atc.id_atc and abonents.id_position 
                    = position.id) as our_count
                    from atc, position
                    where atc.caption = ?
                    order by our_count desc limit 1 """)
            self.query.addBindValue(geograph)
            self.query.exec_()
            while self.query.next():
                self.name = self.query.value(0)
                self.count = self.query.value(1)
        self.label_res.setText("Социальная категория, которая чаще пользуется услугами: " + self.name)
        self.gridlayout.addWidget(self.label_res, 4, 0, 1, 4)











