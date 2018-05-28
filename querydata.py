# -*- coding: utf-8 -*-
# filename: querydata.py


import web
from dboperation import DBOperation





class TodaySaleDetails:
	def __init__(self):
		self.dbo = DBOperation()

	def GET(self):
		data = web.input()
		colName = [
			"销售订单号",
			"销售订单行号",
			"产品代码",
			"产品数量"
		]
		result = self.dbo.getTodaySaleOrderDetails(data.facility)
		facility = web.template.frender("salesData.html")
		return facility("MIt事业部",result,colName)


if __name__ == '__main__':
	urls = (
		"/todaySaleDetails","TodaySaleDetails"
		)
	app = web.application(urls, globals())
	app.run()