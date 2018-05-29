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



class PushData(object):
	def __init__(self):
		filePath = "../../weChat.json"
		with open(filePath,"r") as jsonFile:
			weChatConfig = json.loads(jsonFile.read())
		self.gi = Info(weChatConfig["appId"],weChatConfig["appSecret"])
		self.gi.mainControl()

	def push(self,MSG,OPENID = "ocwHT08BbAJvZ2Lj9o-fu7JJKWIw"):
		url = "https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token={0}".format(self.gi.accessToken)
		content = {"content":MSG}
		postData = {
				"touser":OPENID,
				"msgtype":"text",
				"text":content
		}
		postData = json.dumps(postData,ensure_ascii=False)
		req = urllib2.Request(url = url, data = postData)
		page = urllib2.urlopen(req).read()
		print page




if __name__ == '__main__':
	filePath = "../public/facility.json"
	with open(filePath,"r") as jsonFile:
		fcyDict = json.loads(jsonFile.read())
	userDict = {
			# "罗博文":["ocwHT08BbAJvZ2Lj9o-fu7JJKWIw",["0101","0102"]],
			# "俞凯":["ocwHT0yHEKfRw39oKIPWIYAvWM_Q",["0101","0102","0201","0202","0203","0301","0401","0501"]],
			"顾蓉蓉":["ocwHT02aKru4DXzNq0Smg-2VYrWA",["0101","0201","0202","0203","0301","0401","0501"]]，
			"徐标":["ocwHT02hzAkhUnANysWlpHiQlTE4",["0701"]]，
			"王晓丽":["ocwHT09qxLNWr9FZ1pUonlkkLFvc",["0301"]]
			# "李俊":["ocwHT05GGGEaGvKP6NdVhuuyL7bI",["0301"]]
	}
	qd = Query(fcyDict)
	MSG = ""
	pd = PushData()
	for userName in userDict.keys():
		OPENID = userDict[userName][0]
		for fcy in userDict[userName][1]:
			MSG = qd.querySales(fcy)
			pd.push(MSG,OPENID)
			# print qd.querySales(fcy)
