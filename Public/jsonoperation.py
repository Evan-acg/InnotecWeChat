# -*- coding: utf-8 -*-
# filename: jsonoperation.py




import json



class ReadJson:
	def readJson(self, filePath):
		with open(filePath, "r") as jsonFile:
			jsonOrganizetion = json.loads(jsonFile.read(), encoding = "utf-8")
		return	jsonOrganizetion
	
