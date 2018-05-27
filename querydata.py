# -*- coding: utf-8 -*-
# filename: querydata.py


import web
from dboperation import DBOperation





class TodaySaleDetails:
	def __init__(self):
		self.dbo = DBOperation()

	def GET(self):
		data = web.input(facility = none)
		facility = data.facility
		result = self.dbo.getTodaySaleOrderDetails('0201')
		colName = []
		for col in result[0]:
			colName.append(col)
		facility = web.template.frender("salesData.html")
		print data
		return facility("MIG事业部",result,colName)


if __name__ == '__main__':
	urls = (
		"/todaySaleDetails/(.*?)","TodaySaleDetails"
		)
	app = web.application(urls, globals())
	app.run()