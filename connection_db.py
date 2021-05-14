from PyQt5.QtSql import QSqlDatabase


def open_db(self):
    db = QSqlDatabase.addDatabase("QPSQL")
    db.setHostName("localhost")
    db.setPort(5432)
    db.setDatabaseName("atc")
    db.setUserName("postgres")
    db.setPassword("12345")
    db.open()
    if db.open():
        print("database is open")
    if not db.open():
        print(db.lastError().databaseText())
        dbliste = QSqlDatabase.drivers()
        print(dbliste)
        print('database not open')