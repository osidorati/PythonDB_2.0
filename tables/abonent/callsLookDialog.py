from PyQt5.QtGui import QFont
from PyQt5.QtSql import QSqlTableModel, QSqlDatabase, QSqlQuery, QSqlQueryModel
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from tables.abonent.callsInsertDialog import RefactorDialog


class LookDialog(QDialog):
    customerAddedSignal = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.query = QSqlQuery()
        self.setWindowTitle("Просмотр сведений об абоненте")
        self.centralwidget = QWidget()
        self.centralwidget.setObjectName(u"centralwidget")
        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(441, 212, 173, 154))
        self.layout = QVBoxLayout()
        self.gridlayout = QGridLayout()
        self.model = QSqlQueryModel(self)

        self.atc = QLineEdit()
        self.surname = QLineEdit()
        self.name = QLineEdit()
        self.middlename = QLineEdit()
        self.number = QLineEdit()
        self.address = QLineEdit()
        self.position = QLineEdit()
        self.benefit = QLineEdit()
        self.label1 = QLabel("Фамилия:")
        self.label2 = QLabel("Имя:")
        self.label3 = QLabel("Отчество:")
        self.label4 = QLabel("АТС:")
        self.label5 = QLabel("Номер телефона:")
        self.label6 = QLabel("Адрес:")
        self.label7 = QLabel("Социальное положение:")
        self.label8 = QLabel("Льгота:")
        self.label9 = QLabel("Документ на льготу:")
        self.label10 = QLabel("Звонки данного абонента:")
        self.label_count = QLabel("Количество звонков: ")
        self.label_calls = QLabel("Сумма звонков:")
        self.label11 = QLabel("Вывести звонки за даты:")
        self.date1 = QDateEdit()
        self.date2 = QDateEdit()
        self.date_push = QPushButton("Вывести")

        self.date2.setFixedWidth(100)
        self.date1.setFixedWidth(100)
        self.date_push.setFixedWidth(100)

        font = QFont()
        font.setPointSize(10)
        self.label10.setFont(font)
        self.label_count.setFont(font)
        self.label_calls.setFont(font)
        self.label11.setFont(font)
        self.insert_btn = QPushButton("Добавить звонок")
        self.insert_btn.setFixedWidth(150)
        self.cancel_btn = QPushButton("Cancel")

        self.surname = QLineEdit()
        self.name = QLineEdit()
        self.middlename = QLineEdit()
        self.address = QLineEdit()
        self.number = QLineEdit()
        self.atc.setReadOnly(True)
        self.surname.setReadOnly(True)
        self.name.setReadOnly(True)
        self.middlename.setReadOnly(True)
        self.number.setReadOnly(True)
        self.address.setReadOnly(True)
        self.position.setReadOnly(True)
        self.benefit.setReadOnly(True)

        self.view = QTableView()
        self.view.setModel(self.model)
        self.view.resizeColumnsToContents()
        self.view.setFixedWidth(850)
        self.view.setFixedHeight(400)

        self.buttonsBox = QDialogButtonBox(self)
        self.buttonsBox.setOrientation(Qt.Horizontal)
        self.buttonsBox.setStandardButtons(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        self.gridlayout.addWidget(self.label4, 1, 0)
        self.gridlayout.addWidget(self.label1, 2, 0)
        self.gridlayout.addWidget(self.label2, 3, 0)
        self.gridlayout.addWidget(self.label3, 4, 0)
        self.gridlayout.addWidget(self.label5, 5, 0)
        self.gridlayout.addWidget(self.label6, 6, 0)
        self.gridlayout.addWidget(self.label7, 7, 0)
        self.gridlayout.addWidget(self.label8, 8, 0)
        self.gridlayout.addWidget(self.label9, 9, 0)
        self.gridlayout.addWidget(self.label_count, 13, 0)
        self.gridlayout.addWidget(self.insert_btn, 13, 4)

        self.gridlayout.addWidget(self.label11, 11, 0)
        self.gridlayout.addWidget(self.date1, 11, 1)
        self.gridlayout.addWidget(self.date2, 11, 2)
        self.gridlayout.addWidget(self.date_push, 11, 4)

        self.gridlayout.addWidget(self.view, 12, 0, 1, 5)

        self.gridlayout.addWidget(self.atc, 1, 1, 1, 4)
        self.gridlayout.addWidget(self.surname, 2, 1, 1, 4)
        self.gridlayout.addWidget(self.name, 3, 1, 1, 4)
        self.gridlayout.addWidget(self.middlename, 4, 1, 1, 4)
        self.gridlayout.addWidget(self.number, 5, 1, 1, 4)
        self.gridlayout.addWidget(self.address, 6, 1, 1, 4)
        self.gridlayout.addWidget(self.position, 7, 1, 1, 4)
        self.gridlayout.addWidget(self.benefit, 8, 1, 1, 4)
        self.gridlayout.addWidget(self.label_calls, 14, 0)
        self.gridlayout.addWidget(self.buttonsBox, 15, 0, 1, 4)

        self.layout.setGeometry(QRect(441, 212, 173, 154))
        self.layout.addLayout(self.gridlayout)
        self.setLayout(self.layout)
        self.layout.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)

        self.insert_btn.clicked.connect(self.insert)
        self.buttonsBox.accepted.connect(self.reject)
        self.buttonsBox.rejected.connect(self.reject)
        self.date_push.clicked.connect(self.update)

    def update(self):
        date1 = self.date1.text()
        date2 = self.date2.text()
        s = """SELECT calls.id, city.name_city, country.name_country, calls.telephone_in, calls.date, calls.duration, tariff.type_tariff, 
            (calls.duration/60+1)*country.price*tariff.coefficient as price
            FROM calls 
            join city on calls.id_city = city.id
            join country on country.id = city.id_country
            join tariff on calls.id_tariff = tariff.id
            join abonents on calls.id_abonent = abonents.id
            left join benefit on abonents.id_benefit = benefit.id
            WHERE id_abonent = """ + str(self.index) + " and calls.date between '" + str(date1) + "' and '" + str(date2) + "' order by calls.id"
        self.model.setQuery(s)
        query = QSqlQuery()
        query.prepare("""SELECT count(*) from calls where id_abonent = ? and calls.date between ? and ?""")
        query.addBindValue(self.index)
        query.addBindValue(date1)
        query.addBindValue(date2)
        query.exec_()
        while query.next():
            count = query.value(0)
        self.label_count.setText("Количество звонков: " + str(count))

        query.prepare("""SELECT sum((calls.duration/60+1)*country.price*tariff.coefficient) as price
                    FROM calls 
                    join city on calls.id_city = city.id
                    join country on country.id = city.id_country
                    join tariff on calls.id_tariff = tariff.id
                    join abonents on calls.id_abonent = abonents.id
                    left join benefit on abonents.id_benefit = benefit.id
                    WHERE id_abonent = ? and calls.date between ? and ?""")
        query.addBindValue(self.index)
        query.addBindValue(date1)
        query.addBindValue(date2)
        query.exec_()
        while query.next():
            sum = query.value(0)
        self.label_calls.setText("Сумма звонков: " + str(sum))


    def setIndex(self, index):
        self.index = index
        self.setData()
        self.setTable()

    def setTable(self):
        s = """SELECT calls.id, city.name_city, country.name_country, calls.telephone_in, calls.date, calls.duration, tariff.type_tariff, 
            (calls.duration/60+1)*country.price*tariff.coefficient as price
            FROM calls 
            join city on calls.id_city = city.id
            join country on country.id = city.id_country
            join tariff on calls.id_tariff = tariff.id
            join abonents on calls.id_abonent = abonents.id
            left join benefit on abonents.id_benefit = benefit.id
            WHERE id_abonent = """ + str(self.index) + " order by calls.id"
        self.model.setQuery(s)  # вывод звонков одного абонента
        self.model.setHeaderData(0, Qt.Horizontal, "id_звонка")
        self.model.setHeaderData(1, Qt.Horizontal, "Город")
        self.model.setHeaderData(2, Qt.Horizontal, "Страна")
        self.model.setHeaderData(3, Qt.Horizontal, "Телефон собеседника")
        self.model.setHeaderData(4, Qt.Horizontal, "Дата")
        self.model.setHeaderData(5, Qt.Horizontal, "Продолжительность")
        self.model.setHeaderData(6, Qt.Horizontal, "Тариф")
        self.model.setHeaderData(7, Qt.Horizontal, "Цена звонка")
        self.view.resizeColumnsToContents()

    def setData(self):
        query = QSqlQuery()
        data = []
        query.prepare("""select atc.caption, abonents.surname, abonents.name, abonents.middlename, 
                abonents.phone_number, abonents.address, 
                position.type_positon, benefit.type, abonents.document 
                from abonents 
                join atc on abonents.id_atc = atc.id_atc
                join position on abonents.id_position = position.id
                left join benefit on abonents.id_benefit = benefit.id
                where abonents.id = ?;""")
        query.addBindValue(self.index)
        query.exec_()
        while query.next():
            for i in range(9):
                data.append(query.value(i))
        self.atc.setReadOnly(True)
        self.atc.setText(data[0])
        self.surname.setText(data[1])
        self.name.setText(data[2])
        self.middlename.setText(data[3])
        self.number.setText(data[4])
        self.address.setText(data[5])
        self.position.setText(data[6])
        self.benefit.setText(data[7])
        query.prepare("""SELECT count(*) from calls where id_abonent = ?""")
        query.addBindValue(self.index)
        query.exec_()
        while query.next():
            count = query.value(0)
        self.label_count.setText("Количество звонков: " + str(count))

        query.prepare("""SELECT sum((calls.duration/60+1)*country.price*tariff.coefficient) as price
            FROM calls 
            join city on calls.id_city = city.id
            join country on country.id = city.id_country
            join tariff on calls.id_tariff = tariff.id
            join abonents on calls.id_abonent = abonents.id
            left join benefit on abonents.id_benefit = benefit.id
            WHERE id_abonent = ? """)
        query.addBindValue(self.index)
        query.exec_()
        while query.next():
            sum = query.value(0)
        self.label_calls.setText("Сумма звонков: " + str(sum))

    def insert(self):
        dialog = RefactorDialog()
        dialog.setIndex(self.index)
        dialog.exec()
        self.setTable()
        self.setData()



