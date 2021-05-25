import xlwt as xlwt
from PyQt5.QtGui import QFont
from PyQt5.QtSql import QSqlQuery, QSqlQueryModel
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from tables.calls.abonentsLookDialog import LookDialog
from tables.calls.callsChangeDialog import ChangeDialog
from tables.calls.callsInsertDialog import RefactorDialog


class CallsWidget(QWidget):
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

        self.model = QSqlQueryModel(self)
        self.model.setQuery("""select calls.id, abonents.surname, abonents.name, abonents.middlename, abonents.phone_number, 
        city.name_city, calls.telephone_in, calls.date, calls.duration, tariff.type_tariff 
        from calls join abonents on calls.id_abonent = abonents.id 
        join city on calls.id_city = city.id 
        join tariff on calls.id_tariff = tariff.id order by calls.id;""")
        # self.model.setTable("calls")
        # self.model.setEditStrategy(QSqlTableModel.OnFieldChange)
        self.model.setHeaderData(0, Qt.Horizontal, "ID")
        self.model.setHeaderData(1, Qt.Horizontal, "Фамлия")
        self.model.setHeaderData(2, Qt.Horizontal, "Имя")
        self.model.setHeaderData(3, Qt.Horizontal, "Отчество")
        self.model.setHeaderData(4, Qt.Horizontal, "Номер телефона")
        self.model.setHeaderData(5, Qt.Horizontal, "Город")
        self.model.setHeaderData(6, Qt.Horizontal, "Телефон собеседника")
        self.model.setHeaderData(7, Qt.Horizontal, "Дата")
        self.model.setHeaderData(8, Qt.Horizontal, "Продолжительность")
        self.model.setHeaderData(9, Qt.Horizontal, "Тариф")

        self.view = QTableView()
        self.view.setModel(self.model)
        self.view.resizeColumnsToContents()
        # self.view.setFixedWidth(700)
        # self.view.setFixedHeight(500)

        self.insert_btn = QPushButton("Добавить")
        self.delete_btn = QPushButton("Удалить")
        self.looked_btn = QPushButton("Просмотр")
        self.change_btn = QPushButton("Изменить")
        # self.save = QPushButton("Сохранить")
        self.search = QLineEdit()
        self.search.setFixedWidth(310)
        self.ok_btn = QPushButton("Ok")
        self.ok_btn.setFixedWidth(100)
        self.insert_btn.setFixedWidth(100)
        self.delete_btn.setFixedWidth(100)
        self.looked_btn.setFixedWidth(100)
        self.change_btn.setFixedWidth(100)
        self.label = QLabel("Поиск:")
        font = QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.all = QCheckBox("Выбрать все")

        query = QSqlQuery()
        query.exec_("""select count(*) from calls""")
        while query.next():
            count = query.value(0)
        self.label_count = QLabel("Количество записей: " + str(count))

        self.label_count.setFont(font)
        self.gridlayout.addWidget(self.label_count, 2, 0, 1, 2)
        self.gridlayout.addWidget(self.view, 3, 0, 1, 9)
        self.gridlayout.addWidget(self.label, 0, 6)
        self.gridlayout.addWidget(self.all, 1, 3)
        self.gridlayout.addWidget(self.search, 1, 6, 1, 1)
        self.gridlayout.addWidget(self.ok_btn, 1, 7)
        self.gridlayout.addWidget(self.insert_btn, 0, 0)
        self.gridlayout.addWidget(self.delete_btn, 0, 3)
        self.gridlayout.addWidget(self.looked_btn, 0, 1)
        self.gridlayout.addWidget(self.change_btn, 0, 2)
        # self.gridlayout.addWidget(self.save, 0, 4)

        self.layout.setGeometry(QRect(441, 212, 173, 154))
        self.layout.addLayout(self.gridlayout)
        self.setLayout(self.layout)

        self.layout.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)

        #connections
        self.insert_btn.clicked.connect(self.openAddDialog)
        self.delete_btn.clicked.connect(self.deleteGroup)
        self.looked_btn.clicked.connect(self.openLookDialog)
        self.ok_btn.clicked.connect(self.research)
        self.all.stateChanged.connect(self.selectAll)
        self.change_btn.clicked.connect(self.edit)


    def save_excel(self):
        filename = QFileDialog.getSaveFileName(self, 'Save File', '', ".xls(*.xls)")
        wbk = xlwt.Workbook()
        sheet = wbk.add_sheet("sheet", cell_overwrite_ok=True)
        for currentColumn in range(self.model.columnCount()):
            for currentRow in range(self.model.rowCount()):
                teext = str((self.view.model().data(self.view.model().index(currentRow, currentColumn))))
                sheet.write(currentRow, currentColumn, teext)
        wbk.save(filename[0])

    def edit(self):
        row = self.view.currentIndex()
        index = self.view.model().data(self.view.model().index(row.row(), 0), 0)
        if index is None:
            return
        dialog = ChangeDialog()
        dialog.setIndex(index)
        dialog.exec()
        self.update()

    def selectAll(self, state):
        if state == Qt.Checked:
            self.view.selectAll()
        else:
            self.view.clearSelection()

    def research(self):
        text = self.search.text()
        if text is not None:
            text = "'%" + text + "%'"
            s = ("select calls.id, abonents.surname, abonents.name, abonents.middlename, abonents.phone_number, "
                "city.name_city, calls.telephone_in, calls.date, calls.duration, tariff.type_tariff "
                "from calls join abonents on calls.id_abonent = abonents.id "
                "join city on calls.id_city = city.id "
                "join tariff on calls.id_tariff = tariff.id "
                "where abonents.surname ilike " + text +
                "or abonents.name ilike " + text +
                "or abonents.middlename ilike " + text +
                "or abonents.phone_number ilike " + text +
                "or city.name_city ilike " + text +
                "or calls.telephone_in ilike " + text +
                "or tariff.type_tariff ilike " + text
                 )
            self.model.setQuery(s)
        else:
            self.update()

    def openLookDialog(self):
        row = self.view.currentIndex()
        # if row < 0:
        #     return
        index = self.view.model().data(self.view.model().index(row.row(), 0), 0)
        print(index)
        dialog = LookDialog()
        dialog.setIndex(index)
        dialog.exec()
        self.update()


    def openAddDialog(self):
        dialog = RefactorDialog()
        dialog.exec()
        self.update()


    def update(self):
        query = QSqlQuery()
        query.exec_("""select count(*) from calls""")
        while query.next():
            count = query.value(0)
        self.label_count.setText("Количество записей: " + str(count))
        self.model.setQuery("""select calls.id, abonents.surname, abonents.name, abonents.middlename, abonents.phone_number, 
        city.name_city, calls.telephone_in, calls.date, calls.duration, tariff.type_tariff 
        from calls join abonents on calls.id_abonent = abonents.id 
        join city on calls.id_city = city.id 
        join tariff on calls.id_tariff = tariff.id order by calls.id;""")


    def deleteGroup(self):
        query = QSqlQuery()
        if self.view.selectionModel().hasSelection():
            rows = []
            k3 = 0
            for index in self.view.selectionModel().selectedRows() or []:
                rows.append(index.sibling(index.row(), index.column()).data())
            if rows:
                messageBox = QMessageBox.warning(self, self.tr("Warning!"),
                                                 self.tr("Вы действительно хотите удалить выбранный(-ые) звонки? "),
                                                 QMessageBox.Ok | QMessageBox.Cancel)
                if messageBox == QMessageBox.Ok:
                    for i in rows:
                        query.prepare("""delete from calls where id = ?""")
                        query.addBindValue(i)
                        query.exec_()
                self.update()


    def deleteContact(self):
        row = self.view.currentIndex().row()
        if row < 0:
            return
        t = self.view.currentIndex()
        index = self.view.model().data(self.view.model().index(t.row(), 0), 0)
        messageBox = QMessageBox.warning(self, self.tr("Warning!"),
                                         self.tr("Вы действительно хотите удалить этот звонок?"),
                                         QMessageBox.Ok | QMessageBox.Cancel)
        if messageBox == QMessageBox.Ok:
            self.deleteContactModel(index)


    def deleteContactModel(self, row):
        query = QSqlQuery()
        query.prepare("""delete from calls where id = ?""")
        query.addBindValue(row)
        query.exec_()
        self.update()




