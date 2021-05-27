import random

import low as low
import matplotlib
import medium as medium
import numpy as np
from PyQt5.QtGui import QFont
from PyQt5.QtSql import QSqlQuery, QSqlQueryModel
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import pandas as pd

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import ticker
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.patches import Rectangle
from past.builtins import xrange

from tables.atc.atcChangeDialog import ChangeDialog
from tables.atc.atcInsertDialog import RefactorDialog
from tables.atc.atcLookDialog import LookDialog
from generaton import Generation


class Plot3Widget(QWidget):
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

        self.label1 = QLabel("Количество абонентов каждой социальной группы по районам")
        font = QFont()
        font.setPointSize(14)
        self.label1.setFont(font)
        district = ['', '']
        self.query.exec_("select district.name_district from district order by district.id")
        while self.query.next():
            district.append(self.query.value(0))

        position = ['']
        self.query.exec_("select position.type_positon from position order by position.id")
        while self.query.next():
            position.append(self.query.value(0))

        self.query.exec_("select district.name_district, position.type_positon, count(abonents.id)"
                            " from district "
                           " right join atc on atc.id_district = district.id"
                           " left join abonents on abonents.id_atc = atc.id_atc"
                           " join position on abonents.id_position = position.id"
                           " group by district.id, district.name_district, position.type_positon order by district.id")

        type = ['']
        count = []
        distrcit2 = []
        while self.query.next():
            count.append(self.query.value(2))

        for i in range(len(district)):
            for j in range(len(position)):
                self.query.prepare("select district.name_district, position.type_positon, count(abonents.id)"
                                 " from district "
                                 " right join atc on atc.id_district = district.id"
                                 " left join abonents on abonents.id_atc = atc.id_atc"
                                 " join position on abonents.id_position = position.id"
                                   " where district.name_district = ? and position.type_positon = ?"
                                 " group by district.id, district.name_district, position.type_positon order by district.id")

                self.query.addBindValue(district[i])
                self.query.addBindValue(position[j])
                self.query.exec_()

        fig = plt.figure()

        index = np.arange(len(district))

        #----------------------------------------3d
        ax = fig.add_subplot(projection='3d')

        num_bars = 10
        x_pos = random.sample(xrange(20), num_bars)

        x_list = [1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6, 7, 7, 7, 8, 8, 8, 9, 9, 9]
        y_list = [1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3]
        y_pos = random.sample(xrange(20), num_bars)

        z_pos = [0] * 27
        x_size = np.ones(len(x_list))
        y_size = np.ones(len(y_list))
        z_size = count

        color = ['aqua', 'red', 'yellow', 'aqua', 'red', 'yellow', 'aqua', 'red', 'yellow', 'aqua', 'red', 'yellow',
                 'aqua', 'red', 'yellow', 'aqua', 'red', 'yellow', 'aqua', 'red', 'yellow', 'aqua', 'red', 'yellow',
                 'aqua', 'red', 'yellow']

        ax.bar3d(x_list, y_list, z_pos, x_size, y_size, z_size, color=color)

        ax.set_xticklabels(district)
        ax.set_yticklabels(position)

        ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
        #  Устанавливаем интервал вспомогательных делений:
        ax.yaxis.set_major_locator(ticker.MultipleLocator(1))

        plt.legend()

        ax.set_xlim(0, 11)

        fig.set_figwidth(25)
        fig.set_figheight(25)

        self.plotWidget = FigureCanvas(fig)
        self.model = QSqlQueryModel(self)
        self.model.setQuery("""select district.name_district, position.type_positon, count(abonents.id)"
                                 " from district "
                                 " right join atc on atc.id_district = district.id"
                                 " left join abonents on abonents.id_atc = atc.id_atc"
                                 " join position on abonents.id_position = position.id"
                                 " group by district.id, district.name_district, position.type_positon order by district.id""")
        # self.model.setHeaderData(0, Qt.Horizontal, "ID")
        # self.model.setHeaderData(1, Qt.Horizontal, "Тип льготы")
        # self.model.setHeaderData(2, Qt.Horizontal, "Условия льготы")
        # self.model.setHeaderData(3, Qt.Horizontal, "Тариф по льготе")

        lay = QVBoxLayout(self.centralwidget)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.addWidget(self.plotWidget)

        self.gridlayout.addWidget(self.label1, 0, 0, 1, 8)
        self.gridlayout.addWidget(self.plotWidget, 2, 2)


        self.layout.setGeometry(QRect(441, 212, 173, 154))
        self.layout.addLayout(self.gridlayout)
        self.setLayout(self.layout)
        self.layout.setAlignment(Qt.AlignTop)























