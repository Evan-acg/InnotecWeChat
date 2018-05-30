# -*- coding: utf-8 -*-
# filename: querydata.py

import common
import web
import os
from Public.dboperation import DBOperation
from Public.getdate import GetDate
from Public.getexchangerate import GetExchangeRate
import json



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
		gd = GetDate()
		dateRange = gd.Today()
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
			MSG = MSG + "汇总数据:\n　　数量 :" + str(self.total["数量"]) + " PCS　\n　　金额约等于人民币 :" \
				+ str(self.total["金额"]) + "\n <a href = 'http://121.46.30.178/todaySaleDetails?facility=" + facility + "&date=" + dateRange["start"] +"'>点此查看明细</a>"
		self.total = {
					"金额":0.0,
					"数量": 0
		}
		return MSG.encode("utf-8")

class TodaySaleDetails:
	def __init__(self):
		self.dbo = DBOperation()

	def GET(self):
		filePath = os.path.dirname((os.path.dirname(__file__))) + "/Static/Json/facility.json"
		with open(filePath,"r") as jsonFile:
			facilityDict = json.loads(jsonFile.read(), encoding="utf-8")
		gd = GetDate()
		data = web.input()
		colName = [
			"客户名称",
			"销售订单号",
			"销售订单行号",
			"产品代码",
			"产品数量",
			"毛价",
			"小计",
			"产品名称",
			"订单客户",
			"真实客户",
			"客户名称",
			"备注",
			"客户订单号",
			"客户订单行号"
		]
		result = self.dbo.getTodaySaleOrderDetails(data.facility, data.date)
		randerTemplatePage = os.path.dirname((os.path.dirname(__file__))) + "/Static/Html/salesData.html"
		facility = web.template.frender(randerTemplatePage)
		return facility(facilityDict[data.facility],result,colName,data.date)


if __name__ == '__main__':
	urls = (
		"/todaySaleDetails","TodaySaleDetails"
		)
	app = web.application(urls, globals())
	app.run()