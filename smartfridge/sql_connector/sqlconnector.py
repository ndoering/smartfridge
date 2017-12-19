#TODO: Find MySQLdb package
import MySQLdb
#from datetime import datetime


class SQLConnector():
    def __init__(self):
        self.id = 0
        self.connected = False

    def connect(self):
        self.connected = True

    def disconnect(self):
        self.connected = False


class MySQLConnector(SQLConnector):
    def __init__(self, host, user, password, database):
        super().__init__()
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None

    def connect(self):
        #TODO: Interface überprüfen
        self.connection = MySQLdb.connect(self.host, self.user, self.password, self.database)
        self.cursor = db.cursor()
        self.connected = True

    def disconnect(self):
        db.close()
        self.connection = None
        self.cursor = None
        self.connected = False

    def execute_stmt(self, statement):
        #TODO: Proper error handling for disconnected objects
        assert self.connected == True

        if self.connected:
            return self.cursor.execute(statement)

    def execute_stmt_w_data(self, statement, data):
        #TODO: Proper error handling for disconnected objects
        assert self.connected == True

        if self.connected:
            return self.cursor.execute(statement, data)


if __name__ == "__main__":
    # Open database connection
    db = MySQLConnector("localhost", "root", "", "smartfridge")

    # Dropping tables
    db.execute_stmt("DROP TABLE fridgelog")
    db.execute_stmt("DROP TABLE all_fruits")

    # Create tables at first
    db.execute_stmt(
        "CREATE TABLE fridgelog (fid INT AUTO_INCREMENT PRIMARY KEY, capturetime TIMESTAMP, full_image LONGBLOB, manual_labeled BOOLEAN, note CHAR(20))")

    db.execute_stmt(
        "CREATE TABLE all_fruits (afid INT NOT NULL AUTO_INCREMENT PRIMARY KEY, fid INT, half_image LONGBLOB, class CHAR(1), confidence FLOAT, prediction FLOAT ,FOREIGN KEY (fid) REFERENCES fridgelog(fid))")

    # now = datetime.now()
    # Insert values
    # Python gibt timestamp
    stmt = 'INSERT INTO fridgelog (note) VALUES (%s)'
    data = ("hey")
    db.execute_stmt_w_data(stmt, data)

    # test1
    db.execute_stmt("INSERT INTO fridgelog (note) VALUES ('hey')")

    # test2
    db.execute_stmt("INSERT INTO fridgelog (note) VALUES (%s)", ("hey"))

    # test3
    db.execute_stmt("INSERT INTO fridgelog VALUES '', (now, NULL, TRUE)")
    db.execute_stmt("INSERT INTO all_fruits")

    # disconnect from server
    db.disconnect()
