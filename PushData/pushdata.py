# -*- coding: utf-8 -*-
# filename: pushdata.py

import sys
sys.path.append("../")

import urllib2
import json
from Public.dboperation import DBOperation
from Public.getinfo import Info
from Public.getdate import GetDate
from decimal import Decimal
from Public.getexchangerate import GetExchangeRate
from PushData.querydata import Query
from Public.jsonoperation import ReadJson



class PushData(object):
	def __init__(self):
		filePath = "../../weChat.json"
		with open(filePath,"r") as jsonFile:
			weChatConfig = json.loads(jsonFile.read())
		self.gi = Info(weChatConfig["appId"],weChatConfig["appSecret"])
		self.gi.mainControl()

	def push(self,MSG,OPENID = "ocwHT08BbAJvZ2Lj9o-fu7JJKWIw"):
		url = "https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token={0}".format(self.gi.accessToken)
		content = {"content":MSG.encode("utf-8")}
		postData = {
				"touser":OPENID,
				"msgtype":"text",
				"text":content
		}
		postData = json.dumps(postData,ensure_ascii=False)
		postData = postData.encode("utf-8")
		req = urllib2.Request(url = url, data = postData)
		page = urllib2.urlopen(req).read()
		print page




if __name__ == '__main__':
	rj = ReadJson()
	dbo = DBOperation()
	filePath = "../public/facility.json"
	fcyDict = rj.readJson(filePath)
	userDict = dbo.getAuthList()
	qd = Query(fcyDict)
	pd = PushData()
	for userName in userDict:
		OPENID = userName[0]
		facility = userName[2]
		message = qd.querySales(facility)
		pd.push(message,OPENID)
		# 	# print qd.querySales(fcy)
