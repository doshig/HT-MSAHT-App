import pypyodbc

## Might need / instea of \
con = pypyodbc.connect(r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};UID=admin;UserCommitSync=Yes;Threads=3;SafeTransactions=0;PageTimeout=5;MaxScanRows=8;MaxBufferSize=2048;FIL=MS Access;DriverId=25;{DefaultDir=C:\Users\stefflc\Desktop\HeatTreat - Moreno Project};{DBQ=C:\Users\stefflc\Desktop\HeatTreat - Moreno Project\Heat Treatmess around 2.accdb};')
# con = pypyodbc.connect('DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};UID=admin;UserCommitSync=Yes;Threads=3;SafeTransactions=0;PageTimeout=5;MaxScanRows=8;MaxBufferSize=2048;FIL=MS Access;DriverId=25;{DefaultDir=C:/Users/stefflc/Desktop/HeatTreat - Moreno Project};{DBQ=C:/Users/stefflc/Desktop/HeatTreat - Moreno Project/Heat Treatmess around 2.accdb};')

cursor = con.cursor()

cursor.execute("SELECT * FROM Solution Treat Orders")

for row in cursor.fetchall():
    print(row)