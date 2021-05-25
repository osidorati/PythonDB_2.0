from PyQt5.QtGui import QFont
from PyQt5.QtSql import QSqlTableModel, QSqlQuery
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from tables.district.DistrictInsertDialog import RefactorDialog


class DistrictWidget(QWidget):
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

        self.model = QSqlTableModel(self)
        self.model.setTable("district")
        self.model.setEditStrategy(QSqlTableModel.OnFieldChange)
        self.model.setHeaderData(0, Qt.Horizontal, "ID")
        self.model.setHeaderData(1, Qt.Horizontal, "Район")

        self.model.select()

        self.view = QTableView()
        self.view.setModel(self.model)
        self.view.resizeColumnsToContents()
        self.view.setFixedWidth(1000)

        self.insert_btn = QPushButton("Добавить")
        self.delete_btn = QPushButton("Удалить")
        font = QFont()
        font.setPointSize(10)

        query = QSqlQuery()
        query.exec_("""select count(*) from district""")
        while query.next():
            count = query.value(0)
        self.label_count = QLabel("Количество записей: " + str(count))
        self.label_count.setFont(font)
        self.gridlayout.addWidget(self.label_count, 1, 0, 1, 2)
        self.gridlayout.addWidget(self.view, 2, 0, 1, 9)
        self.gridlayout.addWidget(self.insert_btn, 0, 0)
        self.gridlayout.addWidget(self.delete_btn, 0, 1)

        self.layout.setGeometry(QRect(441, 212, 173, 154))
        self.layout.addLayout(self.gridlayout)
        self.setLayout(self.layout)
        self.layout.setAlignment(Qt.AlignTop)

        #connections
        self.insert_btn.clicked.connect(self.openAddDialog)
        self.delete_btn.clicked.connect(self.deleteContact)


    def openAddDialog(self):
        dialog = RefactorDialog()
        if dialog.exec() == QDialog.Accepted:
            self.addContact(dialog.data)

    def addContact(self, data):
        """Add a contact to the database."""
        rows = self.model.rowCount()
        self.model.insertRows(rows, 1)
        for column, field in enumerate(data):
            self.model.setData(self.model.index(rows, column + 1), field)
        self.model.submitAll()
        self.model.select()
        self.update()

    def update(self):
        query = QSqlQuery()
        query.exec_("""select count(*) from district""")
        while query.next():
            count = query.value(0)
        self.label_count.setText("Количество записей: " + str(count))


    def deleteContact(self):
        k1 = 0
        k2 = 0
        k3 = 0
        row = self.view.currentIndex().row()
        if row < 0:
            return
        t = self.view.currentIndex()
        index = self.view.model().data(self.view.model().index(t.row(), 0), 0)
        query = QSqlQuery()
        query.prepare("""select
            count(distinct atc.id_atc) as atc,
            count(distinct abonents.id) as abonents,
            count(distinct calls.id) as calls
            from district
            left join atc on district.id = atc.id_district
            left join abonents on atc.id_atc = abonents.id_atc
            left join calls on abonents.id = calls.id_abonent
            where district.id = ?""")
        query.addBindValue(index)
        query.exec_()
        while query.next():
            k1 = query.value(0)
            k2 = query.value(1)
            k3 = query.value(2)
        messageBox = QMessageBox.warning(self, self.tr("Warning!"),
                                         self.tr("Вы действительно хотите удалить этот район? "
                                                 "\nВместе с ним удаляться {} АТС, {} абонентов и {} звонков".format(k1, k2, k3)),
                                         QMessageBox.Ok | QMessageBox.Cancel)
        if messageBox == QMessageBox.Ok:
            self.deleteContactModel(row)


    def deleteContactModel(self, row):
        self.model.removeRow(row)
        self.model.submitAll()
        self.model.select()
        self.update()


