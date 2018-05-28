# -*- coding: utf-8 -*-
# filename: querydata.py


import web
from dboperation import DBOperation
from getdate import GetDate
import json





class TodaySaleDetails:
	def __init__(self):
		self.dbo = DBOperation()

	def GET(self):
		filePath = "./public/facility.json"
		with open(filePath,"r") as jsonFile:
			facilityDict = json.loads(jsonFile.read(), encoding="utf-8")
		gd = GetDate()
		dateRange = gd.Today()
		data = web.input()
		colName = [
			"销售订单号",
			"销售订单行号",
			"产品代码",
			"产品数量",
			"毛价",
			"小计",
			"产品名称",
			"订单客户",
			"客户名称",
			"真实客户",
			"客户名称",
			"备注",
			"客户订单号",
			"客户订单行号"
		]
		result = self.dbo.getTodaySaleOrderDetails(data.facility)
		facility = web.template.frender("salesData.html")
		return facility(facilityDict[data.facility],result,colName,dateRange["start"])


if __name__ == '__main__':
	urls = (
		"/todaySaleDetails","TodaySaleDetails"
		)
	app = web.application(urls, globals())
	app.run()