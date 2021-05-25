import explode
import matplotlib
import numpy as np
from PyQt5.QtGui import QFont
from PyQt5.QtSql import QSqlQuery, QSqlQueryModel
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from tables.atc.atcChangeDialog import ChangeDialog
from tables.atc.atcInsertDialog import RefactorDialog
from tables.atc.atcLookDialog import LookDialog
from generaton import Generation


class Plot2Widget(QWidget):
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

        self.view = QTableView()
        self.view.resizeColumnsToContents()
        self.view.setFixedWidth(1400)

        self.label1 = QLabel("Количество АТС в районах")
        font = QFont()
        font.setPointSize(14)
        self.label1.setFont(font)
        sum = 1
        self.query.exec_("select count(atc.id_atc) from atc")
        while self.query.next():
            sum = self.query.value(0)

        self.query.exec_("select district.name_district, count(atc.id_atc) "
                            " from district "
                           " left join atc on atc.id_district = district.id "
                           " group by district.name_district")
        district = []
        count = []
        param = []
        while self.query.next():
            district.append(self.query.value(0))
            param.append(self.query.value(1))
            count.append(self.query.value(1)/sum * 100)

        plt.rcParams["font.size"] = "8"
        # district = np.array(district)
        # count = np.array(count)

        fig, ax1 = plt.subplots()

        ax1.pie(count, labels=district, autopct='%1.1f%%', shadow=True, startangle=90)
        ax1.axis('equal')
        # labels = ax1.set_xticklabels(district, fontsize=7, verticalalignment='center')
        #
        fig.set_figwidth(20)

        self.plotWidget = FigureCanvas(fig)
        lay = QVBoxLayout(self.centralwidget)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.addWidget(self.plotWidget)

        self.gridlayout.addWidget(self.label1, 0, 0, 1, 8)
        self.gridlayout.addWidget(self.plotWidget, 2, 2)

        self.layout.setGeometry(QRect(441, 212, 173, 154))
        self.layout.addLayout(self.gridlayout)
        self.setLayout(self.layout)
        self.layout.setAlignment(Qt.AlignTop)























