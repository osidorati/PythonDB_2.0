import xlwt
from PyQt5.QtGui import QFont
from PyQt5.QtSql import QSqlQuery, QSqlQueryModel
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from tables.abonent.abonentInsertDialog import RefactorDialog
from tables.abonent.abonentsChangeDialog import ChangeDialog
from tables.abonent.callsLookDialog import LookDialog


class AbonentWidget(QWidget):
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
        self.model.setQuery("""select abonents.id, atc.caption, abonents.surname, abonents.name, abonents.middlename, 
        abonents.phone_number, abonents.address, position.type_positon, benefit.type, abonents.document 
        from abonents join atc on abonents.id_atc = atc.id_atc 
        join position on abonents.id_position = position.id 
        left join benefit on abonents.id_benefit = benefit.id order by abonents.id;""")

        # self.model.setEditStrategy(QSqlTableModel.OnFieldChange)
        self.model.setHeaderData(0, Qt.Horizontal, "ID")
        self.model.setHeaderData(1, Qt.Horizontal, "Название АТС")
        self.model.setHeaderData(2, Qt.Horizontal, "Фамилия")
        self.model.setHeaderData(3, Qt.Horizontal, "Имя")
        self.model.setHeaderData(4, Qt.Horizontal, "Отчество")
        self.model.setHeaderData(5, Qt.Horizontal, "Номер")
        self.model.setHeaderData(6, Qt.Horizontal, "Адрес")
        self.model.setHeaderData(7, Qt.Horizontal, "Социальное положение")
        self.model.setHeaderData(8, Qt.Horizontal, "Льгота")
        self.model.setHeaderData(9, Qt.Horizontal, "Документ на льготу")

        self.view = QTableView()
        self.view.setModel(self.model)
        self.view.resizeColumnsToContents()
        self.view.setFixedWidth(1800)

        self.insert_btn = QPushButton("Добавить")
        self.delete_btn = QPushButton("Удалить")
        self.look_btn = QPushButton("Просмотр")
        self.change_btn = QPushButton("Изменить")
        self.save = QPushButton("Сохранить в эксель")
        self.search = QLineEdit()
        self.search.setFixedWidth(310)
        self.ok_btn = QPushButton("Ok")
        self.ok_btn.setFixedWidth(100)
        self.insert_btn.setFixedWidth(100)
        self.delete_btn.setFixedWidth(100)
        self.look_btn.setFixedWidth(100)
        self.change_btn.setFixedWidth(100)
        self.label = QLabel("Поиск:")
        font = QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.all = QCheckBox("Выбрать все")

        query = QSqlQuery()
        query.exec_("""select count(*) from abonents""")
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
        self.gridlayout.addWidget(self.look_btn, 0, 1)
        self.gridlayout.addWidget(self.change_btn, 0, 2)
        self.gridlayout.addWidget(self.save, 0, 4)

        self.layout.setGeometry(QRect(441, 212, 173, 154))
        self.layout.addLayout(self.gridlayout)
        self.setLayout(self.layout)

        self.layout.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)

        # connections
        self.insert_btn.clicked.connect(self.openAddDialog)
        self.delete_btn.clicked.connect(self.deleteGroup)
        self.look_btn.clicked.connect(self.openLookDialog)
        self.ok_btn.clicked.connect(self.research)
        self.all.stateChanged.connect(self.selectAll)
        self.change_btn.clicked.connect(self.edit)
        self.save.clicked.connect(self.save_excel)

    def save_excel(self):
        filename, _ = QFileDialog.getSaveFileName(self, 'Save File', '', ".xls(*.xls)")
        wbk = xlwt.Workbook()
        sheet = wbk.add_sheet("sheet", cell_overwrite_ok=True)
        style = xlwt.XFStyle()
        font = xlwt.Font()
        font.bold = True
        style.font = font
        model = self.view.model()
        for c in range(model.columnCount()):
            text = model.headerData(c, Qt.Horizontal)
            sheet.write(0, c + 1, text, style=style)

        for r in range(model.rowCount()):
            text = model.headerData(r, Qt.Vertical)
            sheet.write(r + 1, 0, text, style=style)

        for c in range(model.columnCount()):
            for r in range(model.rowCount()):
                text = model.data(model.index(r, c))
                sheet.write(r + 1, c + 1, text)
        wbk.save(filename)
        messageBox = QMessageBox.information(self, self.tr("Success!"),
                                         self.tr("Таблица экспортирована! "),
                                         QMessageBox.Ok)
        # filename = QFileDialog.getSaveFileName(self, 'Save File', '', ".xls(*.xls)")
        # wbk = xlwt.Workbook()
        # sheet = wbk.add_sheet("sheet", cell_overwrite_ok=True)
        # for currentColumn in range(self.model.columnCount()):
        #     for currentRow in range(self.model.rowCount()):
        #         teext = str((self.view.model().data(self.view.model().index(currentRow, currentColumn))))
        #         sheet.write(currentRow, currentColumn, teext)
        # wbk.save(filename[0])


    def edit(self):
        row = self.view.currentIndex()
        index = self.view.model().data(self.view.model().index(row.row(), 0), 0)
        if index is None:
            return
        dialog = ChangeDialog()
        dialog.setIndex(index)
        dialog.exec()
        self.update()

    def research(self):
        text = self.search.text()
        if text is not None:
            text = "'%" + text + "%'"
            s = ("select abonents.id, atc.caption, abonents.surname, abonents.name, abonents.middlename, "
                 " abonents.phone_number, abonents.address, position.type_positon, benefit.type, abonents.document "
                 "from abonents join atc on abonents.id_atc = atc.id_atc "
                 "join position on abonents.id_position = position.id "
                 "left join benefit on abonents.id_benefit = benefit.id "
                 "where atc.caption ilike " + text +
                 "or abonents.surname ilike " + text +
                 "or abonents.name ilike " + text +
                 "or abonents.middlename ilike " + text +
                 "or abonents.phone_number ilike " + text +
                 "or abonents.address ilike " + text +
                 "or position.type_positon ilike " + text +
                 "or benefit.type ilike " + text +
                 "or abonents.document ilike " + text
                 )
            self.model.setQuery(s)
        else:
            self.update()

    def openLookDialog(self):
        row = self.view.currentIndex()
        index = self.view.model().data(self.view.model().index(row.row(), 0), 0)
        if index is not None:
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
        query.exec_("""select count(*) from abonents""")
        while query.next():
            count = query.value(0)
        self.label_count.setText("Количество записей: " + str(count))
        self.model.setQuery("""select abonents.id, atc.caption, abonents.surname, abonents.name, abonents.middlename, 
                abonents.phone_number, abonents.address, position.type_positon, benefit.type, abonents.document 
                from abonents join atc on abonents.id_atc = atc.id_atc 
                join position on abonents.id_position = position.id 
                left join benefit on abonents.id_benefit = benefit.id order by abonents.id""")

    def selectAll(self, state):
        if state == Qt.Checked:
            self.view.selectAll()
        else:
            self.view.clearSelection()

    def deleteGroup(self):
        query = QSqlQuery()
        if self.view.selectionModel().hasSelection():
            rows = []
            k3 = 0
            for index in self.view.selectionModel().selectedRows() or []:
                rows.append(index.sibling(index.row(), index.column()).data())
            if rows:
                for i in rows:
                    query = QSqlQuery()
                    query.prepare("""select
                                           count(distinct calls.id) as calls
                                           from abonents
                                           left join calls on abonents.id = calls.id_abonent
                                           where abonents.id = ?""")
                    query.addBindValue(i)
                    query.exec_()
                    while query.next():
                        k3 += query.value(0)
                messageBox = QMessageBox.warning(self, self.tr("Warning!"),
                                                 self.tr("Вы действительно хотите удалить выбранных абонентов? "
                                                         "\nВместе с ними удаляться {} звонков".format(k3)),
                                                 QMessageBox.Ok | QMessageBox.Cancel)
                if messageBox == QMessageBox.Ok:
                    for i in rows:
                        query.prepare("""delete from abonents where id = ?""")
                        query.addBindValue(i)
                        query.exec_()
                self.update()

    def deleteContact(self):
        k3 = 0
        row = self.view.currentIndex().row()
        if row < 0:
            return
        t = self.view.currentIndex()
        index = self.view.model().data(self.view.model().index(t.row(), 0), 0)
        query = QSqlQuery()
        query.prepare("""select
            count(distinct calls.id) as calls
            from abonents
            left join calls on abonents.id = calls.id_abonent
            where abonents.id = ?""")
        query.addBindValue(index)
        query.exec_()
        while query.next():
            k3 = query.value(0)
        messageBox = QMessageBox.warning(self, self.tr("Warning!"),
                                         self.tr("Вы действительно хотите удалить этого абонента? "
                                                 "\nВместе с ним удаляться {} звонков".format(k3)),
                                         QMessageBox.Ok | QMessageBox.Cancel)
        if messageBox == QMessageBox.Ok:
            self.deleteContactModel(index)

    def deleteContactModel(self, row):
        query = QSqlQuery()
        query.prepare("""delete from abonents where id = ?""")
        query.addBindValue(row)
        query.exec_()
        self.update()
