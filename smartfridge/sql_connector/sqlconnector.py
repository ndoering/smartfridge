import mysql.connector as msqlc
import configuration_management as conf
from datetime import datetime

#ToDo: Implement for easier encapsulation and access.
class QueryResult():
    def __init__(self):
        self.afid = None
        self.fid = None
        self.half_image = None
        self.fruit_class = None
        self.confidence = None
        self.prediction = None
        self.capturetime = None
        self.full_image = None
        self.manual_labeled = None
        self.note = None

def read_file(filename):
    with open(filename, 'rb') as f:
        photo = f.read()
    return photo

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
        self.cursor = None

    def connect(self):
        self.db = msqlc.connect(host=self.host, user=self.user, password=self.password, database=self.database)
        self.cursor = self.db.cursor(buffered=True)
        self.connected = True

    def disconnect(self):
        self.db.close()
        self.db = None
        self.cursor = None
        self.connected = False

    def db_create_tables(self):
        # Table 'fridgelog' contains image with all fruit
        self.cursor.execute(
            "CREATE TABLE fridgelog (fid INT AUTO_INCREMENT PRIMARY KEY, capturetime TIMESTAMP, full_image LONGBLOB, manual_labeled BOOLEAN, note CHAR(20))")

        # Table 'fridgelog' contains image with single fruit
        # afid - AllFruitsID, fid - FridgelogID, half_image - Seperated Fruit Image, class - class of fruit, confidence - how sure is the classifier?, prediction - between 0 and 1, note - for later usage
        self.cursor.execute(
            "CREATE TABLE all_fruits (afid INT NOT NULL AUTO_INCREMENT PRIMARY KEY, fid INT, half_image LONGBLOB, class CHAR(1), confidence FLOAT, prediction FLOAT, note CHAR(20), FOREIGN KEY (fid) REFERENCES fridgelog(fid))")

    def reset_tables(self):
        self.cursor.execute("TRUNCATE TABLE all_fruits")
        self.cursor.execute("TRUNCATE TABLE fridgelog")

    def execute_stmt(self, query, values):
        # TODO: Proper error handling for disconnected objects
        assert self.connected == True
        self.query = query
        if self.connected:
            if values == "":
                self.values = None
                self.cursor.execute(self.query)
            else:
                self.values = values
                self.cursor.execute(self.query, self.values)
            self.stmt_result = self.cursor.fetchall()

    def print_fridgelog(self, arg):
        query1 = "SELECT * FROM fridgelog"
        query2 = "SELECT * FROM fridgelog WHERE fridgelog.fid = %s"
        if arg == "":
            dbhdl.execute_stmt(query1,"")
        else:
            dbhdl.execute_stmt(query2, arg)
        for row in self.stmt_result:
            self.fid = row[0]
            self.capturetime = row[1]
            self.full_image = row[2]
            self.manual_labeled = row[3]
            self.note = row[4]
            print("fid = %s,capturetime = %s,manual_labeled = %s,note=%s" % \
                  (self.fid, self.capturetime, self.manual_labeled, self.note))

    def print_all_fruits(self, arg):
        query1 = "SELECT * FROM all_fruits"
        query2 = "SELECT * FROM all_fruits WHERE all_fruits.afid = %s"
        if arg == "":
            dbhdl.execute_stmt(query1,"")
        else:
            dbhdl.execute_stmt(query2, arg)
        #On each execution a result is given and saved
        for row in self.stmt_result:
            self.afid = row[0]
            self.fid = row[1]
            self.half_image = row[2]
            self.fruitclass = row[3]
            self.confidence = row[4]
            self.prediction = row[5]
            self.note = row[6]
            print("afid = %s, fid = %s, fruitclass = %s, confidence = %s, prediction=%s, note = %s" % \
                  (self.afid, self.fid, self.fruitclass, self.confidence, self.prediction, self.note))

    def insert_fridgelog(self, capturetime, full_image, manual_labeled, note):
        self.cursor.execute("INSERT INTO fridgelog (capturetime, full_image, manual_labeled, note) VALUES (%s, %s, %s, %s)", \
                       (capturetime, full_image, manual_labeled, note))
        self.db.commit()

    def insert_all_fruits(self, fid, half_image, fruit_class, confidence, prediction, note):
        self.cursor.execute(
            "INSERT INTO all_fruits (fid, half_image, class, confidence, prediction, note) VALUES (%s, %s, %s, %s, %s, %s)", \
            (fid, half_image, fruit_class, confidence, prediction, note))
        self.db.commit()

if __name__ == "__main__":

    ## Load DB configuration from config.ini within module package
    c = conf.Configuration()
    host = c.config["MYSQL"]["Host"]
    user = c.config["MYSQL"]["User"]
    pw = c.config["MYSQL"]["Password"]
    dbc = c.config["MYSQL"]["Database"]

    ## Open database connection with Database Handle
    dbhdl = MySQLConnector(host, user, pw, dbc)
    dbhdl.connect()

    # Should be a list of objects, right now it's only one single object for one row
    #qr = QueryResult()
    #Loading images

    # Working well
    #ToDo: load bytestream from camera module
    img = read_file('C:\\fatcat.jpg')
    #dbhdl.insert_fridgelog(datetime.now(), img, 1, "hey")
    #dbhdl.insert_all_fruits(1, img, "T", 0.25, 0.65, "ha")

    # Parsing Bug
    dbhdl.print_fridgelog("1")
    # print(dbhdl.stmt_result)

    #Working well
    #dbhdl.print_fridgelog("")
    #dbhdl.print_all_fruits("")

    dbhdl.db.commit()
    dbhdl.disconnect()