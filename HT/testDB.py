import pyodbc


dataFile = "testDB.accdb"
databaseFile = os.getcwd() + "\\" + dataFile
connectionString = "Driver={Microsoft Access Driver (*.mdb, *.accdb)};Dbq=%s" % databaseFile
cnxn = pyodbc.connect(connectionString)
cursor =cnxn.cursor()
cursor.execute("SELECT * FROM [Solution Treat Orders]")
rows = cursor.fetchall()
for row in rows:
    print(row)



# connStr = (
#     r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};"
#     r"DBQ=C:\Users\stefflc\Desktop\HeatTreat - Moreno Project.accdb;"
#     )
# cnxn = pyodbc.connect(connStr)
# sql = """\
# SELECT * FROM mySavedSelectQueryInAccess
# """
# crsr = cnxn.execute(sql)
# for row in crsr:
#     print(row)
# crsr.close()
# cnxn.close()