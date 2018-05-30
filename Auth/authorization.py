# -*- coding: utf-8 -*-
# filename: authorization.py

import common
from Public.jsonoperation import ReadJson
from Public.dboperation import DBOperation


class Authorization:
	def __init__(self):
		self.rj = ReadJson()
		self.dbo = DBOperation()


	def authorize(self, OPENID, facility):
		self.dbo.authorize(OPENID, facility)
	def deauthorize(self):
		self.dbo.deauthorize()

	def run(self):
		fielPath = "../NameList.json"
		NameList = self.rj.readJson(fielPath)
		self.dbo.deauthorize()
		for Name in NameList:
			OPENID = NameList[Name]["OPENID"]
			facility = NameList[Name]["facility"]
			for fcy in facility:
				self.authorize(OPENID, fcy)




if __name__ == '__main__':
	auth = Authorization()
	auth.run()
