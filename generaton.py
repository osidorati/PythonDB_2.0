from PyQt5.QtSql import QSqlQuery
import random

class Generation():
    def __init__(self):
        self.query = QSqlQuery()
        self.query.exec("""TRUNCATE tariff, position, benefit, district, calls, abonents, city, country, atc RESTART IDENTITY;""")
        self.file_name1 = 'D:/PythonDB_2.0/helpers/caption.txt'
        self.file_name2 = 'D:/PythonDB_2.0/helpers/street.txt'
        self.file_name3 = 'D:/PythonDB_2.0/helpers/femaleSurname.txt'
        self.file_name4 = 'D:/PythonDB_2.0/helpers/femaleName.txt'
        self.file_name5 = 'D:/PythonDB_2.0/helpers/femaleMiddlename.txt'
        self.file_name6 = 'D:/PythonDB_2.0/helpers/maleMiddlename.txt'
        self.file_name7 = 'D:/PythonDB_2.0/helpers/maleSurname.txt'
        self.file_name8 = 'D:/PythonDB_2.0/helpers/maleName.txt'
        self.file_name9 = 'D:/PythonDB_2.0/helpers/city.txt'
        self.file_name10 = 'D:/PythonDB_2.0/helpers/country.txt'
        self.file_name11 = 'D:/PythonDB_2.0/helpers/district.txt'
        self.file_name12 = 'D:/PythonDB_2.0/helpers/benefit.txt'
        self.file_name13 = 'D:/PythonDB_2.0/helpers/position.txt'
        self.file_name14 = 'D:/PythonDB_2.0/helpers/tariff.txt'

    def open_file(self, file_name):
        with open(file_name, "r", encoding='utf-8') as file:
            lines = file.readlines()
        list = []
        for i in range(len(lines)):
            s = lines[i].rstrip()
            list.append(s)
        return list


    def generation_Atc(self):
        position = self.open_file(self.file_name13)
        for i in range(len(position)):
            self.query.prepare("INSERT INTO position(type_positon) "
                               "VALUES (?)")
            self.query.addBindValue(position[i])
            self.query.exec_()

        district = self.open_file(self.file_name11)
        for i in range(len(district)):
            self.query.prepare("INSERT INTO district(name_district) "
                           "VALUES (?)")
            self.query.addBindValue(district[i])
            self.query.exec_()

        benefit = self.open_file(self.file_name12)
        for i in range(len(benefit)):
            list = benefit[i].split(",")
            self.query.prepare("INSERT INTO benefit(type, terms, tarriff) "
                           "VALUES (?, ?, ?)")
            self.query.addBindValue(str(list[0]))
            self.query.addBindValue(str(list[1]))
            self.query.addBindValue(list[2])
            self.query.exec_()
            print(self.query.lastError().text())

        tariff = self.open_file(self.file_name14)
        for i in range(len(tariff)):
            list = tariff[i].split(",")
            self.query.prepare("INSERT INTO tariff(type_tariff, time_start, time_finish, coefficient) "
                           "VALUES (?, ?, ?, ?)")
            self.query.addBindValue(list[0])
            self.query.addBindValue(list[1])
            self.query.addBindValue(list[2])
            self.query.addBindValue(list[3])
            self.query.exec_()
            print(self.query.lastError().text())

        atc_name = self.open_file(self.file_name1)     #list with name atc

        district = []                                  #list with district
        self.query.exec("""SELECT id FROM district""")
        while self.query.next():
            district.append(self.query.value(0))

        for i in range(len(atc_name)):
            bool = [True, False]
            r = random.choice(district)
            address = self.generation_address()
            data = str(random.randint(1, 28)) + '.' + str(random.randint(1, 12)) + '.' + str(random.randint(1970, 2000))
            state = random.randint(0, 1)
            licens = ""
            for j in range(7):
                b = random.randint(0, 9)
                licens += str(b)

            self.query.prepare("INSERT INTO atc(caption, id_district, address, year, atc_state, license) "
                          "VALUES (?, ?, ?, ?, ?, ?)")
            self.query.addBindValue(atc_name[i])
            self.query.addBindValue(r)
            self.query.addBindValue(address)
            self.query.addBindValue(data)
            self.query.addBindValue(bool[state])
            self.query.addBindValue(licens)
            self.query.exec_()
        self.generation_abonent()


    def generation_address(self):
        street = self.open_file(self.file_name2)
        s = random.choice(street)
        house = random.randint(1, 100)
        appart = random.randint(1, 250)
        address = s + ', ' + str(house) + ', ' + str(appart)
        return address


    def generation_abonent(self):
        benefit = None

        name_list_f = self.open_file(self.file_name4)
        surname_list_f = self.open_file(self.file_name3)
        middlename_list_f = self.open_file(self.file_name5)

        name_list_m = self.open_file(self.file_name8)
        surname_list_m = self.open_file(self.file_name7)
        middlename_list_m = self.open_file(self.file_name6)

        for i in range(1000):
            sex = random.randint(0, 1)
            if sex == 1:
                name = random.choice(name_list_f)
                surname = random.choice(surname_list_f)
                middlename = random.choice(middlename_list_f)
            else:
                name = random.choice(name_list_m)
                surname = random.choice(surname_list_m)
                middlename = random.choice(middlename_list_m)

            self.query.exec("""SELECT id_atc FROM atc ORDER BY RANDOM() LIMIT 1""")
            while self.query.next():
                atc = self.query.value(0)

            phone = '+38071'
            for j in range(7):
                n = random.randint(0, 9)
                phone += str(n)

            address = self.generation_address()

            bool_benefit = random.randint(0, 1)
            if bool_benefit == 1:
                self.query.exec("""SELECT id FROM benefit ORDER BY RANDOM() LIMIT 1""")
                while self.query.next():
                    benefit = self.query.value(0)
                document = "льгота" + surname + name + middlename + ".jpg"
                if benefit == 4:
                    position = 1
                else:
                    position = random.randint(2, 3)
            else:
                position = random.randint(1, 3)
                benefit = None
                document = None

            self.query.prepare("INSERT INTO abonents(id_atc, surname, name, middlename, phone_number, address, id_position, id_benefit, document) "
                      "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)")
            self.query.addBindValue(atc)
            self.query.addBindValue(surname)
            self.query.addBindValue(name)
            self.query.addBindValue(middlename)
            self.query.addBindValue(phone)
            self.query.addBindValue(address)
            self.query.addBindValue(position)
            self.query.addBindValue(benefit)
            self.query.addBindValue(document)
            self.query.exec_()
            print(self.query.lastError().text())
        self.generat_city()


    def generation_calls(self):
        for i in range(8000):
            self.query.exec("""SELECT id FROM abonents ORDER BY RANDOM() LIMIT 1""")
            while self.query.next():
                abonent = self.query.value(0)

            self.query.exec("""SELECT id FROM city ORDER BY RANDOM() LIMIT 1""")
            while self.query.next():
                city = self.query.value(0)

            phone = '+38071'
            for j in range(7):
                n = random.randint(0, 9)
                phone += str(n)

            date = str(random.randint(1, 28)) + '.' + str(random.randint(1, 12)) + '.' + str(random.randint(2018, 2020))
            duration = random.random() + random.randint(1, 10)

            self.query.exec("""SELECT id FROM tariff ORDER BY RANDOM() LIMIT 1""")
            while self.query.next():
                tariff = self.query.value(0)

            self.query.prepare(
                "INSERT INTO calls(id_abonent, id_city, telephone_in, date, duration, id_tariff) "
                "VALUES (?, ?, ?, ?, ?, ?)")
            self.query.addBindValue(abonent)
            self.query.addBindValue(city)
            self.query.addBindValue(phone)
            self.query.addBindValue(date)
            self.query.addBindValue(duration)
            self.query.addBindValue(tariff)
            self.query.exec_()


    def generat_city(self):
        country = self.open_file(self.file_name10)
        for i in range(len(country)):
            price = random.random() + random.randint(1, 5)
            self.query.prepare(
                "INSERT INTO country(name_country, price) "
                "VALUES (?, ?)")
            self.query.addBindValue(country[i])
            self.query.addBindValue(price)
            self.query.exec_()

        city = self.open_file(self.file_name9)
        for i in range(30):
            self.query.prepare(
                "INSERT INTO city(id_country, name_city) "
                "VALUES (?, ?)")
            self.query.addBindValue(1)
            self.query.addBindValue(city[i])
            self.query.exec_()
        for i in range(31, 50, 1):
            self.query.prepare(
                "INSERT INTO city(id_country, name_city) "
                "VALUES (?, ?)")
            self.query.addBindValue(2)
            self.query.addBindValue(city[i])
            self.query.exec_()
        for i in range(51, 80, 1):
            self.query.prepare(
                "INSERT INTO city(id_country, name_city) "
                "VALUES (?, ?)")
            self.query.addBindValue(3)
            self.query.addBindValue(city[i])
            self.query.exec_()
        for i in range(81, 95, 1):
            self.query.prepare(
                "INSERT INTO city(id_country, name_city) "
                "VALUES (?, ?)")
            self.query.addBindValue(4)
            self.query.addBindValue(city[i])
            self.query.exec_()
        for i in range(96, 220, 1):
            self.query.prepare(
                "INSERT INTO city(id_country, name_city) "
                "VALUES (?, ?)")
            self.query.addBindValue(5)
            self.query.addBindValue(city[i])
            self.query.exec_()
        for i in range(221, 250, 1):
            self.query.prepare(
                "INSERT INTO city(id_country, name_city) "
                "VALUES (?, ?)")
            self.query.addBindValue(6)
            self.query.addBindValue(city[i])
            self.query.exec_()
        for i in range(251, 255, 1):
            self.query.prepare(
                "INSERT INTO city(id_country, name_city) "
                "VALUES (?, ?)")
            self.query.addBindValue(7)
            self.query.addBindValue(city[i])
            self.query.exec_()
        self.generation_calls()