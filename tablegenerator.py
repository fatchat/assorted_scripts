import pypyodbc

class TableGenerator:
    def __init__(self):
        self.verbose = False
        self.dryrun = False
        self.crs = None
        self.conn= None
        
    def __del__(self):
        if (self.crs != None):
            self.crs.commit()
            self.crs.close()
            self.conn.close()

    # throws pypyodbc.DatabaseError if connect fails
    def connect (self, dbname):
        self.conn = pypyodbc.connect("database=%s; \
                                     Server=localhost;\
                                     Trusted_Connection=yes;Driver={SQL Server Native Client 11.0}" % dbname)
        self.crs = self.conn.cursor()

    def create(self, table_name, column_spec):
        if (self.crs == None):
            print("Not connected")
            return
        create_str = "CREATE TABLE %s (key_col [nchar](10) NOT NULL," % table_name
        create_str += ", ".join(["%s [%s] NOT NULL" % (x["name"], x["type"]) for x in column_spec])
        create_str += ")"
        if (self.verbose):
            print ("<create string> " + create_str)
        if (not self.dryrun):
            self.crs.execute(create_str)
            self.crs.commit()
        self.insert_str_base = "INSERT INTO %s (key_col, " % table_name
        self.insert_str_base += ", ".join([x["name"] for x in column_spec])
        self.insert_str_base += ") VALUES "
        if (self.verbose):
            print ("<insert base> " + self.insert_str_base)

    def insert(self, values):
        if (self.crs == None):
            print("Not connected")
            return
        insert_str = self.insert_str_base + "("
        insert_str += ",".join([str(x) for x in values])
        insert_str += ")"
        if (self.verbose):
            print("<insert string> " + insert_str)
        if (not self.dryrun):
            self.crs.execute(insert_str)
            self.crs.commit()
