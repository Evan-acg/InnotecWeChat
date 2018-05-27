# -*- coding: utf-8 -*-
# filename: getdate.py

import datetime

class GetDate(object):
	def __init__(self):
		self.today = datetime.datetime.now()

	def year(self,year):
		start = datetime.datetime(year,1,1)
		end = datetime.datetime(start.year + 1, 1, 1) - timedelta(days = 1)
		dateRange = {
				"start":start.strftime("%Y-%m-%d"),
				"end":end.strftime("%Y-%m-%d")
		}
		return dateRange

	def month(self,year,month):
		start = datetime.datetime(year,month,1)
		if start.month == 12:
			end = datetime.datetime(start.year + 1, 1, 1) - timedelta(days = 1)
		else:
			end = datetime.datetime(start.year,start.month + 1, 1) - timedelta(days = 1)
		dateRange = {
				"start":start.strftime("%Y-%m-%d"),
				"end":end.strftime("%Y-%m-%d")
		}
		return dateRange

	def season(self,year,season):
		seasonRange = [(1,3),(4,6),(7,9),(10,12)]
		start = self.month(year,seasonRange[season - 1][0]).start
		end = self.month(year,seasonRange[season - 1][1]).end
		dateRange = {
				"start":start,
				"end":end
		}
		return dateRange

	def Today(self):
		start = self.today
		end = self.today
		dateRange = {
				"start":start.strftime("%Y-%m-%d"),
				"end":end.strftime("%Y-%m-%d")
    #             "start":"2018-05-24",
				# "end":"2018-05-24"
		}
		return dateRange

	def thisYear(self):
		start = datetime.datetime(self.today.year, 1, 1)
		end = datetime.datetime(self.today.year + 1, 1, 1) - timedelta(days = 1)
		dateRange = {
				"start":start.strftime("%Y-%m-%d"),
				"end":end.strftime("%Y-%m-%d")
		}
		return dateRange

	def lastYear(self):
		start = datetime.datetime(self.today.year - 1, 1, 1)
		end = datetime.datetime(self.today.year, 1, 1) - timedelta(days = 1)
		dateRange = {
				"start":start.strftime("%Y-%m-%d"),
				"end":end.strftime("%Y-%m-%d")
		}
		return dateRange

	def thisMonth(self):
		start = datetime.datetime(self.today.year, self.today.month, 1)
		if start.month == 12:
			end = datetime.datetime(self.today.year + 1, 1, 1) - timedelta(days = 1)
		else:
			end = datetime.datetime(self.today.year,self.today.month + 1, 1) - timedelta(days = 1)
		dateRange = {
				"start":start.strftime("%Y-%m-%d"),
				"end":end.strftime("%Y-%m-%d")
		}
		return dateRange

	def lastMonth(self):
		if self.today.month == 1:
			start = datetime.datetime(self.today.year - 1,12,1)
		else:
			start = datetime.datetime(self.today.year, self.today.month - 1,1)
		end = datetime.datetime(self.today.year, self.today.month, 1) - timedelta(days = 1)
		dateRange = {
				"start":start.strftime("%Y-%m-%d"),
				"end":end.strftime("%Y-%m-%d")
		}
		return dateRange
