import matplotlib
import numpy as np
from PyQt5.QtGui import QFont
from PyQt5.QtSql import QSqlQuery, QSqlQueryModel
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import ticker
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from tables.atc.atcChangeDialog import ChangeDialog
from tables.atc.atcInsertDialog import RefactorDialog
from tables.atc.atcLookDialog import LookDialog
from generaton import Generation


class Plot1Widget(QWidget):
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

        self.query.exec_("select district.name_district, count(atc.id_atc) "
                            " from district "
                           " left join atc on atc.id_district = district.id "
                           " group by district.name_district")
        district = []
        count = []
        while self.query.next():
            district.append(self.query.value(0))
            count.append(self.query.value(1))
        print(count)

        plt.rcParams["font.size"] = "8"
        district = np.array(district)
        count = np.array(count)

        fig, ax1 = plt.subplots()

        ax1.bar(district, count)

        plt.bar(district, count, color='royalblue', alpha=0.7)
        plt.grid(color='#95a5a6', linestyle='--', linewidth=2, axis='y', alpha=0.7)

        labels = ax1.set_xticklabels(district, fontsize=7, verticalalignment='center')

        rects = ax1.patches
        labels1 = count


        for rect, label in zip(rects, labels1):
            height = rect.get_height()
            ax1.text(rect.get_x() + rect.get_width() / 2, height + 0.01, label,
                    ha='center', va='bottom')

        fig.set_figwidth(15)
        fig.set_figheight(15)

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























