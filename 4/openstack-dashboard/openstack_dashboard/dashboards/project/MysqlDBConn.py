import MySQLdb
import MySQLdb.cursors
import sys

if not "/usr/share/openstack-dashboard/openstack_dashboard/" in sys.path:
    sys.path.append("/usr/share/openstack-dashboard/openstack_dashboard/")
#if not 'get_ip' in sys.modules:
#    get_ip = __import__('get_ip')
#else:
#    eval('import get_ip')
#    get_ip = eval('reload(get_ip)')

import get_ip
	
class DBConn:
	conn = None
	ip = get_ip.get_one_ip("database_ip")	
	def connect(self):
		self.conn= MySQLdb.connect(	
			host = self.ip,
			port = 3306,
			user='root',
			passwd='tsinghua',
			db ='test_zxl',
			cursorclass = MySQLdb.cursors.DictCursor 
			)
	def cursor(self):
		try:
			return self.conn.cursor()
		except (AttributeError, MySQLdb.OperationalError):
			self.connect()
			return self.conn.cursor()
	def commit(self):
		return self.conn.commit()	
	def close(self):
		return self.conn.close()

