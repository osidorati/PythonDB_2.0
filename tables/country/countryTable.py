from PyQt5.QtGui import QFont
from PyQt5.QtSql import QSqlTableModel, QSqlDatabase, QSqlQuery, QSqlQueryModel
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from tables.country.countryChangeDialog import ChangeDialog
from tables.country.countryInsertTable import RefactorDialog


class CountryTableWidget(QWidget):
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
        self.model.setQuery("""select * from country order by id""")
        self.model.setHeaderData(0, Qt.Horizontal, "ID")
        self.model.setHeaderData(1, Qt.Horizontal, "Страна")
        self.model.setHeaderData(2, Qt.Horizontal, "Цена за 1 мин")

        self.view = QTableView()
        self.view.setModel(self.model)
        self.view.resizeColumnsToContents()

        self.insert_btn = QPushButton("Добавить")
        self.delete_btn = QPushButton("Удалить")
        self.change_btn = QPushButton("Изменить")
        self.insert_btn.setFixedWidth(100)
        self.delete_btn.setFixedWidth(100)
        self.change_btn.setFixedWidth(100)

        font = QFont()
        font.setPointSize(10)

        query = QSqlQuery()
        query.exec_("""select count(*) from country""")
        while query.next():
            count = query.value(0)
        self.label_count = QLabel("Количество записей: " + str(count))
        self.label_count.setFont(font)
        self.gridlayout.addWidget(self.label_count, 1, 0, 1, 2)
        self.gridlayout.addWidget(self.view, 2, 0, 1, 6)  # строка, столбец
        self.gridlayout.addWidget(self.insert_btn, 0, 0)
        self.gridlayout.addWidget(self.delete_btn, 0, 1)
        self.gridlayout.addWidget(self.change_btn, 0, 2)

        self.layout.setGeometry(QRect(441, 212, 173, 154))
        self.layout.addLayout(self.gridlayout)
        self.setLayout(self.layout)
        self.layout.setAlignment(Qt.AlignTop)

        self.insert_btn.clicked.connect(self.openAddDialog)
        self.delete_btn.clicked.connect(self.deleteGroup)
        self.change_btn.clicked.connect(self.edit)

    def edit(self):
        row = self.view.currentIndex()
        index = self.view.model().data(self.view.model().index(row.row(), 0), 0)
        if index is None:
            return
        dialog = ChangeDialog()
        dialog.setIndex(index)
        dialog.exec()
        self.update()

    def openAddDialog(self):
        dialog = RefactorDialog()
        dialog.exec()
        self.update()

    def update(self):
        self.model.setQuery("""select * from country order by id""")
        query = QSqlQuery()
        query.exec_("""select count(*) from country""")
        while query.next():
            count = query.value(0)
        self.label_count.setText("Количество записей: " + str(count))

    def deleteGroup(self):
        query = QSqlQuery()
        if self.view.selectionModel().hasSelection():
            rows = []
            k2 = 0
            k3 = 0
            for index in self.view.selectionModel().selectedRows() or []:
                rows.append(index.sibling(index.row(), index.column()).data())
            if rows:
                for i in rows:
                    query = QSqlQuery()
                    query.prepare("""select
                        count(distinct city.id) as city,
                        count(distinct calls.id) as calls
                        from country
                        left join city on country.id = city.id_country
                        left join calls on city.id = calls.id_city
                        where country.id = ?""")
                    query.addBindValue(i)
                    query.exec_()
                    while query.next():
                        k2 += query.value(0)
                        k3 += query.value(1)
                messageBox = QMessageBox.warning(self, self.tr("Warning!"),
                                                 self.tr("Вы действительно хотите удалить эту страну? "
                                                         "\nВместе с ней удаляться {} городов и {} звонков".format(k2,
                                                                                                                   k3)),
                                                 QMessageBox.Ok | QMessageBox.Cancel)
                if messageBox == QMessageBox.Ok:
                    for i in rows:
                        query.prepare("""delete from country where id = ?""")
                        query.addBindValue(i)
                        query.exec_()
                self.update()

