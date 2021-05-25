from PyQt5.QtGui import QFont
from PyQt5.QtSql import QSqlQuery, QSqlQueryModel
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from tables.atc.atcChangeDialog import ChangeDialog
from tables.atc.atcInsertDialog import RefactorDialog
from tables.atc.atcLookDialog import LookDialog
from generaton import Generation


class FifteenWidget(QWidget):
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
        self.view.setModel(self.attempt)
        self.view.resizeColumnsToContents()
        self.view.setFixedWidth(1400)

        self.attempt.setQuery("""SELECT atc.id_atc, atc.caption, country.name_country,
                        (select count(calls.id) from calls 
                            where calls.id_city in (select city.id from city where city.id_country = country.id) and
                            calls.id_abonent in (select abonents.id from abonents where abonents.id_atc = atc.id_atc))
                        from atc, country
                        group by atc.id_atc, atc.caption, country.name_country, country.id
                        order by atc.id_atc""")

        self.attempt.setHeaderData(0, Qt.Horizontal, "id_атс")
        self.attempt.setHeaderData(1, Qt.Horizontal, "Название АТС")
        self.attempt.setHeaderData(2, Qt.Horizontal, "Название страны")
        self.attempt.setHeaderData(3, Qt.Horizontal, "Количество звонков")

        self.view.resizeColumnsToContents()

        self.label1 = QLabel("Вывод количества звонков в определенной стране через определенную АТС: ")

        font = QFont()
        font.setPointSize(12)
        self.label1.setFont(font)

        self.gridlayout.addWidget(self.label1, 1, 0, 1, 8)
        self.gridlayout.addWidget(self.view, 3, 0, 1, 8)

        self.layout.setGeometry(QRect(441, 212, 173, 154))
        self.layout.addLayout(self.gridlayout)
        self.setLayout(self.layout)
        self.layout.setAlignment(Qt.AlignTop)












