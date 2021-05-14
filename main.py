import sys

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import *

from query.eightQuery import EightWidget
from query.fifeQuery import FifeWidget
from query.firstQuery import FirstWidget
from query.fourQuery import FourWidget
from query.nineQuery import NineWidget
from query.secondQuery import SecondWidget
from query.sevenQuery import SevenWidget
from query.sixQuery import SixWidget
from tables.abonent.abonents import AbonentWidget
from tables.atc.atcTable import AtcWidget
from tables.benefit.benefit import BenefitWidget
from tables.calls.callsTable import CallsWidget
from tables.city.cityTable import CityWidget
from connection_db import open_db
from tables.country.countryTable import CountryTableWidget
from tables.district.districtTable import DistrictWidget
from tables.position.positionTable import PositionWidget
from register import RegisterWidget
from tables.tariff.tariffTable import TariffWidget
from query.tenQuery import TenWidget
from query.thirdQuery import ThirdWidget


class ShopWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(1800, 800)
        self.login_1 = "osidorati"
        self.password_1 = "12345"

        #open database
        open_db(self)

        self.gridlayout = QGridLayout()
        self.layout = QVBoxLayout()

        #create actions - these can be used in menus/toolbars etc.
        self.atc = QAction("АТС",self)
        #self.register = QAction("Вход", self)
        self.abonents = QAction("Абоненты", self)
        self.calls = QAction("Звонки", self)
        self.districts = QAction("Районы", self)
        self.benefit = QAction("Льготы", self)
        self.city = QAction("Города", self)
        self.position = QAction("Cоциальное положение", self)
        self.country = QAction("Страны", self)
        self.tariff = QAction("Тарифы", self)
        self.first = QAction("Запрос 1", self)
        self.second = QAction("Запрос 2", self)
        self.third = QAction("Запрос 3", self)
        self.four = QAction("Запрос 4", self)
        self.fife = QAction("Запрос 5", self)
        self.six = QAction("Запрос 6", self)
        self.seven = QAction("Запрос 7", self)
        self.eight = QAction("Запрос 8", self)
        self.nine = QAction("Запрос 9", self)
        self.ten = QAction("Запрос 10", self)

        #create the menubar
        self.menu_bar = QMenuBar()
        self.database_menu = self.menu_bar.addMenu("Database")
        self.optional_menu = self.menu_bar.addMenu("Optional")
        self.query_menu = self.menu_bar.addMenu("Query 1")
        self.query2_menu = self.menu_bar.addMenu("Query 2")

        #add the actions to the menubar
        self.database_menu.addAction(self.atc)
        self.database_menu.addAction(self.abonents)
        self.database_menu.addAction(self.calls)
        self.optional_menu.addAction(self.districts)
        self.optional_menu.addAction(self.benefit)
        self.optional_menu.addAction(self.city)
        self.optional_menu.addAction(self.position)
        self.optional_menu.addAction(self.country)
        self.optional_menu.addAction(self.tariff)

        self.query_menu.addAction(self.first)
        self.query_menu.addAction(self.second)
        self.query_menu.addAction(self.third)
        self.query_menu.addAction(self.four)
        self.query_menu.addAction(self.fife)
        self.query_menu.addAction(self.six)
        self.query_menu.addAction(self.seven)
        self.query_menu.addAction(self.eight)

        self.query2_menu.addAction(self.nine)
        self.query2_menu.addAction(self.ten)
        #create toolbars
        font = QFont()
        font.setPointSize(14)
        self.database_toolbar = QToolBar("Manage Databases")
        self.optional_toolbar = QToolBar("Manage Optional")
        self.query_toolbar = QToolBar("Manage Request")
        self.query2_toolbar = QToolBar("Manage Request 2")
        self.database_toolbar.setFont(font)
        self.optional_toolbar.setFont(font)
        self.query_toolbar.setFont(font)
        self.query2_toolbar.setFont(font)
        #add toolbars to window
        self.addToolBar(self.database_toolbar)
        self.addToolBar(self.optional_toolbar)
        self.addToolBar(self.query_toolbar)
        self.addToolBar(self.query2_toolbar)

        self.open_register()

    def authentification(self):
        l = self.add_register_widget.login.text()
        p = self.add_register_widget.password.text()
        if l == self.login_1 and p == self.password_1:
            self.authentic()
        else:
            messageBox = QMessageBox.critical(self, self.tr("Error!"),
                                             self.tr("Ошибка входа! "
                                                     "\nНеверный логин или пароль. Повторите попытку"),
                                             QMessageBox.Ok)


    def open_tariff(self):
        self.add_tariff_widget = TariffWidget()
        self.setCentralWidget(self.add_tariff_widget)
        # # connect the custom signal in the widget to our method
        self.add_tariff_widget.customerAddedSignal.connect(self.process_save_customer)

    def open_position(self):
        self.add_pos_widget = PositionWidget()
        self.setCentralWidget(self.add_pos_widget)
        # # connect the custom signal in the widget to our method
        self.add_pos_widget.customerAddedSignal.connect(self.process_save_customer)

    def open_city(self):
        self.add_city_widget = CityWidget()
        self.setCentralWidget(self.add_city_widget)
        # # connect the custom signal in the widget to our method
        self.add_city_widget.customerAddedSignal.connect(self.process_save_customer)

    def open_benefit(self):
        self.add_benefit_widget = BenefitWidget()
        self.setCentralWidget(self.add_benefit_widget)
        # # connect the custom signal in the widget to our method
        self.add_benefit_widget.customerAddedSignal.connect(self.process_save_customer)

    def open_register(self):
        self.add_register_widget = RegisterWidget()
        self.setCentralWidget(self.add_register_widget)
        self.add_register_widget.enter.clicked.connect(self.authentification)
        # if self.add_register_widget.getStatus():
        #     self.authentic()
        # # connect the custom signal in the widget to our method
        self.add_register_widget.customerAddedSignal.connect(self.process_save_customer)

    def authentic(self):
        #self.database_toolbar.addAction(self.register)
        self.database_toolbar.addAction(self.atc)
        self.database_toolbar.addAction(self.abonents)
        self.database_toolbar.addAction(self.calls)
        self.optional_toolbar.addAction(self.districts)
        self.optional_toolbar.addAction(self.benefit)
        self.optional_toolbar.addAction(self.city)
        self.optional_toolbar.addAction(self.position)
        self.optional_toolbar.addAction(self.country)
        self.optional_toolbar.addAction(self.tariff)

        self.query_toolbar.addAction(self.first)
        self.query_toolbar.addAction(self.second)
        self.query_toolbar.addAction(self.third)
        self.query_toolbar.addAction(self.four)
        self.query_toolbar.addAction(self.fife)
        self.query_toolbar.addAction(self.six)
        self.query_toolbar.addAction(self.seven)
        self.query_toolbar.addAction(self.eight)
        self.query2_toolbar.addAction(self.nine)
        self.query2_toolbar.addAction(self.ten)

        self.database_menu.addAction(self.atc)
        self.database_menu.addAction(self.abonents)
        self.database_menu.addAction(self.calls)
        self.optional_menu.addAction(self.districts)
        self.optional_menu.addAction(self.benefit)
        self.optional_menu.addAction(self.city)
        self.optional_menu.addAction(self.position)
        self.optional_menu.addAction(self.country)
        self.optional_menu.addAction(self.tariff)

        self.query_menu.addAction(self.first)
        self.query_menu.addAction(self.second)
        self.query_menu.addAction(self.third)
        self.query_menu.addAction(self.four)
        self.query_menu.addAction(self.fife)
        self.query_menu.addAction(self.six)
        self.query_menu.addAction(self.seven)
        self.query_menu.addAction(self.eight)
        self.query2_menu.addAction(self.nine)
        self.query2_menu.addAction(self.ten)

        self.districts.triggered.connect(self.open_districts)
        self.atc.triggered.connect(self.open_atc_table)
        self.country.triggered.connect(self.open_country)
        self.abonents.triggered.connect(self.open_abonents)
        self.calls.triggered.connect(self.open_calls)
        self.benefit.triggered.connect(self.open_benefit)
        self.city.triggered.connect(self.open_city)
        self.position.triggered.connect(self.open_position)
        self.tariff.triggered.connect(self.open_tariff)
        self.first.triggered.connect(self.open_first)
        self.second.triggered.connect(self.open_second)
        self.third.triggered.connect(self.open_third)
        self.four.triggered.connect(self.open_four)
        self.fife.triggered.connect(self.open_fife)
        self.six.triggered.connect(self.open_six)
        self.seven.triggered.connect(self.open_seven)
        self.eight.triggered.connect(self.open_eight)
        self.nine.triggered.connect(self.open_nine)
        self.ten.triggered.connect(self.open_ten)
        self.open_atc_table()

    def open_first(self):
        self.add_first = FirstWidget()
        self.setCentralWidget(self.add_first)
        # # connect the custom signal in the widget to our method
        self.add_first.customerAddedSignal.connect(self.process_save_customer)

    def open_second(self):
        self.add_second = SecondWidget()
        self.setCentralWidget(self.add_second)
        # # connect the custom signal in the widget to our method
        self.add_second.customerAddedSignal.connect(self.process_save_customer)

    def open_third(self):
        self.add_third = ThirdWidget()
        self.setCentralWidget(self.add_third)
        # # connect the custom signal in the widget to our method
        self.add_third.customerAddedSignal.connect(self.process_save_customer)

    def open_four(self):
        self.add_four = FourWidget()
        self.setCentralWidget(self.add_four)
        # # connect the custom signal in the widget to our method
        self.add_four.customerAddedSignal.connect(self.process_save_customer)

    def open_fife(self):
        self.add_fife = FifeWidget()
        self.setCentralWidget(self.add_fife)
        self.add_fife.customerAddedSignal.connect(self.process_save_customer)

    def open_six(self):
        self.add_six = SixWidget()
        self.setCentralWidget(self.add_six)
        self.add_six.customerAddedSignal.connect(self.process_save_customer)

    def open_seven(self):
        self.add_seven = SevenWidget()
        self.setCentralWidget(self.add_seven)
        self.add_seven.customerAddedSignal.connect(self.process_save_customer)

    def open_eight(self):
        self.add_eight = EightWidget()
        self.setCentralWidget(self.add_eight)
        self.add_eight.customerAddedSignal.connect(self.process_save_customer)

    def open_nine(self):
        self.add_nine = NineWidget()
        self.setCentralWidget(self.add_nine)
        self.add_nine.customerAddedSignal.connect(self.process_save_customer)

    def open_ten(self):
        self.add_ten = TenWidget()
        self.setCentralWidget(self.add_ten)
        self.add_ten.customerAddedSignal.connect(self.process_save_customer)

    def open_calls(self):
        self.add_call_widget = CallsWidget()
        self.setCentralWidget(self.add_call_widget)
        # # connect the custom signal in the widget to our method
        self.add_call_widget.customerAddedSignal.connect(self.process_save_customer)

    def open_abonents(self):
        self.add_abonent_widget = AbonentWidget()
        self.setCentralWidget(self.add_abonent_widget)
        # # connect the custom signal in the widget to our method
        self.add_abonent_widget.customerAddedSignal.connect(self.process_save_customer)

    def open_districts(self):
        self.add_customer_widget = DistrictWidget()
        self.setCentralWidget(self.add_customer_widget)
        # # connect the custom signal in the widget to our method
        self.add_customer_widget.customerAddedSignal.connect(self.process_save_customer)

    def open_atc_table(self):
        self.add_atc_widget = AtcWidget()
        self.setCentralWidget(self.add_atc_widget)
        # # connect the custom signal in the widget to our method
        self.add_atc_widget.customerAddedSignal.connect(self.process_save_customer)

    def open_country(self):
        self.add_country_widget = CountryTableWidget()
        self.setCentralWidget(self.add_country_widget)
        self.add_country_widget.customerAddedSignal.connect(self.process_save_customer)

    def add_customer_view(self):
        #self.add_customer_widget = AddCustomerWidget()
        self.setCentralWidget(self.add_customer_widget)
        #connect the custom signal in the widget to our method
        self.add_customer_widget.customerAddedSignal.connect(self.process_save_customer)

    def process_save_customer(self):
        details = self.add_customer_widget.customer_details()
        self.connection.add_new_customer(details)
        self.add_customer_widget.clear_details()

    def add_order_view(self):
        #self.add_order_widget = CustomerOrderWidget(self.connection)
        self.setCentralWidget(self.add_order_widget)



if __name__ == "__main__":
    application = QApplication(sys.argv)
    window = ShopWindow()
    window.show()
    window.raise_()
    application.exec_()








