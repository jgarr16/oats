import sqlite3
import csv
import datetime
import csv_export
import settings


if settings.system == 'mac' or settings.system == 'linux':
    csv_export.read(settings.base+'data/v1export.csv')
    sql = sqlite3.connect(settings.base+'data/caprs-v1.db')
elif settings.system == 'windows':
    csv_export.read(settings.base+'data\\export.csv')
    sql = sqlite3.connect(settings.base+'data\\caprs-v1.db')
cur = sql.cursor()


cur.execute('DROP TABLE IF EXISTS V1_tickets')
cur.execute('''CREATE TABLE IF NOT EXISTS V1_tickets
            ("Name" text, 
             "Display Id" text PRIMARY KEY,
             "Type" text,
             "Requested By" text, 
             "Found By" text, 
             "State" text,
             "Team Name" text,
             "Portfolio Item Display Id" text,
             "Created By Name" text,
             "Backlog Group Name" text,
             "Closed Date" datetime,
             "Closed By Name" text,
             "Release Name" text
            )
           ''')
for row in settings.reader:
    cur.execute(
        "INSERT INTO V1_tickets VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", row)
sql.commit()


def format_date(col_num, col_named):
    col_name = str(col_named)    # print(col_num)
    fixtup = []
    count = 0
    cur.execute(''' SELECT * FROM V1_tickets ''')
    datemod = cur.fetchall()
    for row in datemod:
        if row[col_num] != '':
            fix = datetime.datetime.strptime(row[col_num], "%m/%d/%Y")
            im = str(row[1])
            val = str(fix)
            fixtup.append((val, im))
            cur.execute( ''' UPDATE V1_tickets SET "%s"="%s" WHERE "Display ID"="%s" ''' % (col_name, fixtup[count][0], fixtup[count][1]))
            count = count + 1
        else:
            continue
    # print('updated dates on '+str(count)+' "{}" records' .format(col_name))


format_date(10, "Closed Date")


sql.commit()
sql.close()


# TO-DO --- Implement exception handling for database connection errors (reference below)

# Fri Dec 29 - 21:47:24 ❤️  :~ python3 convert.py
# Traceback (most recent call last):
#   File "convert.py", line 1, in <module>
#     import CAPRSdb
#   File "/Users/jrgarrigues/repos/caprs/CAPRSdb.py", line 18, in <module>
#     cur.execute('DROP TABLE IF EXISTS caprs_tickets')
# sqlite3.OperationalError: database is locked

# http://thepythonguru.com/handling-errors/