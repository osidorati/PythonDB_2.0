from PyQt5.QtGui import QFont
from PyQt5.QtSql import QSqlQuery, QSqlQueryModel
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from tables.atc.atcChangeDialog import ChangeDialog
from tables.atc.atcInsertDialog import RefactorDialog
from tables.atc.atcLookDialog import LookDialog
from generaton import Generation


class ElevenWidget(QWidget):
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
        self.attempt.setQuery("""select atc.id_atc, atc.caption, district.name_district, count(abonents.id)
                    from atc
                    right join abonents on abonents.id_atc = atc.id_atc
                    inner join district on atc.id_district = district.id
                    group by atc.id_atc, district.name_district order by atc.id_atc
                    """)

        self.attempt.setHeaderData(0, Qt.Horizontal, "id_атс")
        self.attempt.setHeaderData(1, Qt.Horizontal, "Название АТС")
        self.attempt.setHeaderData(2, Qt.Horizontal, "Район")
        self.attempt.setHeaderData(3, Qt.Horizontal, "Количество абонентов")

        self.view = QTableView()
        self.view.setModel(self.attempt)
        self.view.resizeColumnsToContents()
        self.view.setFixedWidth(1400)

        self.label1 = QLabel("Вывод АТС по районам и количество их абонентов: ")
        font = QFont()
        font.setPointSize(12)
        self.label1.setFont(font)
        self.label_count = QLabel("Количество записей: ")
        query = QSqlQuery()
        query.prepare("""select count(*) from atc""")
        query.exec_()
        while query.next():
            count = query.value(0)
        self.label_count.setText("Количество записей: " + str(count))

        self.abonent = QComboBox()
        abonent = []
        self.query.exec("""SELECT name_district FROM district""")
        while self.query.next():
            name = self.query.value(0)
            abonent.append(name)
        self.abonent.addItems(abonent)

        self.btn = QPushButton("Вывести")

        self.label_count.setFont(font)
        self.gridlayout.addWidget(self.label1, 0, 0, 1, 8)
        self.gridlayout.addWidget(self.abonent, 1, 0)
        self.gridlayout.addWidget(self.btn, 1, 1)
        self.gridlayout.addWidget(self.view, 3, 0, 1, 8)

        self.layout.setGeometry(QRect(441, 212, 173, 154))
        self.layout.addLayout(self.gridlayout)
        self.setLayout(self.layout)
        self.layout.setAlignment(Qt.AlignTop)

        self.btn.clicked.connect(self.update)

    def update(self):
        abonent = self.abonent.currentText()


        self.query.prepare("""SELECT id FROM district
                                    WHERE name_district = ?;""")
        self.query.addBindValue(abonent)
        self.query.exec_()
        while self.query.next():
            abonent_id = self.query.value(0)

        s = ("select atc.id_atc, atc.caption, district.name_district, count(abonents.id) "
            "from atc "
            "right join abonents on abonents.id_atc = atc.id_atc "
            "inner join district on atc.id_district = district.id "
            "where district.id = " + str(abonent_id) +
            " group by atc.id_atc, district.name_district order by atc.id_atc ")
        self.attempt.setQuery(s)

        self.attempt.setHeaderData(0, Qt.Horizontal, "id_атс")
        self.attempt.setHeaderData(1, Qt.Horizontal, "Название АТС")
        self.attempt.setHeaderData(2, Qt.Horizontal, "Район")
        self.attempt.setHeaderData(3, Qt.Horizontal, "Количество абонентов")











