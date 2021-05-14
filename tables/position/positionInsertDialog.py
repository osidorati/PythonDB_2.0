from PyQt5.QtSql import QSqlTableModel, QSqlDatabase, QSqlQuery
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class RefactorDialog(QDialog):

    def __init__(self):
        super().__init__()
        self.data = None

        self.setWindowTitle("Добавление района")

        self.centralwidget = QWidget()
        self.centralwidget.setObjectName(u"centralwidget")
        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(441, 212, 173, 154))
        self.layout = QVBoxLayout()
        self.gridlayout = QGridLayout()

        self.label_distr = QLabel("Социальное положение:")
        self.insert_btn = QPushButton("Добавить")
        self.cancel_btn = QPushButton("Cancel")
        self.name_district_add = QLineEdit()

        self.buttonsBox = QDialogButtonBox(self)
        self.buttonsBox.setOrientation(Qt.Horizontal)
        self.buttonsBox.setStandardButtons(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )

        self.gridlayout.addWidget(self.buttonsBox, 2, 0)
        self.gridlayout.addWidget(self.name_district_add, 1, 0)
        self.gridlayout.addWidget(self.label_distr, 0, 0)

        self.layout.setGeometry(QRect(441, 212, 173, 154))
        self.layout.addLayout(self.gridlayout)
        self.setLayout(self.layout)

        self.layout.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)

        self.buttonsBox.accepted.connect(self.accept)
        self.buttonsBox.rejected.connect(self.reject)

    def accept(self):
        self.data = []
        if len(self.name_district_add.text()) < 3 or self.name_district_add.text().isdigit() == True:
            messageBox = QMessageBox.critical(self, self.tr("Ошибка!"),
                                              self.tr(
                                                  "Социальное положение должно быть не меньше 3 символов и не должно состоять из цирф!"),
                                              QMessageBox.Ok)
        else:
            for field in (self.name_district_add,):
                if not field.text():
                    QMessageBox.critical(
                        self,
                        "Error!",
                        f"You must provide a contact's {field.objectName()}",
                    )
                    self.data = None  # Reset .data
                    return
                self.data.append(field.text())
            if not self.data:
                return
            super().accept()

    def insert(self):
        new_line = self.name_district_add.text()
        if self.name_district_add.text() == '':
            error = QMessageBox()
            error.setWindowTitle("Ошибка ввода")
            error.setText("Нельзя добавить пустую строку")
            error.setIcon(QMessageBox.Critical)
            error.exec_()

        else:
            query = QSqlQuery()
            query.exec("""INSERT INTO district (name_district) VALUES ('%s') """ % (''.join(new_line)))
            QSqlTableModel.insertRecord(20)
            success = QMessageBox()
            success.setWindowTitle("Запись успешно добавлена")
            success.setText("Запись успешно добавлена")
            success.setIcon(QMessageBox.Information)
            success.exec_()
