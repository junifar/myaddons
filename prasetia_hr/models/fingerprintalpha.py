import sys
import time
from zk import ZK, const
from pprint import pprint


def checkIP(ip):
    conn = None
    zk = ZK(ip, port=4370, timeout=5)
    try:
        print('Connecting to device')
        conn = zk.connect()
        print('Disabling device')
        conn.disable_device
        print("Firmware Version: : {}".format(conn.get_firmware_version()))
        users = conn.get_users()
        for user in users:
            # print dir(user)
            print str(user.uid) + ' - ' + user.name

            # attendances = conn.get_attendance()
            # for attendance in attendances:
            # 	print attendance.user_id + ' - ' + str(attendance.timestamp) + ' - ' + str(attendance.status)

    except Exception as e:
        print("Process terminate IP %s : {}".format(e) % (ip))
    finally:
        if conn:
            conn.disconnect()


# for i in range(0,255):
#	checkIP('192.168.1.' + str(i))
checkIP('192.168.1.220')


# conn = None
# zk = ZK("192.168.1.220", port=4370, timeout=5)
# try:
# 	print 'Connecting to device'
# 	conn = zk.connect()
# 	print 'Disabling device'
# 	conn.disable_device
# 	print 'Firmware Version: : {}'.format(conn.get_firmware_version())
# 	users = conn.get_users()
# 	for user in users:
# 		print user.name
# except Exception, e:
# 	print "Process terminate : {}".format(e)
# finally:
# 	if conn:
# 		conn.disconnect()
