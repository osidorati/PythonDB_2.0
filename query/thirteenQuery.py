from PyQt5.QtGui import QFont
from PyQt5.QtSql import QSqlQuery, QSqlQueryModel
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from tables.atc.atcChangeDialog import ChangeDialog
from tables.atc.atcInsertDialog import RefactorDialog
from tables.atc.atcLookDialog import LookDialog
from generaton import Generation


class ThirteenWidget(QWidget):
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

        query = QSqlQuery()
        query.prepare("""select avg((calls.duration/60+1)*country.price*tariff.coefficient) 
                                                FROM calls
                                                INNER JOIN abonents ON calls.id_abonent = abonents.id
                                                INNER JOIN tariff ON calls.id_tariff = tariff.id 
                                                join city on calls.id_city = city.id
                                                join country on country.id = city.id_country""")
        query.exec_()
        while query.next():
            count = query.value(0)

        s = ("SELECT calls.id, abonents.phone_number, calls.telephone_in, date, duration, city.name_city, tariff.coefficient, "
             "(calls.duration/60+1)*country.price*tariff.coefficient as price "
             "FROM calls "
             "INNER JOIN abonents ON calls.id_abonent = abonents.id "
             "INNER JOIN tariff ON calls.id_tariff = tariff.id "
             "join city on calls.id_city = city.id "
             "join country on country.id = city.id_country "
             "where (calls.duration/60+1)*country.price*tariff.coefficient < " +
             "(select avg((calls.duration/60+1)*country.price*tariff.coefficient) "
                                                " FROM calls "
                                                " INNER JOIN abonents ON calls.id_abonent = abonents.id "
                                                " INNER JOIN tariff ON calls.id_tariff = tariff.id "
                                                " join city on calls.id_city = city.id "
                                                " join country on country.id = city.id_country)")
        self.attempt.setQuery(s)

        self.attempt.setHeaderData(0, Qt.Horizontal, "id_????????????")
        self.attempt.setHeaderData(1, Qt.Horizontal, "?????????? ???????????????????? ????????????")
        self.attempt.setHeaderData(2, Qt.Horizontal, "?????????? ?????????????????? ????????????")
        self.attempt.setHeaderData(3, Qt.Horizontal, "????????")
        self.attempt.setHeaderData(4, Qt.Horizontal, "??????????????????????????????????")
        self.attempt.setHeaderData(5, Qt.Horizontal, "??????????")
        self.attempt.setHeaderData(6, Qt.Horizontal, "?????????????????????? ????????????")
        self.attempt.setHeaderData(7, Qt.Horizontal, "???????? ????????????")

        self.label1 = QLabel("?????????? ??????????????, ?? ?????????????? ???????? ???????????? ??????????????: ")
        self.label2 = QLabel("?????????????? ????????: " + str(count))
        font = QFont()
        font.setPointSize(12)
        self.label1.setFont(font)
        self.label2.setFont(font)

        self.gridlayout.addWidget(self.label2, 0, 0, 1, 8)
        self.gridlayout.addWidget(self.label1, 1, 0, 1, 8)
        self.gridlayout.addWidget(self.view, 3, 0, 1, 8)

        self.layout.setGeometry(QRect(441, 212, 173, 154))
        self.layout.addLayout(self.gridlayout)
        self.setLayout(self.layout)
        self.layout.setAlignment(Qt.AlignTop)












