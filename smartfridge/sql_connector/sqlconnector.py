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

class QueryRow():

    def __init__(self):
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
        print("Properties for current QueryRow:")
        # if self.object_id is not None:
        #   print ("object_id = %s",self.object_id)
        if self.afid is not None:
            print ("afid = %s",self.afid)
        if self.fid is not None:
            print ("fid = %s",self.fid)
        if self.half_image is not None:
            print ("half_image = %s",self.half_image)
        if self.fruit_class is not None:
            print ("fruit_class = %s",self.fruit_class)
        if self.confidence is not None:
            print ("confidence = %s",self.confidence)
        if self.prediction is not None:
            print ("prediction = %s",self.prediction)
        if self.capturetime is not None:
            print ("capturetime = %s",self.capturetime)
        if self.full_image is not None:
            print ("full_image = %s",self.full_image)
        if self.manual_labeled is not None:
            print ("manual_labeled = %s",self.manual_labeled)
        if self.note is not None:
            print ("afid = %s",self.note)
        if self.stmt_result is not None:
            print ("stmt_result = %s",self.stmt_result)

class MySQLConnector:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.cursor = None
        self.db = None
        self.result = None
        self.qrow = None       #Single row within a query
        self.qresult = []      #query can contain several rows
        self.qresult_list = [] #all query results

    def connect(self):
        self.db = msqlc.connect (host=self.host, user=self.user, password=self.password, database=self.database)
        self.cursor = self.db.cursor (buffered=True)
        self.connected = True
        print("DB connection established successfully.")

    def disconnect(self):
        self.db.close ()
        self.db = None
        self.cursor = None
        self.connected = False
        print ("DB successfully disconnected.")

    def exec_stmt(self, stmt=None, values=None):
        assert self.connected is True
        # In order to find the correct return type, its recommend
        # to call the exec_stmt method with the direct dictionary key.
        # Hence, exec_knows which form of return statement to parse for the qr-object.
        stmtcode = (stmt[ :2 ])
        if stmtcode == "AF" or stmtcode == "FL":
            query = querydict.get(stmt)
        else:
            query = stmt
        if self.connected:
            print ("SQL query:")
            if values is None:
                print(query)
                self.cursor.execute (query)
            else:
                print (query % values)
                self.cursor.execute (query, values)
            self.result = self.cursor.fetchall()
            #print ("Raw query result:")
            #print(self.result)
            self.db.commit

            # Create an object for each query that saves properties and stack objects in a list.
            self.qrow = QueryRow ()
            # If query starts with AF create and iterate in one way, with FL in the other.
            if stmtcode == "AF":
                for row in self.result:
                    # Create one new object for each row
                    self.qrow.afid = row[ 0 ]
                    self.qrow.fid = row[ 1 ]
                    self.qrow.half_image = row[ 2 ]
                    self.qrow.fruitclass = row[ 3 ]
                    self.qrow.confidence = row[ 4 ]
                    self.qrow.prediction = row[ 5 ]
                    self.qrow.note = row[ 6 ]
                    # Append object to the qresult class property
                    self.qresult.append (self.qrow)
            elif stmtcode == "FL":
                for row in self.result:
                    self.qrow.fid = row[ 0 ]
                    self.qrow.capturetime = row[ 1 ]
                    self.qrow.full_image = row[ 2 ]
                    self.qrow.manual_labeled = row[ 3 ]
                    self.qrow.note = row[ 4 ]
                    self.qresult.append(self.qrow)
            self.qresult_list.append(self.qresult)

    def print_latest_qresult(self):
        print(len(self.qresult))
        for qr in self.qresult:
            qr.printProperties()
            print()

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

    ## Loading images
    # img = read_file ('/home/shogun/Downloads/test.jpg')
    img = read_file ('c:\\fatcat.jpg')

    ## When using the exec_stmt function:
    ## 1st parameter, please use the dictionary key, so the correct query object will be returned.
    ## Alternatively, a direct sql statement without values, but then no return object is available.

    ## Initialising DBs
    #dbhdl.exec_stmt ("FL_empty")
    #dbhdl.exec_stmt ("AF_empty")
    #dbhdl.exec_stmt ("AF_delete")
    #dbhdl.exec_stmt ("FL_delete")
    #dbhdl.exec_stmt ("FL_create")
    #dbhdl.exec_stmt ("AF_create")

    ## Testing statements. Comparing plain execute and exec_stmt methods
    #dbhdl.cursor.execute("INSERT INTO fridgelog (capturetime, manual_labeled, note) VALUES (%s, %s, %s)", (datetime.now(), "1", "hey"))
    #dbhdl.cursor.execute("FL_insert_nopic", (datetime.now(), "1", "hey"))

    #dbhdl.cursor.execute ("INSERT INTO all_fruits (fid, class, confidence, prediction, note) VALUES (%s, %s, %s, %s, %s)" , (1, 5, 0.25, 0.65, "ha"))
    #dbhdl.exec_stmt ("AF_insert_nopic", (1, 5, 0.25, 0.65, "ha"))

    dbhdl.exec_stmt("FL_sel_all")
    dbhdl.print_latest_qresult()

    # TODO: One parameter does not work, allthoug a param vector works. Why?
    #dbhdl.exec_stmt("AF_sel_afid", 1) #Not working
    #dbhdl.exec_stmt ("SELECT * FROM all_fruits WHERE all_fruits.afid = %s", 1) #Not working
    #dbhdl.cursor.execute("SELECT * FROM all_fruits WHERE all_fruits.afid = 1") #works with plain cursor.execute

    dbhdl.db.commit()
    dbhdl.disconnect()

    