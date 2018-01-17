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
        self.db = msqlc.connect(host=self.host,
                                user=self.user,
                                password=self.password,
                                database=self.database)
        self.cursor = self.db.cursor(buffered=True)
        self.connected = True

    def disconnect(self):
        self.db.close()
        self.db = None
        self.cursor = None
        self.connected = False

    def db_create_tables(self):
        # Table 'fridgelog' contains one image with all fruits
        self.cursor.execute("CREATE TABLE fridgelog "
                            "(fid INT AUTO_INCREMENT PRIMARY KEY, "
                            "capturetime TIMESTAMP, "
                            "full_image LONGBLOB, "
                            "manual_labeled BOOLEAN, "
                            "note CHAR(20))")

        # Table 'all_fruits' contains image with one fruit each
        # afid - AllFruitsID,
        # fid - FridgelogID,
        # half_image - Seperated Fruit Image,
        # class - class of fruit,
        # confidence - how sure is the classifier?,
        # prediction - between 0 and 1,
        # note - for later usage
        self.cursor.execute("CREATE TABLE all_fruits "
                            "(afid INT NOT NULL AUTO_INCREMENT PRIMARY KEY, "
                            "fid INT, "
                            "half_image LONGBLOB, "
                            "class INT, "
                            "confidence FLOAT, "
                            "prediction FLOAT, "
                            "note CHAR(20), "
                            "FOREIGN KEY (fid) REFERENCES fridgelog(fid))")

    def drop_tables(self):
        self.cursor.execute("DROP TABLE IF EXISTS all_fruits")
        self.cursor.execute("DROP TABLE IF EXISTS fridgelog")

    def insert_fridgelog(self, data):      
        statement = ("INSERT INTO fridgelog "
                     "(full_image, manual_labeled, note) "
                     "VALUES (%s, %s, %s)")

        self.cursor.execute(statement, data)
        self.db.commit()

    def insert_all_fruits(self, data):
        statement = ("INSERT INTO all_fruits "
                     "(fid, half_image, class, confidence, prediction, note) "
                     "VALUES(%s, %s, %s, %s, %s, %s)")

        self.cursor.execute(statement, data)
        self.db.commit()

    def retrieve(self, what, where, condition=''):
        ''' returns list of tuples that are rows of the statement result '''
        statement = ("SELECT " + what + " FROM " + where + condition)
        self.cursor.execute(statement)
        rows = []
        for what in self.cursor:
            rows.append(what)
        return rows



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
    img = read_file('test.jpg')
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
