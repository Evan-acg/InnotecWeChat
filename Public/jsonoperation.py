# -*- coding: utf-8 -*-
# filename: jsonoperation.py




import simplejson



class ReadJson:
	def readJson(self, filePath):
		with open(filePath, "r") as jsonFile:
			jsonOrganizetion = simplejson.loads(jsonFile.read(), encoding = "utf-8")
		return	jsonOrganizetion
	
