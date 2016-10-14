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
		self.ssh_client_pwd = "al"
		#self.rwdimg="openwrt-ar71xx-generic-ap147-16M-squashfs-sysupgrade_v1.2.14_redwood-2.6.030.bin"
		#self.satimg="openwrt-ar71xx-generic-ap152-32M-squashfs-sysupgrade_v1.2.14_saturn-1.4.028.bin"
		self.rwdimg="openwrt-ar71xx-generic-ap147-16M-squashfs-sysupgrade_v1.0.128_redwood-2.4.040.bin"
		self.satimg="openwrt-ar71xx-generic-ap152-32M-squashfs-sysupgrade_v1.0.128_saturn-1.2.044.bin"
		self.rwdsrcdir="/home/ivts/GetMeshInfo/"+self.rwdimg
		self.satsrcdir="/home/ivts/GetMeshInfo/"+self.satimg
		self.destdit="/tmp/."

	def connectToHost(self, slave):
		self.client = paramiko.SSHClient()
		self.client.set_missing_host_key_policy(client.AutoAddPolicy())
		self.client.connect(slave, 22,  self.ssh_client_user, self.ssh_client_pwd)

	def getRWDIP(self):
		#RWD=["00:78:cd:00:1a:94","00:78:cd:00:19:ec","00:78:cd:00:1c:00"]
		RWD=["00:78:cd:00:1a:94"]
		#RWD=["00:78:cd:00:0e:20"]
		rwdcontent = []
		for ix in range(0,(len(RWD)),1):
			stdin, stdout, stderr = self.client.exec_command("cat /proc/net/arp | grep "+ RWD[ix] +"| awk '{print $1}'")
			iip = stdout.readlines()
			rwdcontent += iip
			print ''.join(iip) + "Download Redwood Image"
			self.Scpimg(''.join(iip),self.rwdsrcdir)
		print rwdcontent
		for ix in range((len(RWD)-1),-1,-1):
			print ''.join(rwdcontent[ix]) + "Redwood Image Upgrade"
			self.upgrade(''.join(rwdcontent[ix]),self.rwdimg)

	def PortalIP(self):
		#PORTAL=["00:78:cd:00:13:b0","00:78:cd:00:15:2c","00:78:cd:00:13:00"]
		PORTAL=["00:78:cd:00:13:b0"]
		#PORTAL=["00:78:cd:00:08:14"]
		saturncontent = []
		for ix in range(0,(len(PORTAL)),1):
			stdin, stdout, stderr = self.client.exec_command("cat /proc/net/arp | grep "+ PORTAL[ix] +"| awk '{print $1}'")
			iip = stdout.readlines()
			if iip :
				print iip			
			else :
				iip = ["192.168.8.1"]	
			saturncontent += iip
			#self.ScpLog(''.join(iip))
			#os.system("cp /home/ivts/GetMeshInfo/rwdagent.log /home/ivts/GetMeshInfo/rwdagent.log." + `ix`)
			self.close()
			print ''.join(iip)+"Download Saturn Image\n"
			self.Scpimg(''.join(iip),self.satsrcdir)
		for ix in range((len(PORTAL)-1),-1,-1):
			print ''.join(saturncontent[ix])+"Saturn Image Upgrade\n"
			self.upgrade(''.join(saturncontent[ix]),self.satimg)

	def ScpLog(self,slave):
		self.ssh = paramiko.SSHClient()
		self.ssh.set_missing_host_key_policy(client.AutoAddPolicy())
		self.ssh.connect(slave, 22,  self.ssh_client_user, self.ssh_client_pwd)
		self.scp = SCPClient(self.ssh.get_transport())
		self.scp.get('/tmp/rwdagent.log')
		self.scp.close()

	def Scpimg(self,slave,slave1):
		self.ssh = paramiko.SSHClient()
		self.ssh.set_missing_host_key_policy(client.AutoAddPolicy())
		self.ssh.connect(slave, 22,  self.ssh_client_user, self.ssh_client_pwd)
		self.scp = SCPClient(self.ssh.get_transport())
		self.scp.put(slave1,self.destdit)
		self.scp.close()

	def upgrade(self,slave,slave1):
		self.connectToHost(slave)
		stdin, stdout, stderr = self.client.exec_command('cd /tmp;sysupgrade ' + slave1)
		for line in stdout:
			if "Reboot" in line:
				self.close()
				print "Reboot..."
				

	def close(self):
		self.ssh = paramiko.SSHClient()
		if self.ssh:
			self.ssh.close()

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
