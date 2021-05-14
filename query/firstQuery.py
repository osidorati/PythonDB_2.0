from PyQt5.QtGui import QFont
from PyQt5.QtSql import QSqlQuery, QSqlQueryModel
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from tables.atc.atcChangeDialog import ChangeDialog
from tables.atc.atcInsertDialog import RefactorDialog
from tables.atc.atcLookDialog import LookDialog
from generaton import Generation


class FirstWidget(QWidget):
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
        self.attempt.setQuery("""select atc.id_atc, atc.caption, district.name_district, atc.address, 
                                    atc.year, atc.atc_state, atc.license 
                                    from atc join district on atc.id_district = district.id;""")

        self.attempt.setHeaderData(0, Qt.Horizontal, "id_АТС")
        self.attempt.setHeaderData(1, Qt.Horizontal, "Название АТС")
        self.attempt.setHeaderData(2, Qt.Horizontal, "Район")
        self.attempt.setHeaderData(3, Qt.Horizontal, "Адрес")
        self.attempt.setHeaderData(4, Qt.Horizontal, "Год открытия")
        self.attempt.setHeaderData(5, Qt.Horizontal, "Тип собственности")
        self.attempt.setHeaderData(6, Qt.Horizontal, "Лицензия")

        self.view = QTableView()
        self.view.setModel(self.attempt)
        self.view.resizeColumnsToContents()
        self.view.setFixedWidth(1400)
        self.date1 = QDateEdit()
        self.date2 = QDateEdit()
        self.date1.setFixedWidth(100)
        self.date2.setFixedWidth(100)
        self.btn = QPushButton("Вывести")
        self.btn.setFixedWidth(100)

        self.label1 = QLabel("Количеcтво АТС открытых за указанный период:")
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

        self.label_count.setFont(font)
        self.gridlayout.addWidget(self.label1, 0, 2, 1, 8)
        self.gridlayout.addWidget(self.label_count, 2, 0)
        self.gridlayout.addWidget(self.view, 3, 0, 1, 8)
        self.gridlayout.addWidget(self.date1, 1, 2)
        self.gridlayout.addWidget(self.date2, 1, 4)
        self.gridlayout.addWidget(self.btn, 1, 6)

        self.layout.setGeometry(QRect(441, 212, 173, 154))
        self.layout.addLayout(self.gridlayout)
        self.setLayout(self.layout)
        self.layout.setAlignment(Qt.AlignTop)

        self.btn.clicked.connect(self.update)

    def update(self):
        date1 = self.date1.text()
        date2 = self.date2.text()
        s = ("select atc.id_atc, atc.caption, district.name_district, atc.address, atc.year, "
                              "atc.atc_state, atc.license "
                              " from atc join district on atc.id_district = district.id "
                              "where atc.year BETWEEN '" + date1 +
                              "' and  '" + date2 + "'")
        self.attempt.setQuery(s)

        query = QSqlQuery()
        query.prepare("""select count(*) from atc where atc.year between ? and ?""")
        query.addBindValue(date1)
        query.addBindValue(date2)
        query.exec_()
        while query.next():
            count = query.value(0)
        self.label_count.setText("Количество записей: " + str(count))


    def edit(self):
        row = self.view.currentIndex()
        # if row < 0:
        #     return
        index = self.view.model().data(self.view.model().index(row.row(), 0), 0)
        dialog = ChangeDialog()
        dialog.setIndex(index)
        dialog.exec()
        self.update()


    def research(self):
        text = self.search.text()
        if text is not None:
            text = "'%" + text + "%'"
            s = ("select atc.id_atc, atc.caption, district.name_district, atc.address, atc.year, atc.atc_state, atc.license "
                "from atc join district on atc.id_district = district.id "
                "where atc.caption ilike " + text +
                "or district.name_district ilike " + text +
                "or atc.address ilike " + text +
                "or atc.license ilike " + text
                 )
            self.attempt.setQuery(s)
        else:
            self.update()

    def selectAll(self, state):
        if state == Qt.Checked:
            self.view.selectAll()
        else:
            self.view.clearSelection()

    def generate(self):
        messageBox = QMessageBox.warning(self, self.tr("Warning!"),
                                         self.tr("Вы действительно хотите сгенерировать новые данные? "
                                                 "\nВсе предыдущие записи удаляться"),
                                         QMessageBox.Ok | QMessageBox.Cancel)
        if messageBox == QMessageBox.Ok:
            generation = Generation()
            generation.generation_Atc()
            self.update()
            self.view.resizeColumnsToContents()
            messageBox = QMessageBox.information(self, self.tr("Success!"),
                                             self.tr("Новые данные сгенерированы!"),
                                             QMessageBox.Ok)

    def openAddDialog(self):
        dialog = RefactorDialog()
        dialog.exec()
        self.update()

    def addContact(self):
        self.attempt.setQuery("""select atc.id_atc, atc.caption, district.name_district, atc.address, 
                                            atc.year, atc.atc_state, atc.license 
                                            from atc join district on atc.id_district = district.id;""")

    # def update(self):
    #     self.attempt.setQuery("""select atc.id_atc, atc.caption, district.name_district, atc.address,
    #                                 atc.year, atc.atc_state, atc.license
    #                                 from atc join district on atc.id_district = district.id;""")

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
                        count(distinct abonents.id) as abonents,
                        count(distinct calls.id) as calls
                        from atc
                        left join abonents on atc.id_atc = abonents.id_atc
                        left join calls on abonents.id = calls.id_abonent
                        where atc.id_atc = ?""")
                    query.addBindValue(i)
                    query.exec_()
                    while query.next():
                        k2 += query.value(0)
                        k3 += query.value(1)
                messageBox = QMessageBox.warning(self, self.tr("Warning!"),
                                                 self.tr("Вы действительно хотите удалить данные АТС? "
                                                 "\nВместе удаляться {} абонентов и {} звонков".format(k2, k3)),
                                                 QMessageBox.Ok | QMessageBox.Cancel)
                if messageBox == QMessageBox.Ok:
                    for i in rows:
                        query.prepare("""delete from atc where id_atc = ?""")
                        query.addBindValue(i)
                        query.exec_()
                self.update()

    def deleteContact(self):
        k2 = 0
        k3 = 0
        row = self.view.currentIndex().row()
        if row < 0:
            return
        t = self.view.currentIndex()
        index = self.view.model().data(self.view.model().index(t.row(), 0), 0)
        print(index)
        query = QSqlQuery()
        query.prepare("""select
            count(distinct abonents.id) as abonents,
            count(distinct calls.id) as calls
            from atc
            left join abonents on atc.id_atc = abonents.id_atc
            left join calls on abonents.id = calls.id_abonent
            where atc.id_atc = ?""")
        query.addBindValue(index)
        query.exec_()
        while query.next():
            k2 = query.value(0)
            k3 = query.value(1)
        messageBox = QMessageBox.warning(self, self.tr("Warning!"),
                                         self.tr("Вы действительно хотите удалить эту АТС? "
                                                 "\nВместе с ней удаляться {} абонентов и {} звонков".format(k2, k3)),
                                         QMessageBox.Ok | QMessageBox.Cancel)
        if messageBox == QMessageBox.Ok:
            self.deleteContactModel(index)


    def deleteContactModel(self, row):
        query = QSqlQuery()
        query.prepare("""delete from atc where id_atc = ?""")
        query.addBindValue(row)
        query.exec_()
        self.update()







