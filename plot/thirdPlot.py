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

        values1 = []
        values2 = []
        values3 = []

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
               # count = 0
               #  while self.query.next():
               #      count = self.query.value(2)
               #  if j == 0:
               #      values1.append(count)
               #  elif j == 1:
               #      values2.append(count)
               #  elif j == 2:
               #      values3.append(count)

        # print(values1)
        # print(values2)
        # print(values3)

        # plt.rcParams["font.size"] = "8"
        # district = np.array(district)
        # print(count)
        # # count = np.array(count)
        # type = [1, 2, 3]
        # type = np.array(type)
        # print(type)
        # print(count)
        #
        # ax.bar3d(district, type, count, 9, 3, 20)

        fig, ax1 = plt.subplots()
        # fig = plt.figure()

        index = np.arange(len(district))
        # values1 = [5, 7, 3, 4, 6, 1, 1, 1, 1]
        # values2 = [6, 6, 4, 5, 7, 1, 1, 1, 1]
        # values3 = [5, 6, 5, 4, 6, 1, 1, 1, 1]
        #---------------------------2d
        # bw = 0.2
        # plt.axis([-1, 9, 0, 100])
        # plt.bar(index, values1, bw, label=position[0])
        # plt.bar(index + bw, values2, bw, label=position[1])
        # plt.bar(index + 2 * bw, values3, bw, label=position[2])
        # plt.xticks(index + 1.5 * bw, district)
        #
        # plt.legend()
        #
        # data = {position[0]: values1,
        #         position[1]: values2,
        #         position[2]: values3}
        # print(data)
        #
        # # plt.bar(district, count, color='royalblue', alpha=0.7)
        # plt.grid(color='#95a5a6', linestyle='--', linewidth=2, axis='y', alpha=0.7)
        #
        # labels = ax1.set_xticklabels(district, fontsize=7, verticalalignment='center')



        # rects = ax1.patches[]
        # labels2 = values2
        # for rect, label in zip(rects, labels2):
        #     height = rect.get_height()
        #     ax1.text(rect.get_x() + 0.25 + rect.get_width()  / 2, height + 0.01, label,
        #              ha='center', va='bottom')

        # handles = [Rectangle((0, 0), 1, 1, color=c, ec="k") for c in [low, medium, high]]
        # labels = ["low", "medium", "high"]
        # plt.legend(handles, labels)

        #



        #----------------------------------------3d
        ax = fig.add_subplot(projection='3d')

        num_bars = 10
        x_pos = random.sample(xrange(20), num_bars)
        print(x_pos)
        # x_pos = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        # x_list = ['F','F','F', 'q','q','q', 'z','z','z', 'r','r','r', 'p','p','p', 'd','d','d', 'x','x','x' ,'g','g','g', 'w','w','w']
        x_list = [1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6, 7, 7, 7, 8, 8, 8, 9, 9, 9]
        y_list = [1,2,3, 1,2,3, 1,2,3, 1,2,3, 1,2,3, 1,2,3, 1,2,3, 1,2,3, 1,2,3]
        y_pos = random.sample(xrange(20), num_bars)
        print(y_pos)
        # y_pos = [1, 2, 3]
        z_pos = [0] * 27
        print(z_pos)
        x_size = np.ones(len(x_list))
        print(x_size)
        y_size = np.ones(len(y_list))
        print(y_size)
        z_size = count

        print(z_size)



        ax.bar3d(x_list, y_list, z_pos, x_size, y_size, z_size, color='aqua')

        ax.set_xticklabels(district)
        ax.set_yticklabels(position)

        ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
        #  Устанавливаем интервал вспомогательных делений:
        ax.yaxis.set_major_locator(ticker.MultipleLocator(1))



        ax.set_xlim(0, 11)
        # ax.set_ylim(0, 10)
        # ax.set_zlim(0, 10)


        labels = ax1.set_xticklabels(district, fontsize=7, verticalalignment='center')

        fig.set_figwidth(15)

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

        self.view = QTableView()
        self.view.setModel(self.model)
        self.view.resizeColumnsToContents()



        lay = QVBoxLayout(self.centralwidget)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.addWidget(self.plotWidget)

        self.gridlayout.addWidget(self.label1, 0, 0, 1, 8)
        self.gridlayout.addWidget(self.plotWidget, 2, 2)
        self.gridlayout.addWidget(self.view, 2, 3)

        self.layout.setGeometry(QRect(441, 212, 173, 154))
        self.layout.addLayout(self.gridlayout)
        self.setLayout(self.layout)
        self.layout.setAlignment(Qt.AlignTop)























