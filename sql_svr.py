import timing
import pyodbc


con = pyodbc.connect("Driver={SQL Server};Server=AGL-TLS-CTS-01.ba.ad.ssa.gov,55150;Database=pVersionone_DCPS;Trusted_Connection=yes;")
cur = con.cursor()
# this one captures the IM number from the FoundBy column for defects...
cur.execute(''' SELECT Value FROM pVersionone_DCPS.dbo.String WHERE ID IN (SELECT FoundBy FROM pVersionone_DCPS.dbo.String) ''')
# cur.execute(''' SELECT ID, AuditBegin, AssetType, AssetID, AssetTypeName, Name, Implementation, Validator FROM pVersionone_DCPS.dbo.Operation WHERE AuditEnd = 19860 ''')
Drows = cur.fetchall()
for row in Drows:
	print(row)
print(len(Drows))



# SELECT ID, Value, Value_ FROM pVersionone_DCPS.dbo.LongString;
# SELECT ID, AuditBegin, AssetType, AuditEnd, Name, URL, OnMenu, AssetID, AssetState FROM pVersionone_DCPS.dbo.Link
# SELECT ID, AuditBegin, AssetType, AuditEnd, Name, Description, AssetState, ColorName, TeamID FROM pVersionone_DCPS.dbo.List
# SELECT ID, AuditBegin, AssetType, AuditEnd, Name, Description, AssetState FROM pVersionone_DCPS.dbo.Label
# SELECT ID, AuditBegin, AssetType, AssetID, AssetTypeName, Name, Implementation, Validator FROM pVersionone_DCPS.dbo.Operation_Now
# SELECT ID, AuditBegin, AssetType, AuditEnd, Name, Description, AssetState, SubState FROM pVersionone_DCPS.dbo.BaseAsset
# SELECT ID, AuditBegin, AssetType, AuditEnd, Name, AssetID, AssetState FROM pVersionone_DCPS.dbo.Link
# SELECT ID, AuditBegin, AssetType, Name, BaseID, ShortNameAttribute, Initializer FROM pVersionone_DCPS.dbo.AssetType_Now



# SELECT Value FROM pVersionone_DCPS.dbo.String WHERE ID IN (SELECT Benefits FROM pVersionone_DCPS.dbo.Story);
# SELECT Value FROM pVersionone_DCPS.dbo.String WHERE ID IN (SELECT FoundBy FROM pVersionone_DCPS.dbo.Defect);
# SELECT Value FROM pVersionone_DCPS.dbo.String WHERE ID IN (SELECT Name FROM pVersionone_DCPS.dbo.AssetType_Now);
# SELECT Value FROM pVersionone_DCPS.dbo.String WHERE ID IN (SELECT FixedInBuild FROM pVersionone_DCPS.dbo.Defect);
# SELECT Value FROM pVersionone_DCPS.dbo.String WHERE ID IN (SELECT FoundInBuild FROM pVersionone_DCPS.dbo.Defect);
# SELECT Value FROM pVersionone_DCPS.dbo.String WHERE ID IN (SELECT CustomerID FROM pVersionone_DCPS.dbo.Story);
# SELECT Value FROM pVersionone_DCPS.dbo.String WHERE ID IN (SELECT CategoryID FROM pVersionone_DCPS.dbo.Story);
# cur.execute(''' SELECT * FROM PrimaryWorkitem ''') # sys.tables 
# cur.execute(''' SELECT ID,  AssetType FROM pVersionone_DCPS.dbo.Defect WHERE AssetType LIKE 'Defect' ''')





# cur.execute(''' SELECT ID, AssetType FROM pVersionone_DCPS.dbo.Story WHERE AssetType LIKE 'Story' ''')
# Srows = cur.fetchall()
# for row in Srows:
# 	print(row)


# print(len(Srows))



# item = cur.fetchall()
# print('item count =',len(item))
# story = 0 
# defect = 0
# for line in item:
# 	if line[1] == "Story":
# 		story += 1
# 	elif line[1] == "Defect":
# 		defect += 1

# print('Stories: ' + str(story))
# print('Defects: ' + str(defect))




# cur.execute(''' SELECT * FROM defect ''') # sys.tables
# defect_ticket = cur.fetchall()
# for line in defect_ticket:
# 	print(line)


# cur.execute(''' SELECT * FROM story ''') # sys.tables
# story_ticket = cur.fetchall()
# for line in story_ticket:
# 	print(line)


# print("\nStory Count = ",len(story_ticket))
# print("Defect Count = ",len(defect_ticket),"\n","-"*25)
# print("Total Count = ",len(defect_ticket + story_ticket),"\n")
# con.close()



# Getting table schema from VersionOne

# import pyodbc
# con = pyodbc.connect("Driver={SQL Server};Server=AGL-TLS-CTS-01.ba.ad.ssa.gov,55150;Database=pVersionone_DCPS;Trusted_Connection=yes;")
# cur = con.cursor()
# cur.tables()
# rows = cur.fetchall()
# for row in rows:
# 	print(row.table_name)




# Getting column names from VersionOne tables

# import pyodbc
# con = pyodbc.connect("Driver={SQL Server};Server=AGL-TLS-CTS-01.ba.ad.ssa.gov,55150;Database=pVersionone_DCPS;Trusted_Connection=yes;")
# cur = con.cursor()
# for row in cur.columns(table='Workitem'):
# 	print(row.column_name)





# Getting SQL Server version info

# import pyodbc
# con = pyodbc.connect("Driver={SQL Server};Server=AGL-TLS-CTS-01.ba.ad.ssa.gov,55150;Database=pVersionone_DCPS;Trusted_Connection=yes;")
# cur = con.cursor()
# cur.execute(''' SELECT @@version ''')
# ver = cur.fetchall()
# print(ver)



# "Name",
# "Display Id", story.ID or defect.ID
# "Type", story.AssetType or defect.AssetType
# "Requested By", 
# "Found By", defect.FoundBy
# "State",
# "Team Name",
# "Portfolio Item Display Id",
# "Created By Name",
# "Core?",
# "Closed Date",
# "Closed By Name",
# "Release Name"




# columns = [column[0] for column in cursor.description]


# This one finds the "Name" field from V1export.csv:
# cur.execute(''' SELECT ID, Value, Value_ FROM pVersionone_DCPS.dbo.String WHERE Value LIKE 'Refine Test Strategies' ''')

