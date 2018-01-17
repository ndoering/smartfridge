import mysql.connector as msqlc
import configuration_management as conf
import cli_parser as cp
from datetime import datetime
import itertools

## Query Dictionary for SQL Statements without argument values. "Description" : "Query"
querydict = {
    # Create tables
    "FL_create": "CREATE TABLE IF NOT EXISTS fridgelog (fid INT AUTO_INCREMENT PRIMARY KEY, capturetime TIMESTAMP, full_image LONGBLOB, manual_labeled BOOLEAN, note CHAR(20))",
    "AF_create": "CREATE TABLE IF NOT EXISTS all_fruits (afid INT NOT NULL AUTO_INCREMENT PRIMARY KEY, fid INT, half_image LONGBLOB, class INT, confidence FLOAT, prediction FLOAT, note CHAR(20), FOREIGN KEY (fid) REFERENCES fridgelog(fid))",
    # Clear tables
    "AF_empty": "TRUNCATE TABLE all_fruits",
    "FL_empty": "TRUNCATE TABLE all_fridgelog",
    # Delete tables
    "AF_delete": "DROP TABLE all_fruits",
    "FL_delete": "DROP TABLE fridgelog",
    # Show all table entries
    "FL_sel_all": "SELECT * FROM fridgelog",
    "AF_sel_all": "SELECT * FROM all_fruits",
    # Show row via prtimary keys
    "FL_sel_fid": "SELECT * FROM fridgelog WHERE fridgelog.fid = %s",
    "AF_sel_afid": "SELECT * FROM all_fruits WHERE all_fruits.afid = %s",
    # Show both rows (tomato & banana) from all_fruits for the given common fridgelog fid
    "AF_both_fruits": "SELECT * FROM all_fruits, fridgelog WHERE all_fruits.fid = %s",
    # Show fridgelog rows by timestamp
    "FL_sel_capturetime": "SELECT * FROM fridgelog WHERE fridgelog.capturetime = %s",
    # Show fridgelog rows with given confidence value and higher
    "FL_sel_min_confidence": "SELECT * FROM fridgelog WHERE fridgelog.confidence >= %s",
    # Show all_fruits rows with given class value and higher (1-5 values possible)
    "AF_sel_min_class": "SELECT * FROM all_fruits WHERE all_fruits.class >= %s",
    # Show all_fruits rows with exact given class value
    "AF_sel_class": "SELECT * FROM all_fruits WHERE all_fruits.class = %s",
    # Show all_fruits rows with given prediction value and higher
    "AF_min_pred": "SELECT * FROM all_fruits WHERE all_fruits.prediction >= %s",
    # Show all_fruits rows with exact given prediction value
    "AF_equ_pred": "SELECT * FROM all_fruits WHERE all_fruits.prediction = %s",
    # Insert values into tables
    "FL_insert": "INSERT INTO fridgelog (capturetime, full_image, manual_labeled, note) VALUES (%s, %s, %s, %s)",
    "AF_insert": "INSERT INTO all_fruits (fid, half_image, class, confidence, prediction, note) VALUES (%s, %s, %s, %s, %s, %s)",
    "FL_insert_nopic": "INSERT INTO fridgelog (capturetime, manual_labeled, note) VALUES (%s, %s, %s)",
    "AF_insert_nopic": "INSERT INTO all_fruits (fid, class, confidence, prediction, note) VALUES (%s, %s, %s, %s, %s)"
}


def read_file(filename):
    with open (filename, 'rb') as f:
        photo = f.read ()
    return photo


# Query result objects are created after each statement and encapsulate returned data.
# For now, we refrain from creating different classes tables,
# since for all possible queries, a specific object needs to be be determined
class QueryResult():
    #counter = itertools.count ()
    #newid = next(counter)

    def __init__(self):
        #self.object_id = QueryResult.newid (self)
        self.note = None
        # Contains a query result as one string per row (for debugging purposes)
        self.stmt_result = []
        self.afid = None
        self.fid = None
        self.half_image = None
        self.fruit_class = None
        self.confidence = None
        self.prediction = None
        self.capturetime = None
        self.full_image = None
        self.manual_labeled = None

    def printProperties(self):
        #if self.object_id is not None:
        #    print (self.object_id)
        if self.afid is not None:
            print (self.afid)
        if self.fid is not None:
            print (self.fid)
        if self.half_image is not None:
            print (self.half_image)
        if self.fruit_class is not None:
            print (self.fruit_class)
        if self.confidence is not None:
            print (self.confidence)
        if self.prediction is not None:
            print (self.prediction)
        if self.capturetime is not None:
            print (self.capturetime)
        if self.full_image is not None:
            print (self.full_image)
        if self.manual_labeled is not None:
            print (self.manual_labeled)
        if self.note is not None:
            print (self.note)
        if self.stmt_result is not None:
            print (self.stmt_result)

class MySQLConnector:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.cursor = None
        self.db = None
        self.qr_obj = None

    def connect(self):
        self.db = msqlc.connect (host=self.host, user=self.user, password=self.password, database=self.database)
        self.cursor = self.db.cursor (buffered=True)
        self.connected = True
        self.query_result_list = [ ]
        print("DB connection established.")

    def disconnect(self):
        self.db.close ()
        self.db = None
        self.cursor = None
        self.connected = False

    def execute_stmt(self, query, values=None):
        # TODO: Proper error handling for disconnected objects

        assert self.connected is True
        if self.connected:
            if values is None:
                print(query)
                self.cursor.execute (query)
            else:
                print (query % values)
                self.cursor.execute (query, values)
            result = self.cursor.fetchall
            # TODO: Determine the execution tables type and create objects accordingly
            # if query starts with AF create and iterate in one way
            # if query starts with FL create and iterate in other way
            qr_obj = QueryResult ()
            if query[ :2 ] == "AF":
                for row in result:
                    # Create one new object for row within the result set
                    qr_obj.afid = row[ 0 ]
                    qr_obj.fid = row[ 1 ]
                    qr_obj.half_image = row[ 2 ]
                    qr_obj.fruitclass = row[ 3 ]
                    qr_obj.confidence = row[ 4 ]
                    qr_obj.prediction = row[ 5 ]
                    qr_obj.note = row[ 6 ]
            elif query[ :2 ] == "FL":
                for row in result:
                    qr_obj.fid = row[ 0 ]
                    qr_obj.capturetime = row[ 1 ]
                    qr_obj.full_image = row[ 2 ]
                    qr_obj.manual_labeled = row[ 3 ]
                    qr_obj.note = row[ 4 ]
            #self.qr_obj.stmt_result = result #ToDo: AttributeError: 'NoneType' object has no attribute 'stmt_result'
            self.query_result_list.append (qr_obj)
            self.db.commit

    def get_latestQueryResult(self):
        return self.query_result_list.pop ()

    # Todo: Discussing, wheter we need a function that searches the results for characteristics, such as IDs.


if __name__ == "__main__":
    ## Load DB configuration from config.ini within module package
    parser = cp.CliParser ()

    c = conf.Configuration (parser.args.config)
    host = c.config[ "MYSQL" ][ "Host" ]
    user = c.config[ "MYSQL" ][ "User" ]
    pw = c.config[ "MYSQL" ][ "Password" ]
    dbc = c.config[ "MYSQL" ][ "Database" ]

    ## Open database connection with Database Handle
    dbhdl = MySQLConnector (host, user, pw, dbc)
    dbhdl.connect ()
    img = read_file ('c:\\fatcat.jpg')

    #dbhdl.execute_stmt(querydict.get("AF_delete"))
    #dbhdl.execute_stmt (querydict.get ("FL_delete"))
    #dbhdl.execute_stmt (querydict.get ("FL_create"))
    #dbhdl.execute_stmt (querydict.get ("AF_create"))

    ## Testing cursor.execute() directly, since parsing error still occurs. One central db.commit at eol.

    ## works with comma. dbhdl.cursor.execute(query_string, argument_vector)
    #dbhdl.cursor.execute("INSERT INTO fridgelog (capturetime, manual_labeled, note) VALUES (%s, %s, %s)", (datetime.now(), "1", "hey"))
    #dbhdl.cursor.execute(querydict.get ("FL_insert_nopic"), (datetime.now(), "1", "hey"))

    dbhdl.cursor.execute ("INSERT INTO all_fruits (fid, class, confidence, prediction, note) VALUES (%s, %s, %s, %s, %s)" , (1, 5, 0.25, 0.65, "ha"))
    dbhdl.execute_stmt (querydict.get ("AF_insert_nopic"), (1, 5, 0.25, 0.65, "ha"))

    # dbhdl.cursor.execute ("INSERT INTO all_fruits (fid, class, confidence, prediction, note) VALUES (%s, %s, %s, %s, %s)" % (1, 5, 0.25, 0.65, "ha") )

    #dbhdl.get_latestQueryResult().printProperties()
    #dbhdl.cursor.execute ("SHOW TABLES FROM smartfridge")
    dbhdl.db.commit()
    # Loading images
    #img = read_file ('/home/shogun/Downloads/test.jpg')
    dbhdl.disconnect ()
