import mysql.connector as mysqlc
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
        self.dict_label = {
            'banana_fresh':             1,
            'banana_fresh-neutral':     2,
            'banana_neutral':           3,
            'banana_neutral-bad':       4,
            'banana_bad':               5
            }

    def connect(self):
        self.db = mysqlc.connect(host=self.host,
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
                            "note CHAR(20))")

        # Table 'all_fruits' contains image with one fruit each
        # afid - AllFruitsID,
        # fid - FridgelogID,
        # half_image - Seperated Fruit Image,
        # class - class of fruit,
        # confidence - how sure is the classifier?,
        # note - for later usage
        self.cursor.execute("CREATE TABLE all_fruits "
                            "(afid INT NOT NULL AUTO_INCREMENT PRIMARY KEY, "
                            "fid INT, "
                            "half_image LONGBLOB, "
                            "class INT, "
                            "confidence FLOAT, "
                            "note CHAR(20), "
                            "FOREIGN KEY (fid) REFERENCES fridgelog(fid))")

    def drop_tables(self):
        self.cursor.execute("DROP TABLES IF EXISTS all_fruits, fridgelog")

    def insert_fridgelog(self, data):      
        statement = ("INSERT INTO fridgelog "
                     "(full_image, note) "
                     "VALUES (%s, %s)")

        self.cursor.execute(statement, data)
        self.db.commit()

    def insert_all_fruits(self, json):
        statement = ("INSERT INTO all_fruits "
                     "(fid, half_image, class, confidence, note) "
                     "VALUES(%s, %s, %s, %s, %s)")

        # get fid of latest entry in fridgelog
        foreign_key = self.retrieve("MAX(fid)", "fridgelog")[0][0]

        # parse json
        for label in json:
            if label['value'] > 0.7:
                data = (foreign_key,
                        'NULL',
                        self.dict_label[label['id']],
                        label['value'],
                        'this is a note')
                self.cursor.execute(statement, data)
                self.db.commit()
            else:
                break # legit because json response is ordered by value
        
        

    def retrieve(self, what, where, condition=''):
        ''' returns list of tuples that are rows of the statement result '''
        statement = ("SELECT " + what + " FROM " + where + condition)
        self.cursor.execute(statement)
        rows = []
        for what in self.cursor:
            rows.append(what)
        return rows


# Dictionary for SQL Statements with placeholder parameters.
# "Description" : "Query"
querydict = {
    # Create tables
    "FL_create":    "CREATE TABLE IF NOT EXISTS fridgelog (\
                    fid INT AUTO_INCREMENT PRIMARY KEY, \
                    capturetime TIMESTAMP, \
                    full_image LONGBLOB, \
                    manual_labeled BOOLEAN, \
                    note CHAR(20))",
    "AF_create":    "CREATE TABLE IF NOT EXISTS all_fruits (\
                    afid INT NOT NULL AUTO_INCREMENT PRIMARY KEY, \
                    fid INT, \
                    half_image LONGBLOB, \
                    class INT, \
                    confidence FLOAT, \
                    note CHAR(20), \
                    FOREIGN KEY (fid) REFERENCES fridgelog(fid))",

    # Clear tables
    "AF_empty":     "TRUNCATE TABLE all_fruits",
    "FL_empty":     "TRUNCATE TABLE all_fridgelog",

    # Delete tables
    "AF_delete":    "DROP TABLE all_fruits",
    "FL_delete":    "DROP TABLE fridgelog",

    # Show all table entries
    "FL_sel_all":   "SELECT * FROM fridgelog",
    "AF_sel_all":   "SELECT * FROM all_fruits",

    # Show row via primary keys
    "FL_sel_fid":   "SELECT * FROM fridgelog WHERE fridgelog.fid = %s",
    "AF_sel_afid":  "SELECT * FROM all_fruits WHERE all_fruits.afid = %s",

    # Show both rows (tomato & banana) from all_fruits for the given fid
    "AF_both_fruits":           "SELECT * FROM all_fruits, fridgelog \
                                WHERE all_fruits.fid = %s",

    # Show fridgelog rows by timestamp
    "FL_sel_capturetime":       "SELECT * FROM fridgelog \
                                WHERE fridgelog.capturetime = %s",

    # Show fridgelog rows with given confidence value and higher
    "FL_sel_min_confidence":    "SELECT * FROM fridgelog \
                                WHERE fridgelog.confidence >= %s",

    # Show all_fruits rows with given class (1-5) value and higher
    "AF_sel_min_class":         "SELECT * FROM all_fruits \
                                WHERE all_fruits.class >= %s",

    # Show all_fruits rows with exact given class value
    "AF_sel_class":     "SELECT * FROM all_fruits \
                        WHERE all_fruits.class = %s",

    # Show all_fruits rows with given prediction value and higher
    "AF_min_pred":      "SELECT * FROM all_fruits \
                        WHERE all_fruits.prediction >= %s",

    # Show all_fruits rows with exact given prediction value
    "AF_equ_pred":      "SELECT * FROM all_fruits \
                        WHERE all_fruits.prediction = %s",

    # Insert values into tables
    "FL_insert":        "INSERT INTO fridgelog \
                        (capturetime, full_image, manual_labeled, note) \
                        VALUES (%s, %s, %s, %s)",
    "AF_insert":        "INSERT INTO all_fruits \
                        (fid, half_image, class, confidence, prediction, note) \
                        VALUES (%s, %s, %s, %s, %s, %s)",
    "FL_insert_nopic":  "INSERT INTO fridgelog \
                        (capturetime, manual_labeled, note) \
                        VALUES (%s, %s, %s)",
    "AF_insert_nopic":  "INSERT INTO all_fruits \
                        (fid, class, confidence, prediction, note) \
                        VALUES (%s, %s, %s, %s, %s)"
}


if __name__ == "__main__":
    pass
