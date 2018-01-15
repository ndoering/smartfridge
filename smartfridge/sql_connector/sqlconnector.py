import mysql.connector as msqlc
import configuration_management as conf
import cli_parser as cp
from datetime import datetime


#ToDo: Implement for easier encapsulation and access.
#Easier to store results in a list of objects
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
        self.stmt_result = None


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
        self.db = None
        self.qrl = [] #QueryResultList

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
        self.cursor.execute("CREATE TABLE fridgelog (fid INT AUTO_INCREMENT PRIMARY KEY, capturetime TIMESTAMP, full_image LONGBLOB, manual_labeled BOOLEAN, note CHAR(20))")

        # Table 'fridgelog' contains image with single fruit
        # afid - AllFruitsID, fid - FridgelogID, half_image - Seperated Fruit Image, class - class of fruit, confidence - how sure is the classifier?, prediction - between 0 and 1, note - for later usage
        self.cursor.execute("CREATE TABLE all_fruits (afid INT NOT NULL AUTO_INCREMENT PRIMARY KEY, fid INT, half_image LONGBLOB, class CHAR(1), confidence FLOAT, prediction FLOAT, note CHAR(20), FOREIGN KEY (fid) REFERENCES fridgelog(fid))")

    def reset_tables(self):
        self.cursor.execute("TRUNCATE TABLE all_fruits")
        self.cursor.execute("TRUNCATE TABLE fridgelog")

    # Executing an sql statement consisting of query and filtered values. If no values are available, please call function with an empty string.
    def execute_stmt(self, query, values):
        # TODO: Proper error handling for disconnected objects
        assert self.connected is True

        if self.connected:
            if values == "":
                self.cursor.execute(query)
            else:
                self.cursor.execute(query % values)
            #self.stmt_result = self.cursor.fetchall()
            qr.stmt_result = self.cursor.fetchall()

    # Queries for 'fridgelog'-table, depending on ID
    def print_fridgelog(self, mode, arg):
        #The method uses several mode parameters for several queries
        query1 = "SELECT * FROM fridgelog"
        query2 = "SELECT * FROM fridgelog WHERE fridgelog.fid = %s"
        query3 = "SELECT * FROM fridgelog WHERE fridgelog.capturetime = %s"
        if mode == 1:
            dbhdl.execute_stmt(query1,"")
        elif mode == 2:
            dbhdl.execute_stmt(query2, arg)
        elif mode == 3:
            dbhdl.execute_stmt(query3, arg)
        for row in qr.stmt_result:
            qr.fid = row[0]
            qr.capturetime = row[1]
            qr.full_image = row[2]
            qr.manual_labeled = row[3]
            qr.note = row[4]
            print("fid = %s,capturetime = %s,manual_labeled = %s,note=%s" % \
                  (qr.fid, qr.capturetime, qr.manual_labeled, qr.note))
            self.qrl.append(qr)

    # Queries for 'all_fruits'-table, depending on ID
    def print_all_fruits(self, mode, arg):
        # The method uses several mode parameters for several queries
        query1 = "SELECT * FROM all_fruits"
        query2 = "SELECT * FROM all_fruits WHERE all_fruits.afid = %s"
        query3 = "SELECT * FROM all_fruits WHERE all_fruits.prediction >= %s"

        #TODO: Implementing the confidence filter for query 3.
        if mode == 1:
            dbhdl.execute_stmt(query1,"")
        elif mode == 2:
            dbhdl.execute_stmt(query2, arg)
        elif mode == 3:
            dbhdl.execute_stmt(query3, arg)
        for row in qr.stmt_result:
            qr.afid = row[0]
            qr.fid = row[1]
            qr.half_image = row[2]
            qr.fruitclass = row[3]
            qr.confidence = row[4]
            qr.prediction = row[5]
            qr.note = row[6]

            print("afid = %s, fid = %s, fruitclass = %s, confidence = %s, prediction=%s, note = %s" % \
                  (qr.afid, qr.fid, qr.fruitclass, qr.confidence, qr.prediction, qr.note))
            self.qrl.append(qr)

    # Central 'image'-table containing mainly images with mixed fruit, timestamps, a manual flag and notes
    def insert_fridgelog(self, capturetime, full_image, manual_labeled, note):
        self.cursor.execute("INSERT INTO fridgelog (capturetime, full_image, manual_labeled, note) VALUES(%s, %s, %s, %s)", \
                       (capturetime, full_image, manual_labeled, note))
        self.db.commit()

    # Supplementary table containing a seperate image with highlighted specific fruits, along with the classification data
    def insert_all_fruits(self, fid, half_image, fruit_class, confidence, prediction, note):
        self.cursor.execute(
            "INSERT INTO all_fruits (fid, half_image, class, confidence, prediction, note) VALUES(%s, %s, %s, %s, %s, %s)", \
            (fid, half_image, fruit_class, confidence, prediction, note))
        self.db.commit()


if __name__ == "__main__":

    ## Load DB configuration from config.ini within module package
    parser = cp.CliParser()

    c = conf.Configuration(parser.args.config)
    host = c.config["MYSQL"]["Host"]
    user = c.config["MYSQL"]["User"]
    pw = c.config["MYSQL"]["Password"]
    dbc = c.config["MYSQL"]["Database"]

    ## Open database connection with Database Handle
    dbhdl = MySQLConnector(host, user, pw, dbc)
    dbhdl.connect()
    qr = QueryResult() #Single query result object. List of results is qrl

    # Should be a list of objects, right now it's only one single object for one row

    #Loading images
    img = read_file('/home/shogun/Downloads/test.jpg')
    dbhdl.insert_fridgelog(datetime.now(), img, 1, "hey")
    dbhdl.insert_all_fruits(1, img, "T", 0.25, 0.65, "ha")

    #Works
    #dbhdl.print_fridgelog(1,"")
    #dbhdl.print_fridgelog(2, "1")
    #dbhdl.print_fridgelog(3, "0.85")

    dbhdl.print_all_fruits(1,"")
    dbhdl.print_all_fruits(2,"1")
    dbhdl.print_all_fruits(3,"0.75")

    #Works
    #dbhdl.cursor.execute("SELECT * FROM fridgelog WHERE fridgelog.fid = %s" % "1")
    #print(dbhdl.cursor.fetchall())

    dbhdl.db.commit()
    dbhdl.disconnect()
