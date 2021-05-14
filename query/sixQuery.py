from PyQt5.QtGui import QFont
from PyQt5.QtSql import QSqlQuery, QSqlQueryModel
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from tables.atc.atcChangeDialog import ChangeDialog
from tables.atc.atcInsertDialog import RefactorDialog
from tables.atc.atcLookDialog import LookDialog
from generaton import Generation


class SixWidget(QWidget):
    customerAddedSignal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.centralwidget = QWidget()
        self.centralwidget.setObjectName(u"centralwidget")
        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(441, 212, 173, 154))
        self.layout = QVBoxLayout()
        self.gridlayout = QGridLayout()
        self.attempt = QSqlQueryModel(self)
        self.attempt.setQuery("""SELECT abonents.id, abonents.surname, abonents.name, abonents.middlename, benefit.type, abonents.document
                                from benefit
                                right join abonents on benefit.id = abonents.id_benefit and benefit.id = 2""")

        self.attempt.setHeaderData(0, Qt.Horizontal, "id_абонента")
        self.attempt.setHeaderData(1, Qt.Horizontal, "Фамилия")
        self.attempt.setHeaderData(2, Qt.Horizontal, "Имя")
        self.attempt.setHeaderData(3, Qt.Horizontal, "Отчество")
        self.attempt.setHeaderData(4, Qt.Horizontal, "Льгота")
        self.attempt.setHeaderData(5, Qt.Horizontal, "Документ на льготу")

        self.view = QTableView()
        self.view.setModel(self.attempt)
        self.view.resizeColumnsToContents()
        self.view.setFixedWidth(1400)

        self.label1 = QLabel("Вывод льгот ветеранов :")
        font = QFont()
        font.setPointSize(12)
        self.label1.setFont(font)
        self.label_count = QLabel("Количество записей: ")
        query = QSqlQuery()
        query.prepare("""select count(*) from abonents""")
        query.exec_()
        while query.next():
            count = query.value(0)
        self.label_count.setText("Количество записей: " + str(count))

        self.label_count.setFont(font)
        self.gridlayout.addWidget(self.label1, 0, 2, 1, 8)
        self.gridlayout.addWidget(self.label_count, 2, 0)
        self.gridlayout.addWidget(self.view, 3, 0, 1, 8)

        self.layout.setGeometry(QRect(441, 212, 173, 154))
        self.layout.addLayout(self.gridlayout)
        self.setLayout(self.layout)
        self.layout.setAlignment(Qt.AlignTop)











