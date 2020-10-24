import sqlite3
import csv
import datetime
import csv_export
import city_site
import url_make
import windows_mac
import settings
import re
import fix_encoding
import os
import shutil
import previous


# if settings.system == 'mac' or settings.system == 'linux':
#   csv_export.read(settings.base + 'data/export.csv')
# elif settings.system == 'windows':
#   csv_export.read(settings.base + 'data\\export.csv')


if settings.system == 'mac' or settings.system == 'linux':
    sql2 = sqlite3.connect(settings.base+'data/caprs-v1.db')
elif settings.system == 'windows':
    sql2 = sqlite3.connect(settings.base+'data\\caprs-v1.db')
cur2 = sql2.cursor()


# TO-DO: add a 'suspended time' field so that we can tell how long our tickets are in a suspended mode.
# database = ':memory:'
sql = sqlite3.connect(
    ':memory:', detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
cur = sql.cursor()
cur.execute('DROP TABLE IF EXISTS rpt_caprs_all')
cur.execute('''CREATE TABLE IF NOT EXISTS rpt_caprs_all
            ("Incident ID" text PRIMARY KEY,
             "Urgency" text,
             "Open Time" datetime,
             "City" text,
             "Brief Description" text,
             "Contact" text,
             "Description" text,
             "Initial Impact" text,
             "Last Updated By" text,
             "Update Time" datetime,
             "Updated By" text,
             "Close Time" datetime,
             "Unsuspend Time" datetime,
             "Solution" text,
             "Status" text,
             "Master Incident" text,
             "Update Action" text
            )
            ''')


ignoreCAPRS = ['IM10862815', 'IM11003357']
for ignore in ignoreCAPRS:
  # print(ignore)
  # cur2.execute( " SELECT 'Incident ID' FROM caprs_tickets_2 " )
  cur2.execute( " DELETE FROM caprs_tickets_2 WHERE 'Incident ID' = ? ", (ignore,)) 
  print('another one bites the dust -', ignore)


cur2.execute(" SELECT * FROM caprs_tickets_2 ")
tickets = cur2.fetchall()
for ticket in tickets:
  cur.execute(
      "INSERT INTO rpt_caprs_all VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", ticket)


# TO-DO: can I move this func to an external module so that I can use it universally?
def format_date(col_num, col_named):
  col_name = str(col_named)
  fixtup = []
  count = 0
  cur.execute(''' SELECT * FROM rpt_caprs_all ''')
  datemod = cur.fetchall()
  for row in datemod:
    if row[col_num] != '' and row[col_num] != None:
      fix = datetime.datetime.strptime(row[col_num],"%Y-%m-%d %H:%M:%S").strftime("%m/%d/%y %H:%M:%S")
      im = str(row[0])
      val = str(fix)
      fixtup.append((val, im))
      cur.execute(''' UPDATE rpt_caprs_all SET "%s"="%s" WHERE "Incident ID"="%s" ''' % (
          col_name, fixtup[count][0], fixtup[count][1]))
      # print(col_name, fixtup[count][0], fixtup[count][1])
      count = count + 1
    else:
      continue
  # print('updated rpt_caprs_all on ' + str(count) +
  #       ' "{}" records' .format(col_name))


format_date(2, "Open Time")
format_date(9, "Update Time")
format_date(11, "Close Time")


rels = {"r1_24_0":"1/25/20 06:00:00", "r1_23_0":"12/14/19 06:00:00", "r1_22_0":"11/23/19 06:00:00", "r1_21_0":"10/19/19 06:00:00", "r1_20_0":"9/21/19 06:00:00", "r1_19_0":"8/24/19 06:00:00", "r1_18_0":"7/27/19 06:00:00", "r1_17_0":"6/22/19 06:00:00", "r1_16_0":"5/25/19 06:00:00", "r1_15_0":"4/20/19 06:00:00", "r1_14_0":"3/23/19 06:00:00", "r1_13_0":"2/23/19 06:00:00", "r1_12_0":"1/26/19 06:00:00", "r1_11_0":"12/15/18 06:00:00", "r1_10_0":"11/17/18 06:00:00", "r1_9_0":"10/20/18 06:00:00", "r1_8_0":"9/22/18 06:00:00", "r1_7_0":"8/25/18 06:00:00", "r1_6_0":"7/28/18 06:00:00", "r1_5_0":"6/23/18 06:00:00", "r1_4_0":"5/26/18 06:00:00", "r1_3_0":"4/28/18 06:00:00", "r1_2_0":"3/31/18 06:00:00", "r1_1_0":"2/24/18 06:00:00", "r1_0_1":"2/3/18 06:00:00", "r1_0_0":"1/27/18 06:00:00", "r0_93_2":"12/16/17 06:00:00", "r0_93_1":"11/18/17 06:00:00", "r0_93_0":"10/14/17 06:00:00", "r0_92_2":"9/2/17 06:00:00", "r0_92_1":"8/5/17 06:00:00", "r0_92_0":"7/8/17 06:00:00", "r0_91_2":"6/3/17 06:00:00", "r0_91_1":"5/6/17 06:00:00", "r0_91_0":"4/6/17 06:00:00"}


# TO-DO: add more releases to the list - need some for Aug, Sep, Oct of 2018
def format_suspend_date(col_num, col_named):
  col_name = str(col_named)
  fixtup = []
  count = 0
  cur.execute(''' SELECT * FROM rpt_caprs_all ''')
  datemod = cur.fetchall()
  for row in datemod:
    if row[col_num] != '' and row[col_num] != None:
      if col_name == "Unsuspend Time":
        fixdate = datetime.datetime.strptime(row[col_num],"%Y-%m-%d %H:%M:%S").strftime("%m/%d/%y %H:%M:%S")
        workweek = datetime.timedelta(days=5)
        r1_24_0 = datetime.datetime.strptime(
            "1/25/20 06:00:00", "%m/%d/%y %H:%M:%S")
        r1_23_0 = datetime.datetime.strptime(
            "12/14/19 06:00:00", "%m/%d/%y %H:%M:%S")
        r1_22_0 = datetime.datetime.strptime(
            "11/23/19 06:00:00", "%m/%d/%y %H:%M:%S")
        r1_21_0 = datetime.datetime.strptime(
            "10/19/19 06:00:00", "%m/%d/%y %H:%M:%S")
        r1_20_0 = datetime.datetime.strptime(
            "9/21/19 06:00:00", "%m/%d/%y %H:%M:%S")
        r1_19_0 = datetime.datetime.strptime(
            "8/24/19 06:00:00", "%m/%d/%y %H:%M:%S")
        r1_18_0 = datetime.datetime.strptime(
            "7/27/19 06:00:00", "%m/%d/%y %H:%M:%S")
        r1_17_0 = datetime.datetime.strptime(
            "6/22/19 06:00:00", "%m/%d/%y %H:%M:%S")
        r1_16_0 = datetime.datetime.strptime(
            "5/25/19 06:00:00", "%m/%d/%y %H:%M:%S")
        r1_15_0 = datetime.datetime.strptime(
            "4/20/19 06:00:00", "%m/%d/%y %H:%M:%S")
        r1_14_0 = datetime.datetime.strptime(
            "3/23/19 06:00:00", "%m/%d/%y %H:%M:%S")
        r1_13_0 = datetime.datetime.strptime(
            "2/23/19 06:00:00", "%m/%d/%y %H:%M:%S")
        r1_12_0 = datetime.datetime.strptime(
            "1/26/19 06:00:00", "%m/%d/%y %H:%M:%S")
        r1_11_0 = datetime.datetime.strptime(
            "12/15/18 06:00:00", "%m/%d/%y %H:%M:%S")
        r1_10_0 = datetime.datetime.strptime(
            "11/17/18 06:00:00", "%m/%d/%y %H:%M:%S")
        r1_9_0 = datetime.datetime.strptime(
            "10/20/18 06:00:00", "%m/%d/%y %H:%M:%S")
        r1_8_0 = datetime.datetime.strptime(
            "9/22/18 06:00:00", "%m/%d/%y %H:%M:%S")
        r1_7_0 = datetime.datetime.strptime(
            "8/25/18 06:00:00", "%m/%d/%y %H:%M:%S")
        r1_6_0 = datetime.datetime.strptime(
            "7/28/18 06:00:00", "%m/%d/%y %H:%M:%S")
        r1_5_0 = datetime.datetime.strptime(
            "6/23/18 06:00:00", "%m/%d/%y %H:%M:%S")
        r1_4_0 = datetime.datetime.strptime(
            "5/26/18 06:00:00", "%m/%d/%y %H:%M:%S")
        r1_3_0 = datetime.datetime.strptime(
            "4/28/18 06:00:00", "%m/%d/%y %H:%M:%S")
        r1_2_0 = datetime.datetime.strptime(
            "3/31/18 06:00:00", "%m/%d/%y %H:%M:%S")
        r1_1_0 = datetime.datetime.strptime(
            "2/24/18 06:00:00", "%m/%d/%y %H:%M:%S")
        r1_0_1 = datetime.datetime.strptime(
            "2/3/18 06:00:00", "%m/%d/%y %H:%M:%S")
        r1_0_0 = datetime.datetime.strptime(
            "1/27/18 06:00:00", "%m/%d/%y %H:%M:%S")
        r0_93_2 = datetime.datetime.strptime(
            "12/16/17 06:00:00", "%m/%d/%y %H:%M:%S")
        r0_93_1 = datetime.datetime.strptime(
            "11/18/17 06:00:00", "%m/%d/%y %H:%M:%S")
        r0_93_0 = datetime.datetime.strptime(
            "10/14/17 06:00:00", "%m/%d/%y %H:%M:%S")
        r0_92_2 = datetime.datetime.strptime(
            "9/2/17 06:00:00", "%m/%d/%y %H:%M:%S")
        r0_92_1 = datetime.datetime.strptime(
            "8/5/17 06:00:00", "%m/%d/%y %H:%M:%S")
        r0_92_0 = datetime.datetime.strptime(
            "7/8/17 06:00:00", "%m/%d/%y %H:%M:%S")
        r0_91_2 = datetime.datetime.strptime(
            "6/3/17 06:00:00", "%m/%d/%y %H:%M:%S")
        r0_91_1 = datetime.datetime.strptime(
            "5/6/17 06:00:00", "%m/%d/%y %H:%M:%S")
        r0_91_0 = datetime.datetime.strptime(
            "4/6/17 06:00:00", "%m/%d/%y %H:%M:%S")
        if datetime.datetime.strptime(fixdate, "%m/%d/%y %H:%M:%S") > r1_24_0 + workweek:
            fix = "Post-Jan2020 Backlog - 1.24.0"
        elif datetime.datetime.strptime(fixdate, "%m/%d/%y %H:%M:%S") > r1_23_0 + workweek:
            fix = "Release 1.24.0 - 1/25/20"
        elif datetime.datetime.strptime(fixdate, "%m/%d/%y %H:%M:%S") > r1_22_0 + workweek:
            fix = "Release 1.23.0 - 12/14/19"
        elif datetime.datetime.strptime(fixdate, "%m/%d/%y %H:%M:%S") > r1_21_0 + workweek:
            fix = "Release 1.22.0 - 11/23/19"
        elif datetime.datetime.strptime(fixdate, "%m/%d/%y %H:%M:%S") > r1_20_0 + workweek:
            fix = "Release 1.21.0 - 10/19/19"
        elif datetime.datetime.strptime(fixdate, "%m/%d/%y %H:%M:%S") > r1_19_0 + workweek:
            fix = "Release 1.20.0 - 9/21/19"
        elif datetime.datetime.strptime(fixdate, "%m/%d/%y %H:%M:%S") > r1_18_0 + workweek:
            fix = "Release 1.19.0 - 8/24/19"
        elif datetime.datetime.strptime(fixdate, "%m/%d/%y %H:%M:%S") > r1_17_0 + workweek:
            fix = "Release 1.18.0 - 7/27/19"
        elif datetime.datetime.strptime(fixdate, "%m/%d/%y %H:%M:%S") > r1_16_0 + workweek:
            fix = "Release 1.17.0 - 6/22/19"
        elif datetime.datetime.strptime(fixdate, "%m/%d/%y %H:%M:%S") > r1_15_0 + workweek:
            fix = "Release 1.16.0 - 5/25/19"
        elif datetime.datetime.strptime(fixdate, "%m/%d/%y %H:%M:%S") > r1_14_0 + workweek:
            fix = "Release 1.15.0 - 4/20/19"
        elif datetime.datetime.strptime(fixdate, "%m/%d/%y %H:%M:%S") > r1_13_0 + workweek:
            fix = "Release 1.14.0 - 3/23/19"
        elif datetime.datetime.strptime(fixdate, "%m/%d/%y %H:%M:%S") > r1_12_0 + workweek:
            fix = "Release 1.13.0 - 2/23/19"
        elif datetime.datetime.strptime(fixdate, "%m/%d/%y %H:%M:%S") > r1_11_0 + workweek:
            fix = "Release 1.12.0 - 1/26/19"
        elif datetime.datetime.strptime(fixdate, "%m/%d/%y %H:%M:%S") > r1_10_0 + workweek:
            fix = "Release 1.11.0 - 12/15/18"
        elif datetime.datetime.strptime(fixdate, "%m/%d/%y %H:%M:%S") > r1_9_0 + workweek:
            fix = "Release 1.10.0 - 11/17/18"
        elif datetime.datetime.strptime(fixdate, "%m/%d/%y %H:%M:%S") > r1_8_0 + workweek:
            fix = "Release 1.9.0 - 10/20/18"
        elif datetime.datetime.strptime(fixdate, "%m/%d/%y %H:%M:%S") > r1_7_0 + workweek:
            fix = "Release 1.8.0 - 9/22/18"
        elif datetime.datetime.strptime(fixdate, "%m/%d/%y %H:%M:%S") > r1_6_0 + workweek:
            fix = "Release 1.7.0 - 8/25/18"
        elif datetime.datetime.strptime(fixdate, "%m/%d/%y %H:%M:%S") > r1_5_0 + workweek:
            fix = "Release 1.6.0 - 7/28/18"
        elif datetime.datetime.strptime(fixdate, "%m/%d/%y %H:%M:%S") > r1_4_0 + workweek:
            fix = "Release 1.5.0 - 6/23/18"
        elif datetime.datetime.strptime(fixdate, "%m/%d/%y %H:%M:%S") > r1_3_0 + workweek:
            fix = "Release 1.4.0 - 5/26/18"
        elif datetime.datetime.strptime(fixdate, "%m/%d/%y %H:%M:%S") > r1_2_0 + workweek:
            fix = "Release 1.3.0 - 4/28/18"
        elif datetime.datetime.strptime(fixdate, "%m/%d/%y %H:%M:%S") > r1_1_0 + workweek:
            fix = "Release 1.2.0 - 3/31/18"
        elif datetime.datetime.strptime(fixdate, "%m/%d/%y %H:%M:%S") > r1_0_1 + workweek:
            fix = "Release 1.1.0 - 2/24/18"
        elif datetime.datetime.strptime(fixdate, "%m/%d/%y %H:%M:%S") > r1_0_0 + workweek:
            fix = "Release 1.0.1 - 2/3/18"
        elif datetime.datetime.strptime(fixdate, "%m/%d/%y %H:%M:%S") > r0_93_2 + workweek:
            fix = "Release 1.0.0 - 1/27/18"
        elif datetime.datetime.strptime(fixdate, "%m/%d/%y %H:%M:%S") > r0_93_1 + workweek:
            fix = "Release 0.93.2 - 12/16/17"
        elif datetime.datetime.strptime(fixdate, "%m/%d/%y %H:%M:%S") > r0_93_0 + workweek:
            fix = "Release 0.93.1 - 11/18/17"
        elif datetime.datetime.strptime(fixdate, "%m/%d/%y %H:%M:%S") > r0_92_2 + workweek:
            fix = "Release 0.93.0 - 10/14/17"
        elif datetime.datetime.strptime(fixdate, "%m/%d/%y %H:%M:%S") > r0_92_1 + workweek:
            fix = "Release 0.92.2 - 9/2/17"
        elif datetime.datetime.strptime(fixdate, "%m/%d/%y %H:%M:%S") > r0_92_0 + workweek:
            fix = "Release 0.92.1 - 8/5/17"
        elif datetime.datetime.strptime(fixdate, "%m/%d/%y %H:%M:%S") > r0_91_2 + workweek:
            fix = "Release 0.92.0 - 7/8/17"
        elif datetime.datetime.strptime(fixdate, "%m/%d/%y %H:%M:%S") > r0_91_1 + workweek:
            fix = "Release 0.91.2 - 6/3/17"
        elif datetime.datetime.strptime(fixdate, "%m/%d/%y %H:%M:%S") > r0_91_0 + workweek:
            fix = "Release 0.91.1 - 5/6/17"
        else:
            fix = "This one is really old..."
        # fix = (str(datetime.datetime.strptime(row[col_num], "%m/%d/%y %H:%M:%S").strftime('%B'))+' Release')
        # fix = datetime.datetime.strptime(row[col_num], "%m/%d/%y %H:%M:%S").strftime("%m/%d/%Y")
      else:
        # fix = datetime.datetime.strptime(row[col_num], "%m/%d/%y %H:%M:%S")
        continue
      im = str(row[0])
      val = str(fix)
      fixtup.append((val, im))
      cur.execute(''' UPDATE rpt_caprs_all SET "%s"="%s" WHERE "Incident ID"="%s" ''' % (
          col_name, fixtup[count][0], fixtup[count][1]))
      # print(col_name, fixtup[count][0], fixtup[count][1])
      count = count + 1
    else:
      continue
  # print('updated rpt_caprs_all with suspense dates on ' + str(count) +
        # ' "{}" records' .format(col_name))


format_suspend_date(12, "Unsuspend Time")
sql.commit()


cur.execute(''' SELECT * FROM rpt_caprs_all ''')
alert = cur.fetchall()


im = ""
for i in range(len(alert)):
  # city_site.city_to_site_id(alert[i][3])
  city_site.site_id_to_state(alert[i][3])
  im = alert[i][0]
  cur.execute(
      ''' UPDATE rpt_caprs_all SET City = ? WHERE "Incident ID" = ? ''', (settings.state, im))
  sql.commit()


for i in range(len(alert)):
  urgency = ""
  urgencycode = alert[i][1]
  if urgencycode == "5":
    urgency = "P4"
  elif urgencycode == "4":
    urgency = "P3"
  elif urgencycode == "3":
    urgency = "P2"
  elif urgencycode == "2":
    urgency = "P1"
  elif urgencycode == "1":
    urgency = "Sev1"
  im = alert[i][0]
  cur.execute(
      ''' UPDATE rpt_caprs_all SET Urgency = ? WHERE "Incident ID" = ? ''', (urgency, im))
  sql.commit()


for i in range(len(alert)):
  if alert[i][15] == "true":
    master = "Master Ticket"
  else: master = ""
  im = alert[i][0]
  cur.execute(
      ''' UPDATE rpt_caprs_all SET "Master Incident" = ? WHERE "Incident ID" = ? ''', (master, im))
  sql.commit()


# for i in range(len(alert)):
#   im = alert[i][0]
#   if (alert[i][4] startswith "WL" or alert[i][4] startswith "Sev1" or alert[i][4] startswith " Sev1"):
#     cur.execute(
#       ''' UPDATE rpt_caprs_all SET "Urgency" = "SEV 1" WHERE "Incident ID" = ? ''', (im))
#     sql.commit()



urgency_length = 0
for i in range(len(alert)):
  if len(alert[i][1]) > urgency_length:
    urgency_length = len(alert[i][1])


city_length = 0
for i in range(len(alert)):
  if len(alert[i][3]) > city_length:
    city_length = len(alert[i][3])


proof = []
cur.execute(''' ALTER TABLE rpt_caprs_all ADD COLUMN "CAPRS URL" text ''')
sql.commit()
for i in range(len(alert)):
  im = str(alert[i][0])
  url_make.url_make(im, '1')
  cur.execute(''' UPDATE rpt_caprs_all SET "CAPRS URL" = ? WHERE "Incident ID" = ? ''',
              (settings.newURL, str(im)))
  sql.commit()

# TO-DO: Do you want to assign variables to the items below (e.g., t1 = "CARPS URL") to condense the following structures?
report013 = '"CAPRS URL", "Urgency", "City", "Master Incident", "Open Time", "Status", "Unsuspend Time", "Brief Description"'
report115 = '"CAPRS URL", "Urgency", "City", "Master Incident", "V1 URL #1", "Open Time", "Status", "Unsuspend Time", "Brief Description"'
report217 = '"CAPRS URL", "Urgency", "City", "Master Incident", "V1 URL #1", "V1 URL #2", "Open Time", "Status", "Unsuspend Time", "Brief Description"'
report319 = '"CAPRS URL", "Urgency", "City", "Master Incident", "V1 URL #1", "V1 URL #2", "V1 URL #3", "Open Time", "Status", "Unsuspend Time", "Brief Description"'
report421 = '"CAPRS URL", "Urgency", "City", "Master Incident", "V1 URL #1", "V1 URL #2", "V1 URL #3", "V1 URL #4", "Open Time", "Status", "Unsuspend Time", "Brief Description"'
report523 = '"CAPRS URL", "Urgency", "City", "Master Incident", "V1 URL #1", "V1 URL #2", "V1 URL #3", "V1 URL #4", "V1 URL #5", "Open Time", "Status", "Unsuspend Time", "Brief Description"'
report625 = '"CAPRS URL", "Urgency", "City", "Master Incident", "V1 URL #1", "V1 URL #2", "V1 URL #3", "V1 URL #4", "V1 URL #5", "V1 URL #6", "Open Time", "Status", "Unsuspend Time", "Brief Description"'
report727 = '"CAPRS URL", "Urgency", "City", "Master Incident", "V1 URL #1", "V1 URL #2", "V1 URL #3", "V1 URL #4", "V1 URL #5", "V1 URL #6", "V1 URL #7", "Open Time", "Status", "Unsuspend Time", "Brief Description"'
report829 = '"CAPRS URL", "Urgency", "City", "Master Incident", "V1 URL #1", "V1 URL #2", "V1 URL #3", "V1 URL #4", "V1 URL #5", "V1 URL #6", "V1 URL #7", "V1 URL #8", "Open Time", "Status", "Unsuspend Time", "Brief Description"'
report931 = '"CAPRS URL", "Urgency", "City", "Master Incident", "V1 URL #1", "V1 URL #2", "V1 URL #3", "V1 URL #4", "V1 URL #5", "V1 URL #6", "V1 URL #7", "V1 URL #8", "V1 URL #9", "Open Time", "Status", "Unsuspend Time", "Brief Description"'


dbschema = []
max_no_story = 0
for i in range(len(alert)):
  im = str(alert[i][0])
  v1 = ''
  related_v1 = []
  story_count = 0
  for x in range(len(settings.match_list)):
    if im == settings.match_list[x][1]:
      v1 = settings.match_list[x][0]
      related_v1.append(settings.match_list[x][0])
      if len(related_v1) > story_count:
        story_count = len(related_v1)
      if story_count > max_no_story:
        max_no_story = story_count
  if len(related_v1) > 0:
    for y in range(len(related_v1)):
      if [item for item in dbschema if ("V1 Story #{}".format(str(y + 1))) in item]:
        pass
      else:
        cur.execute(
            ''' ALTER TABLE rpt_caprs_all ADD COLUMN "V1 Story #{}" text '''.format(str(y + 1)))
        cur.execute(
            ''' ALTER TABLE rpt_caprs_all ADD COLUMN "V1 URL #{}" text '''.format(str(y + 1)))
        cur.execute(''' PRAGMA table_info(rpt_caprs_all)  ''')
        fetch = cur.fetchall()
        if len(fetch) > len(dbschema):
          dbschema = fetch
      cur.execute(''' UPDATE rpt_caprs_all SET "V1 Story #%s" = "%s" WHERE "Incident ID" = "%s" ''' % (
          str(y + 1), str(related_v1[y]), im))
      url_make.url_make(related_v1[y], '3')
      # print(settings.newURL)
      # try:
      cur.execute(''' UPDATE rpt_caprs_all SET "V1 URL #%s" = "%s" WHERE "Incident ID" = "%s" ''' % (
          str(y + 1), settings.newURL, im))
      # except sqlite3.OperationalError:
      #   pass
      cur.execute(
          ''' SELECT * FROM rpt_caprs_all WHERE "Incident ID" = "{}" '''.format(im))
      sql.commit()


if max_no_story == 0:
  addl = report013
if max_no_story == 1:
  addl = report115
if max_no_story == 2:
  addl = report217
if max_no_story == 3:
  addl = report319
if max_no_story == 4:
  addl = report421
if max_no_story == 5:
  addl = report523
if max_no_story == 6:
  addl = report625
if max_no_story == 7:
  addl = report727
if max_no_story == 8:
  addl = report829
if max_no_story == 9:
  addl = report931
cur.execute(
    ''' CREATE TABLE rpt_caprs_all_temp AS SELECT {} FROM rpt_caprs_all '''.format(addl))
cur.execute(''' DROP TABLE rpt_caprs_all ''')
cur.execute(''' ALTER TABLE rpt_caprs_all_temp RENAME TO rpt_caprs_all ''')
cur.execute(''' SELECT * FROM rpt_caprs_all ''')
proof.append(cur.fetchall())


if settings.system == 'mac' or settings.system == 'linux':
  rpt_all_CAPRS_csv = (settings.base + 'reports/rpt_all_CAPRS.csv')
elif settings.system == 'windows':
  rpt_all_CAPRS_csv = (settings.base + 'reports\\rpt_all_CAPRS.csv')
with open(rpt_all_CAPRS_csv, 'w') as output:      # , encoding='latin-1'
  writer = csv.writer(output, lineterminator='\n')
  addl = re.sub('\"', '', addl)
  writer.writerow(addl.split(sep=','))
  for row in proof:
    writer.writerows(row)


def previousCAPRS(setting):
  if setting == "Open":
  	previous = settings.OpenCAPRS
  if setting == "Suspended":
  	previous = settings.SuspendedCAPRS
  if setting == "Closed":
  	previous = settings.ClosedCAPRS
  return previous
	

def miniReport(col, setting, col2, setting2, col3, setting3, col4, setting4, status):
  if status == "*":
    cur.execute(''' SELECT COUNT(*) FROM rpt_caprs_all ''')
    recordCount = cur.fetchall()[0][0]
    # print('line 436 -', recordCount)
  else:
    cur.execute(''' SELECT COUNT(*) FROM rpt_caprs_all WHERE ("{}" LIKE "{}" OR "{}" LIKE "{}" OR "{}" LIKE "{}" OR "{}" LIKE "{}") AND Status = "{}" '''.format(col, setting, col2, setting2, col3, setting3, col4, setting4, status))
    recordCount = cur.fetchall()[0][0]
    # print('line 440 -', recordCount)
  return recordCount


# SELECT * FROM caprs_tickets WHERE ("Brief Description" LIKE "%Sev1%" OR "Brief Description" LIKE "WL%" OR Urgency LIKE "Sev 1") AND Status = "Closed"
# SELECT * FROM caprs_tickets WHERE ("Brief Description" LIKE "%Sev1%" OR "Brief Description" LIKE "%WL %" OR Urgency LIKE 1 OR "Initial Impact" LIKE 1) AND Status = "Closed"

settings.OpenCriticalCAPRS = miniReport("Brief Description", "%Sev1%", "Brief Description", "%WL %", "Urgency", "Sev1", "Initial Impact", 1, "Open")
settings.ClosedCriticalCAPRS = miniReport("Brief Description", "%Sev1%", "Brief Description", "%WL %", "Urgency", "Sev1", "Initial Impact", 1, "Closed")
settings.SuspendedCAPRS = miniReport("Brief Description", "%", "Brief Description", "%", "Brief Description", "%", "Brief Description", "%", "Suspended")
settings.OpenCAPRS = miniReport("Brief Description", "%", "Brief Description", "%", "Brief Description", "%", "Brief Description", "%", "Open")
settings.ClosedCAPRS = miniReport("Brief Description", "%", "Brief Description", "%", "Brief Description", "%", "Brief Description", "%", "Closed")
settings.AllCAPRS = miniReport("Brief Description", "%", "Brief Description", "%", "Brief Description", "%", "Brief Description", "%", "*")
previous.add_new(settings.OpenCAPRS, settings.SuspendedCAPRS, settings.ClosedCAPRS)

print('\nOpen Critical    {:4d} '.format(settings.OpenCriticalCAPRS))
print('Closed Critical  {:4d} '.format(settings.ClosedCriticalCAPRS))
print('Open Routine     {:4d} '.format(settings.OpenCAPRS - settings.OpenCriticalCAPRS))
print('Suspended        {:4d} '.format(settings.SuspendedCAPRS))
print('Closed Routine   {:4d} '.format(settings.ClosedCAPRS - settings.ClosedCriticalCAPRS))
print('TOTAL CAPRS      {:4d} \n\n'.format(settings.AllCAPRS))

# print('\nOpen   {:4d} | was {:4d} | delta {:2d}'.format(settings.OpenCAPRS, settings.OpenCAPRS_prior, (settings.OpenCAPRS - settings.OpenCAPRS_prior)))
# print('Suspend{:4d} | was {:4d} | delta {:2d}'.format(settings.SuspendedCAPRS, settings.SuspendedCAPRS_prior, (settings.SuspendedCAPRS - settings.SuspendedCAPRS_prior)))
# print('Closed {:4d} | was {:4d} | delta {:2d}'.format(settings.ClosedCAPRS, settings.ClosedCAPRS_prior, (settings.ClosedCAPRS - settings.ClosedCAPRS_prior)))
# print('Total  {:4d} | was {:4d} | delta {:2d}\n'.format((settings.OpenCAPRS + settings.ClosedCAPRS + settings.SuspendedCAPRS), (settings.OpenCAPRS_prior + settings.ClosedCAPRS_prior + settings.SuspendedCAPRS_prior), ((settings.OpenCAPRS_prior + settings.ClosedCAPRS_prior + settings.SuspendedCAPRS_prior) - (settings.OpenCAPRS + settings.ClosedCAPRS + settings.SuspendedCAPRS))))

sql.commit()
sql.close()


line_count = 0
if settings.system == 'mac' or settings.system == 'linux':
  rpt_all_CAPRS_csv = (settings.base + 'reports/rpt_all_CAPRS.csv')
  rpt_all_CAPRS_archive_csv = (settings.base + 'reports/archive/rpt_all_CAPRS{}.csv'.format(str(datetime.datetime.today().strftime("-%m-%d-%Y"))))
elif settings.system == 'windows':
  rpt_all_CAPRS_csv = (settings.base + 'reports\\rpt_all_CAPRS.csv')
  rpt_all_CAPRS_archive_csv = (settings.base + 'reports\\archive\\rpt_all_CAPRS{}.csv'.format(str(datetime.datetime.today().strftime("-%m-%d-%Y"))))
with open(rpt_all_CAPRS_csv, 'r', encoding='UTF8', errors='ignore') as output:
  reader = csv.reader(output, delimiter=',')
  lines = []
  for line in reader:
    oldline = line
    im = line[0][-10:]
    for x in range(len(oldline)):
      if oldline[x].startswith('http://dnnsoprod2.ba.ad.ssa.gov/ticketstatus/default.aspx?PMNum='):
        oldline[x] = "=HYPERLINK(\"http://dnnsoprod2.ba.ad.ssa.gov/ticketstatus/default.aspx?PMNum={}\",\"{}\")".format(str(line[x][-10:]), str(line[x][-10:]))
      if oldline[x].startswith('https://dcpsv1.ba.ssa.gov/VersionOne/assetdetail.v1?Number='):
        oldline[x] = "=HYPERLINK(\"https://dcpsv1.ba.ssa.gov/VersionOne/assetdetail.v1?Number={}\",\"{}\")".format(str(line[x][-7:]), str(line[x][-7:]))
        line[x] = oldline[x]
    lines.append(line)
  with open(rpt_all_CAPRS_csv, 'w', newline='', errors='ignore') as input:
    writer = csv.writer(input, delimiter=',')
    writer.writerows(lines)
shutil.copy(rpt_all_CAPRS_csv, rpt_all_CAPRS_archive_csv)
# os.remove(rpt_all_CAPRS_csv)
# os.rename(rpt_all_CAPRS2_csv, rpt_all_CAPRS_csv)



  # writer = csv.writer(output, lineterminator='\n')
  # addl = re.sub('\"', '', addl)
  # writer.writerow(addl.split(sep=','))
  # for row in proof:
  #   writer.writerows(row)


# line_count = 0
# marked_item = int(input("Enter the item number:"))
# with open("items.csv", 'r') as f:
    # reader = csv.reader(f, delimiter=',')
    # lines = []
    # for line in reader:
#         if len(line)>3 and line[3] == 'a':
#             line_count += 1
#             if marked_item == line_count:
#                 line[3] = 'b'
#         lines.append(line)
# with open("items.csv", 'w', newline='') as f:
#     writer = csv.writer(f, delimiter=',')
#     writer.writerow(title)
#     writer.writerows(lines)








# TO-DO --- Implement exception handling for database connection errors (reference below)


# Fri Dec 29 - 21:47:24 ❤️  :~ python3 convert.py
# Traceback (most recent call last):
#   File "convert.py", line 1, in <module>
#     import CAPRSdb
#   File "/Users/jrgarrigues/repos/caprs/CAPRSdb.py", line 18, in <module>
#     cur.execute('DROP TABLE IF EXISTS caprs_tickets')
# sqlite3.OperationalError: database is locked

# http://thepythonguru.com/handling-errors/



