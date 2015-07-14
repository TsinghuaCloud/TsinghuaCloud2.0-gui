import datetime
import time
import Mysql
import base64,urllib,httplib,json,os

import sys
if not "/usr/share/openstack-dashboard/openstack_dashboard/" in sys.path:
    sys.path.append("/usr/share/openstack-dashboard/openstack_dashboard/")
#if not 'get_ip' in sys.modules:
#    get_ip = __import__('get_ip')
#else:
#    eval('import get_ip')
#    get_ip = eval('reload(get_ip)')

import get_ip


class user:
	userid = ''
	username = ''
	password = ''
	tenantid = ''
	account = 0
	def __init__(self, uid, uname, up, tenant, ac):
		self.userid = uid
		self.username = uname
		self.password = up
		self.tenantid = tenant
		self.account = ac

ISOTIMEFORMAT='%Y-%m-%d %X'
def get_current_date():
	time1 = time.gmtime()
	time2 = time.strftime( ISOTIMEFORMAT,time1)
	time3 = time.strptime( time2, ISOTIMEFORMAT)
	time4 = time.mktime(time3)
	return time4

#process()
def deduct_daily(now, instanceid, unit_price, userid, instancename):
	sql = "update user_pay set updatetime = '%s' where instanceid = '%s'" % (now, instanceid)
	Mysql.updateData(sql)
	sql = "update user set account = account - '%s' where userid = '%s'" % (unit_price, userid)
	Mysql.updateData(sql)	
	sql = "insert into user_info (userid, instanceid, instancename, op, money, time) values ('%s', '%s', '%s', '-', '%s', '%s')" % (userid, instanceid, instancename, unit_price, now)
	Mysql.insertData(sql)

def get_user(userid):
	sql = "select * from user where userid = '%s' " % userid
	temp =  Mysql.selectData(sql)
	u = user(temp[0]['userid'], temp[0]['username'], temp[0]['password'], temp[0]['tenantid'], temp[0]['account'])
	return u
	
def set_status(instanceid, status):
	sql = "update user_pay set status = '%s' where instanceid = '%s'" % (status, instanceid)
	Mysql.updateData(sql)

def delete_instance(user, instanceid):
	ip = get_ip.get_one_ip('local_ip')
        url1="%s:5000" % (ip)
#	print url1
#        params1 ='{"auth": {"tenantName": "admin","passwordCredentials": { "username": "admin","password": "cloud"}}}'
        params1 ='{"auth": {"tenantName": "%s","passwordCredentials": { "username": "%s","password": "%s"}}}' % (user.username, user.username, user.password)
        headers1 = {"Content-Type": 'application/json'}
        conn1 = httplib.HTTPConnection(url1)
        conn1.request("POST","/v2.0/tokens",params1,headers1)
        response1 = conn1.getresponse()
        data1 = response1.read()
#token=response1.getheader('x-subject-token')
        dd1 = json.loads(data1)
        conn1.close()

        url2 = "%s:8774" % (ip)
        token= dd1['access']['token']['id']
        headers1 = {"X-Auth-Token":token,"Content-Type": 'application/json'}
        conn1 = httplib.HTTPConnection(url2)
#conn.request(method="POST",url=requrl,body=test_data_urlencode,headers = headerdata)  
#        info_project = '{"project": {"enabled": true,"name": "%s"}}'%(username)
        tenant_id = user.tenantid
        server_id = instanceid
        url_grant = '/v2/%s/servers/%s' % (tenant_id, server_id)
        conn1.request("DELETE", url_grant ,"",headers1)
        response1 = conn1.getresponse()
        data1 = response1.read()
    #    dd1 = json.loads(data1)
        conn1.close()
#       print dd1	



def get_user_pay():
	sql = "select * from user_pay"
	rows = Mysql.selectData(sql)
	now1 = get_current_date()
	now = datetime.datetime.fromtimestamp(now1)
	adminid = 'dff7def8e5314b2c8df8b2d639c666f5'
#	print "this is now:: '%s'" % now
	for row in rows:
	    if row['userid'] != adminid:	
#		print "this is row.time: '%s'" % row['updatetime']
		updatetime = row['updatetime']
		dd = now - updatetime
#		print "this is '%s' dd : '%s'" % (row['instancename'], dd)
#		print "this is dd.days: '%s'" % dd.days
#		print "this is dd.seconds : '%s'" % dd.seconds
#		print "this is time difference: '%s'" % dd
#		print "this is time.days:: '%s'" % dd.days	
#		print "this is time.seconds:: '%s'" % dd.seconds
#		account = get_current_account(row['userid'])
		u = get_user(row['userid'])	
#		print "this is u.accont : '%s'" % u.account
#		print "this is row['unit_price'] : %s'" % row['unit_price']
		
		if row['status'] == '1':	
#			print "trrrrrr"
			if u.account >= row['unit_price']:
				if (dd.days == 1) and (dd.seconds >= 0) and (dd.seconds <= 800):
#					print "true"
					deduct_daily(now, row['instanceid'], row['unit_price'], row['userid'], row['instancename'])
			else:
				status = '2'
				set_status(instanceid, status)
		if row['status'] == '2':
			if u.account >= row['unit_price']:
				deduct_daily(now, row['instanceid'], row['unit_price'], row['userid'], row['instancename'])		
		
				status = '1'				
				set_status( row['instanceid'], status)
			else:
				if (dd.days == 3) and (dd.seconds >= 0) and (dd.seconds <= 800):
					status = '3'
					set_status(row['instanceid'], status)
					
					delete_instance(u, row['instanceid'])
		

def process():
	while(1):
		get_user_pay()
		time.sleep(600)

process()


#get_user_pay()
