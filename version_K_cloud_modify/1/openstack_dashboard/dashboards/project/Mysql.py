#import MySQLdb
import MysqlDBConn
dbconn = MysqlDBConn.DBConn()


def createTable_user():
	dbconn.connect()
	cur = dbconn.cursor()
	sql = "CREATE TABLE user(id int(11) PRIMARY KEY NOT NULL auto_increment,userid varchar(64),accout real)"
	cur.execute(sql)
	dbconn.commit()
	cur.close() 
	dbconn.close()
	 

def createTable_info():
	dbconn.connect()
	cur = dbconn.cursor()
	sql = "CREATE TABLE user_info(id int(11) PRIMARY KEY NOT NULL auto_increment,userid varchar(255),instanceid varchar(255), op varchar(1), money real, time datetime)"
	try:
		cur.execute(sql)
		dbconn.commit()
	except:
#		dbconn.rollback()
		print "ccreateTable_info error"
	cur.close()
	dbconn.close()
	


def insertData(sql):
	dbconn.connect() 
	cur = dbconn.cursor()
#	sql = "insert into user(userid, accout) value('%s', '%s')"%("tutkj90908","1.5")
	try:
		cur.execute(sql)
		dbconn.commit()
	except:
		print "insertData error"	
	cur.close() 
	dbconn.close()
	
def selectData(sql):
	dbconn.connect()
	cur = dbconn.cursor()
	results = None
	try:  
		cur.execute(sql)
		results = cur.fetchall()
	except:
		print "Error : unable to fetch data "
	
	cur.close()
	dbconn.close()
	return results 

def updateData(sql):
	dbconn.connect()
	cur = dbconn.cursor()
	try:
		cur.execute(sql)
		dbconn.commit() 
	except:
		print "update the data error"
	cur.close()
	dbconn.close()

def deleteData(sql):
	dbconn.connect()
	cur = dbconn.cursor()
	try:
		cur.execute(sql)
		dbconn.commit() 
	except:
		print "delete data error"
	cur.close()
	dbconn.close()

def process():
#	dbconn.connect()
	#cur = dbconn.cursor();
	print "connect success!"
#	createTable()
#	createTable_info()
#	insertData()
	userid = "613fc5195889492ab531126bb5c77038"
	sql = "select * from user where userid = '%s'" % (userid)
        account = selectData(sql)
	print account

#	dbconn.close()
