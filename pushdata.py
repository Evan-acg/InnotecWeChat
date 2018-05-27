# -*- coding: utf-8 -*-
# filename: pushdata.py


import urllib2
import json
from dboperation import DBOperation
from getinfo import Info
from getdate import GetDate
from decimal import Decimal
from getexchangerate import GetExchangeRate



class PushData(object):
	def __init__(self,accessToken):
		self.accessToken = accessToken

	def push(self,OPENID,MSG):
		url = "https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token={0}".format(self.accessToken)
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
class Query(object):
	def __init__(self,facilityDict):
		self.dbo = DBOperation()
		self.fcyDict = facilityDict
		self.ger = GetExchangeRate()
		self.total = {
					"金额":0.0,
					"数量": 0
		}

	def getSaleTotal(self,facility):
		symbolList = [":",",",";"]
		ResultDict = {}
		Result = self.dbo.getOEMSaleTodayTotal(facility)
		for row in Result:
			MSG = ""
			i = 0
			for col in row:
				if i >= 2:
					MSG = MSG + u"约等于人民币:" + str(col) + symbolList[i]
				else:
					MSG = MSG + str(col) + symbolList[i]
				i += 1
			ResultDict[row[0]] = MSG
			self.total["金额"] = self.total["金额"] + float(row[2])
		return ResultDict

	def getSaleQuantity(self,facility,cur):
		ResultDict = {}
		Result = self.dbo.getTodayQuantity(facility,cur)
		for row in Result:
			MSG = ""
			if row[0] == 0:
				MSG = MSG + "枪: " + str(row[1]) + u" PCS;"
			elif row[0] == 2:
				MSG = MSG + "配件: " + str(row[1]) + u" PCS;"
			ResultDict[row[0]] = MSG
			self.total["数量"] = self.total["数量"] + int(row[1])
		if len(ResultDict) <= 0:
			return None
		else:
			return ResultDict

	def querySales(self,facility):
		rate = self.dbo.selectExchangeRate()
		if len(rate) <= 0:
			self.ger.mainControl()
		amountResult = self.getSaleTotal(facility)
		if len(amountResult) <= 0:
			MSG =  "今天[{0}]没有订单录入！".format(self.fcyDict[facility])
		else:
			MSG = "今天[{0}]的订单情况如下： \n".format(self.fcyDict[facility])
			for cur in amountResult.keys():
				MSG = MSG + "金额:\n"
				MSG = MSG + "　　" + amountResult[cur] + '\n' + u"　　数量:\n"
				quantityResult = self.getSaleQuantity(facility,cur)
				for quantity in quantityResult.keys():
					MSG = MSG + "　　　　" + quantityResult[quantity] + u"\n"
			MSG = MSG + "汇总数据:\n　　数量 :" + str(self.total["数量"]) + " PCS　\n　　金额约等于人民币 :" + str(self.total["金额"])  + "\n http://121.46.30.178/todaySaleDetails"
		self.total = {
					"金额":0.0,
					"数量": 0
		}
		return MSG.encode("utf-8")



if __name__ == '__main__':
	fcyDict = {
				"0101":"OEM事业部",
				"0102":"品牌事业部",
				"0201":"MIG事业部",
				"0202":"TIG事业部",
				"0203":"PLA事业部",
				"0301":"配件事业部",
				"0401":"水冷事业部",
				"0501":"空冷事业部"
	}
	userDict = {
			"罗博文":["ocwHT08BbAJvZ2Lj9o-fu7JJKWIw",["0101"]]
			# "俞凯":["ocwHT0yHEKfRw39oKIPWIYAvWM_Q",["0101","0102","0201","0202","0203","0301","0401","0501"]]
			# "李俊":["ocwHT05GGGEaGvKP6NdVhuuyL7bI",["0301"]]
	}
	qd = Query(fcyDict)
	appId = "wx30052641bcd38b10"
	appSecret = "19f693b0ce091511374fc698f93cdcf5"
	MSG = ""
	gi = Info(appId,appSecret)
	gi.mainControl()
	pd = PushData(gi.accessToken)
	for userName in userDict.keys():
		OPENID = userDict[userName][0]
		for fcy in userDict[userName][1]:
			MSG = qd.querySales(fcy)
			pd.push(OPENID,MSG)
			# print qd.querySales(fcy)
