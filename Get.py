import os
import sys
import time
import urllib2
import re
import paramiko
from paramiko import client
from paramiko import SSHClient
from scp import SCPClient


class GetInfo(object):
	client = None
	def __init__(self):
		self.ssh_client_host = "192.168.8.1"
		self.redwood_host = "192.168.8.100"
		self.ssh_client_user = "root"
		self.ssh_client_pwd = "CassiniRedwwod42562072Portal"

	def connectToHost(self, slave):
		self.client = paramiko.SSHClient()
		self.client.set_missing_host_key_policy(client.AutoAddPolicy())
		self.client.connect(slave, 22,  self.ssh_client_user, self.ssh_client_pwd)

	def getRWDIP(self):
		RWD=["00:78:cd:00:1a:94","00:78:cd:00:19:ec","00:78:cd:00:1c:00"]
		content = []
		ip = []
		for ix in range(0,(len(RWD)),1):
			print ix
			stdin, stdout, stderr = self.client.exec_command("cat /proc/net/arp | grep "+ RWD[ix] +"| awk '{print $1}'")
			print stdout.read()

	def PortalIP(self):
		PORTAL=["00:78:cd:00:13:b0","00:78:cd:00:15:2c","00:78:cd:00:13:00"]
		saturncontent = []
		ip = ""
		for ix in range(0,(len(PORTAL)),1):
			print ix
			stdin, stdout, stderr = self.client.exec_command("cat /proc/net/arp | grep "+ PORTAL[ix] +"| awk '{print $1}'")
                        iip = stdout.readlines()
			if iip :
				print iip
			else:
				iip = ["192.168.8.1"]
				print iip
                        saturncontent += iip
                        self.ScpLog(''.join(iip))
                        os.system("cp /home/ivts/GetMeshInfo/rwdagent.log /home/ivts/GetMeshInfo/rwdagent.log." + `ix`)

	def ScpLog(self,slave):
                print "ip=" + slave
		self.ssh = paramiko.SSHClient()
		self.ssh.set_missing_host_key_policy(client.AutoAddPolicy())
		self.ssh.connect(slave, 22,  self.ssh_client_user, self.ssh_client_pwd)
		self.scp = SCPClient(self.ssh.get_transport())
		self.scp.get('/tmp/rwdagent.log')
		self.scp.close()

if __name__ == '__main__':
	get = GetInfo()
	get.connectToHost("192.168.8.1")
	print "Portal RWD IP"
	get.getRWDIP()
	print "Portal IP"
	get.PortalIP()
	#get.ScpLog()
	#print "MeshAP1 RWD IP"
	#get.getIP("00:78:cd:00:19:ec")
	#print "MeshAP2 RWD IP"
	#get.getIP("00:78:cd:00:1c:00")
