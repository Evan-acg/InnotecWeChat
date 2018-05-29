# -*- coding: utf-8 -*-
# filename: getinfo.py

import urllib
import urllib2
import json
from dboperation import DBOperation
from jsonoperation import ReadJson
import sys
reload(sys)
sys.setdefaultencoding("utf-8")




class Info(object):
	def __init__(self, appId, appSecret):
		self.appId = appId
		self.appSecret = appSecret
		self.dbo = DBOperation()

	def getAccessToken(self):
		url = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={0}&secret={1}".format(self.appId,self.appSecret)
		page = urllib.urlopen(url).read()
		pageJson = json.loads(page)
		print pageJson
		self.accessToken= pageJson["access_token"]
		self.dbo.insertAccessToken(self.accessToken)

	def getUser(self):
		url = "https://api.weixin.qq.com/cgi-bin/user/get?access_token={0}".format(self.accessToken)
		page = urllib.urlopen(url).read()
		pageJson = json.loads(page)
		self.userList = pageJson["data"]["openid"]
		self.nextID = pageJson["next_openid"] 

	def getUserName(self):
		url = "https://api.weixin.qq.com/cgi-bin/user/info/batchget?access_token={0}".format(self.accessToken)
		dataList = []
		for user in self.userList:
			data = {"openid":user, "lang": "zh_CN"}
			dataList.append(data)
		postData = {"user_list":dataList}
		postData = json.dumps(postData)
		req = urllib2.Request(url = url, data = postData)
		page = urllib2.urlopen(req).read()
		page = json.loads(page)
		infoList = page["user_info_list"]
		NameInfo = {}
		for info in infoList:
			NameInfo[info["openid"]] = info["nickname"]
		self.nameList = NameInfo

	def checkIPs(self):
		url = "https://api.weixin.qq.com/cgi-bin/getcallbackip?access_token={0}".format(self.accessToken)
		page = urllib.urlopen(url).read()
		pageJson = json.loads(page)
		IPDict = dict.fromkeys(pageJson["ip_list"])
		self.IPs = IPDict

	def mainControl(self):
		result = self.dbo.getAccessToken()
		if len(result) <= 0:
			self.getAccessToken()
		else:
			accessToken = result[0][0]
			expire = result[0][1]
		if expire >= 7150:
			self.getAccessToken()
		else:
			self.accessToken = result[0][0]
		self.getUser()
		self.getUserName()
		DBUserIDs = []
		for ID in self.dbo.getUserID():
			DBUserIDs.append(ID[0])
		DBUserIDs = dict.fromkeys(DBUserIDs)
		for ID in self.nameList.keys():
			if not DBUserIDs.has_key(ID):
				self.dbo.insertUserID(ID,self.nameList[ID])
		# self.checkIPs()
	def getX3UserInfo(self,X3UserName):
		self.X3NameList = self.dbo.getX3UserInfo(X3UserName)

	def bindX3(self,X3UserName):
		pass
		







if __name__ == '__main__':
	rj = ReadJson()
	filePath = "../../weChat.json"
	config = rj.readJson(filePath)
	appId = config["appId"]
	appSecret = config["appSecret"]
	gi = Info(appId,appSecret)
	gi.mainControl()
	# gi.getX3UserInfo("博文")
	for Name in gi.nameList:
		print Name
		print gi.nameList[Name]
