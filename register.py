from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class RegisterWidget(QWidget):
    customerAddedSignal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.login_1 = "osidorati"
        self.password_1 = "12345"
        self.authentic = False

        self.centralwidget = QWidget()
        self.centralwidget.setObjectName(u"centralwidget")
        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(441, 212, 173, 154))
        self.layout = QVBoxLayout()
        self.gridlayout = QGridLayout()

        #create widgets
        self.title_label = QLabel("Вход")
        font = QFont()
        font.setPointSize(14)
        self.title_label.setFont(font)
        self.title_label.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)

        self.login_label = QLabel("Login")
        self.password_label = QLabel("Password")
        font_2 = QFont()
        font_2.setPointSize(10)
        self.login_label.setFont(font_2)
        self.password_label.setFont(font_2)

        self.login = QLineEdit("osidorati")
        self.password = QLineEdit("12345")

        # self.login = QLineEdit()
        # self.password = QLineEdit()

        self.login.setFixedWidth(200)
        self.login.setFixedHeight(30)

        self.password.setEchoMode(QLineEdit.Password)
        self.password.setFixedWidth(200)
        self.password.setFixedHeight(30)

        self.enter = QPushButton("Войти")
        self.enter.setFixedHeight(40)
        self.enter.setFont(font_2)


        #layouts

        self.gridlayout.addWidget(self.title_label, 0, 0, 1, 3)
        self.gridlayout.addWidget(self.login_label, 1, 1, 1, 2)
        self.gridlayout.addWidget(self.login, 2, 1,1, 1)
        self.gridlayout.addWidget(self.password_label, 3, 1, 1, 1)
        self.gridlayout.addWidget(self.password, 4, 1, 1, 1)
        self.gridlayout.addWidget(self.enter, 6, 1, 1, 1)

        self.layout.setGeometry(QRect(441, 212, 173, 154))
        self.layout.addLayout(self.gridlayout)
        self.setLayout(self.layout)

        self.layout.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        self.enter.clicked.connect(self.read)

    def read(self):
        login = self.login.text()
        password = self.password.text()
        if login == self.login_1 and password == self.password_1:
            self.authentic = True

    def getStatus(self):
        return self.authentic

    def save_details(self):
        self.customerAddedSignal.emit()

    def clear_details(self):
        self.first_name_edit.clear()
        self.last_name_edit.clear()
        self.house_no_edit.clear()
        self.street_edit.clear()
        self.town_edit.clear()
        self.post_code_edit.clear()
        self.telephone_edit.clear()
        self.email_edit.clear()
