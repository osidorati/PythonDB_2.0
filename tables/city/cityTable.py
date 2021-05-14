from PyQt5.QtGui import QFont
from PyQt5.QtSql import QSqlTableModel, QSqlDatabase, QSqlQuery, QSqlQueryModel
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PySide2.QtSql import QSqlRecord

from tables.city.cityChangeTable import ChangeDialog
from tables.city.cityInsertTable import RefactorDialog
from tables.city.cityLookDialog import LookDialog


class CityWidget(QWidget):
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
        self.model.setQuery("select city.id, country.name_country, city.name_city "
                            "from city join country on city.id_country = country.id order by city.id;")
        self.model.setHeaderData(0, Qt.Horizontal, "ID")
        self.model.setHeaderData(1, Qt.Horizontal, "Страна")
        self.model.setHeaderData(2, Qt.Horizontal, "Город")
        self.view = QTableView()
        self.view.setModel(self.model)
        self.view.resizeColumnsToContents()

        self.insert_btn = QPushButton("Добавить")
        self.delete_btn = QPushButton("Удалить")
        self.looked_btn = QPushButton("Просмотр")
        self.change_btn = QPushButton("Изменить")
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
        query.exec_("""select count(*) from city""")
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

        self.layout.setGeometry(QRect(441, 212, 173, 154))
        self.layout.addLayout(self.gridlayout)
        self.setLayout(self.layout)

        self.layout.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        #connections
        self.insert_btn.clicked.connect(self.openAddDialog)
        self.delete_btn.clicked.connect(self.deleteGroup)
        self.change_btn.clicked.connect(self.edit)
        self.all.stateChanged.connect(self.selectAll)
        self.looked_btn.clicked.connect(self.openLookDialog)
        self.ok_btn.clicked.connect(self.research)

    def openLookDialog(self):
        row = self.view.currentIndex()
        index = self.view.model().data(self.view.model().index(row.row(), 0), 0)
        if index is None:
            return
        dialog = LookDialog()
        dialog.setIndex(index)
        dialog.exec()
        self.update()

    def selectAll(self, state):
        if state == Qt.Checked:
            self.view.selectAll()
        else:
            self.view.clearSelection()

    def edit(self):
        row = self.view.currentIndex()
        index = self.view.model().data(self.view.model().index(row.row(), 0), 0)
        if index is None:
            return
        dialog = ChangeDialog()
        dialog.setIndex(index)
        dialog.exec()
        self.update()

    def update(self):
        query = QSqlQuery()
        query.exec_("""select count(*) from city""")
        while query.next():
            count = query.value(0)
        self.label_count.setText("Количество записей: " + str(count))
        self.model.setQuery("""select city.id, country.name_country, city.name_city
                            from city join country on city.id_country = country.id order by city.id;""")

    def openAddDialog(self):
        dialog = RefactorDialog()
        dialog.exec()
        self.update()


    def addContact(self, data):
        """Add a contact to the database."""
        rows = self.model.rowCount()
        self.model.insertRows(rows, 1)
        for column, field in enumerate(data):
            self.model.setData(self.model.index(rows, column + 1), field)
        self.model.submitAll()
        self.model.select()


    def deleteGroup(self):
        query = QSqlQuery()
        if self.view.selectionModel().hasSelection():
            rows = []
            k1 = 0
            for index in self.view.selectionModel().selectedRows() or []:
                rows.append(index.sibling(index.row(), index.column()).data())
            if rows:
                for i in rows:
                    query = QSqlQuery()
                    query.prepare("""select
                        count(distinct calls.id) as calls
                        from city
                        left join calls on city.id = calls.id_city
                        where city.id = ?""")
                    query.addBindValue(i)
                    query.exec_()
                    while query.next():
                        k1 += query.value(0)
                messageBox = QMessageBox.warning(self, self.tr("Warning!"),
                                                 self.tr("Вы действительно хотите удалить этот город? "
                                                         "\nВместе с ним удаляться {} звонков".format(k1)),
                                                 QMessageBox.Ok | QMessageBox.Cancel)
                if messageBox == QMessageBox.Ok:
                    for i in rows:
                        query.prepare("""delete from city where id = ?""")
                        query.addBindValue(i)
                        query.exec_()
                self.update()

    def research(self):
        text = self.search.text()
        if text is not None:
            text = "'%" + text + "%'"
            s = ("select city.id, country.name_country, city.name_city "
                "from city join country on city.id_country = country.id "
                "where country.name_country ilike " + text +
                "or city.name_city ilike" + text
                 )
            self.model.setQuery(s)
        else:
            self.update()

    def deleteContact(self):
        k1 = 0
        row = self.view.currentIndex().row()
        if row < 0:
            return
        t = self.view.currentIndex()
        index = self.view.model().data(self.view.model().index(t.row(), 0), 0)
        query = QSqlQuery()
        query.prepare("""select
            count(distinct calls.id) as calls
            from city
            left join calls on city.id = calls.id_city
            where city.id = ?""")
        query.addBindValue(index)
        query.exec_()
        while query.next():
            k1 = query.value(0)
        messageBox = QMessageBox.warning(self, self.tr("Warning!"),
                                         self.tr("Вы действительно хотите удалить этот город? "
                                                 "\nВместе с ним удаляться {} звонков".format(k1)),
                                         QMessageBox.Ok | QMessageBox.Cancel)
        if messageBox == QMessageBox.Ok:
            self.deleteContactModel(index)


    def deleteContactModel(self, row):
        query = QSqlQuery()
        query.prepare("""delete from city where id = ?""")
        query.addBindValue(row)
        query.exec_()
        self.update()



