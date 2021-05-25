from PyQt5.QtGui import QFont
from PyQt5.QtSql import QSqlQuery, QSqlQueryModel
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from tables.atc.atcChangeDialog import ChangeDialog
from tables.atc.atcInsertDialog import RefactorDialog
from tables.atc.atcLookDialog import LookDialog
from generaton import Generation


class SixteenWidget(QWidget):
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

        self.label3 = QLabel("Выбрать промежуток времени:")
        self.date1 = QDateEdit()
        self.date2 = QDateEdit()

        self.label2 = QLabel("Выбрать географию:")
        self.box1 = QComboBox()
        box1 = ["Городские (по ДНР)", "Международные"]
        self.box1.addItems(box1)

        self.label1 = QLabel("Количество переговоров и стоимость этих переговоров в указанный месяц отдельно по "
                             "городским и по международным звонкам: ")
        self.btn = QPushButton("Вывести")
        self.btn.setFixedWidth(100)
        font = QFont()
        font.setPointSize(12)

        self.label_res = QLabel()
        self.label1.setFont(font)
        self.label_res.setFont(font)

        self.gridlayout.addWidget(self.label1, 0, 0, 1, 8)

        self.gridlayout.addWidget(self.label3, 1, 0)
        self.gridlayout.addWidget(self.date1, 1, 1)
        self.gridlayout.addWidget(self.date2, 1, 2)

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
        date1 = self.date1.text()
        date2 = self.date2.text()
        geograph = self.box1.currentText()
        if geograph == 'Городские (по ДНР)':
            self.query.prepare("""select count(calls.id), sum((calls.duration/60+1)*country.price*tariff.coefficient) as price
                    from calls 
                   join city on calls.id_city = city.id 
                   join country on city.id_country = country.id 
                   join tariff on calls.id_tariff = tariff.id 
                   where country.id = 1 and 
                   calls.date between ? and ?""")
            self.query.addBindValue(date1)
            self.query.addBindValue(date2)
            self.query.exec_()
            while self.query.next():
                self.count = self.query.value(0)
                self.sum = self.query.value(1)
        else:
            self.query.prepare("""select count(calls.id), sum((calls.duration/60+1)*country.price*tariff.coefficient) as price
                                from calls 
                               join city on calls.id_city = city.id 
                               join country on city.id_country = country.id 
                               join tariff on calls.id_tariff = tariff.id 
                               where country.id != 1 and 
                               calls.date between ? and ?""")
            self.query.addBindValue(date1)
            self.query.addBindValue(date2)
            self.query.exec_()
            while self.query.next():
                self.count = self.query.value(0)
                self.sum = self.query.value(1)
        self.label_res.setText(
            "Количество переговоров: " + str(self.count) + "\nСтоимость этих переговоров: " + str(self.sum))
        self.gridlayout.addWidget(self.label_res, 4, 0, 1, 4)











