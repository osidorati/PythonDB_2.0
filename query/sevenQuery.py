from PyQt5.QtGui import QFont
from PyQt5.QtSql import QSqlQuery, QSqlQueryModel
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class SevenWidget(QWidget):
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
        self.attempt.setQuery("""SELECT abonents.id, abonents.surname, abonents.name, abonents.middlename, benefit.type, 
                                (select sum((calls.duration/60+1)*country.price*tariff.coefficient) FROM calls 
                                     join city on calls.id_city = city.id
                                     join country on country.id = city.id_country
                                     join tariff on calls.id_tariff = tariff.id   
                                     WHERE calls.id_abonent = abonents.id),
                                (select sum((calls.duration/60+1)*country.price*tariff.coefficient*benefit.tarriff) FROM calls 
                                     join city on calls.id_city = city.id
                                     join country on country.id = city.id_country
                                     join tariff on calls.id_tariff = tariff.id
                                     left join benefit on abonents.id_benefit = benefit.id
                                     WHERE calls.id_abonent = abonents.id)
                                from abonents left join benefit on abonents.id_benefit = benefit.id order by abonents.id""")

        self.attempt.setHeaderData(0, Qt.Horizontal, "id_абонента")
        self.attempt.setHeaderData(1, Qt.Horizontal, "Фамилия")
        self.attempt.setHeaderData(2, Qt.Horizontal, "Имя")
        self.attempt.setHeaderData(3, Qt.Horizontal, "Отчество")
        self.attempt.setHeaderData(4, Qt.Horizontal, "Льгота")
        self.attempt.setHeaderData(5, Qt.Horizontal, "Цена звонков")
        self.attempt.setHeaderData(6, Qt.Horizontal, "Цена звонков с учетом льготы")

        self.view = QTableView()
        self.view.setModel(self.attempt)
        self.view.resizeColumnsToContents()
        self.view.setFixedWidth(1400)

        self.label1 = QLabel("Цена звонков с учетом льготы и без :")
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











