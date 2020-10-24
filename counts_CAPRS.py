# counts_CAPRS.py - provides a count of CAPRS tickets for the weekly reports

import sqlite3
import csv
import datetime
from datetime import datetime


sql = sqlite3.connect('caprs-v1.db')
cur = sql.cursor()
now = datetime.datetime.now()
datetime_object = datetime.strptime(now, '%m/%d/%y %H:%M:%S')
print(datetime_object)




cur.execute(
    ''' SELECT "Incident ID", "Urgency", "Open Time", "City", "Brief Description", "Contact", "Status" FROM 'caprs_tickets' WHERE "Open Time" LIKE "12/__/17%" ''')
story = cur.fetchall()
sql.commit()

print(len(story))
print(story)

# (SELECT DATETIME('now', '-7 day'))     , detect_types = sqlite3.PARSE_DECLTYPES

# for i in range(len(story)):
#     if str(story[i][1]).startswith('IM1'):
#         # print(story[i][0][:7], story[i][1][:10])
#         validation_list.append([story[i][0][:7], story[i][1][:10]])
#     if str(story[i][2]).startswith('IM1'):
#         # print(story[i][0][:7], story[i][2][:10])
#         validation_list.append([story[i][0][:7], story[i][2][:10]])


# cur.execute(
#     ''' SELECT "Incident ID", Solution FROM caprs_tickets WHERE Solution GLOB "*S-[0-9][0-9][0-9][0-9][0-9]*" OR Solution GLOB "*D-[0-9][0-9][0-9][0-9][0-9]*" ''')
# alert = cur.fetchall()
# sql.commit()
# for i in range(len(alert)):
#     carve = alert[i][1]
#     carved = carve.split()
#     for x in range(len(carved)):
#         if carved[x].startswith('S-') and [carved[x][:7], alert[i][0][:10]] not in validation_list:
#             # print(carved[x][:7], alert[i][0][:10])
#             print('\n***CAPRS ALERT***')
#             print('The following CAPRS ticket has references to a V1 Story/Defect, but is not officially \'associated\' with it in the VersionOne application. Please check it out:\nIncident ID:',
#                   alert[i][0][:10], '\nStory/Defect:', carved[x][:7], '\nSolution:', alert[i][1], '\n')
# for i in range(len(alert)):
#     carve = alert[i][1]
#     carved = carve.split()
#     for x in range(len(carved)):
#         if carved[x].startswith('D-') and [carved[x][:7], alert[i][0][:10]] not in validation_list:
#             # print(carved[x][:7], alert[i][0][:10])
#             print('\n***CAPRS ALERT***')
#             print('The following CAPRS ticket has references to a V1 Story/Defect, but is not officially \'associated\' with it in the VersionOne application. Please check it out:\nIncident ID:',
#                   alert[i][0][:10], '\nStory/Defect:', carved[x][:7], '\nSolution:', alert[i][1], '\n')


sql.close()
