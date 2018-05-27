# -*- coding: utf-8 -*-
# filename: querydata.py


import web
from dboperation import DBOperation





class TodaySaleDetails:
	def __init__(self):
		self.dbo = DBOperation()

	def GET(self):

		result = self.dbo.getTodaySaleOrderDetails('0201')
		colName = []
		for col in result[0]:
			colName.append(col)
		render = web.template.frender("salesData.html")
		return render("MIG事业部",result,colName)


if __name__ == '__main__':
	urls = (
		"/todaySaleDetails","TodaySaleDetails"
		)
	app = web.application(urls, globals())
	app.run()