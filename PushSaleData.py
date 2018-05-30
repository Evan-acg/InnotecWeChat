# -*- coding: utf-8 -*-
# filename: PushSaleData.py

import common
from PushData.pushdata import PushSaleData
from Public.jsonoperation import ReadJson
from Public.dboperation import DBOperation
from PushData.querydata import Query
from PushData.pushdata import PushSaleData



class RunPushSales(PushSaleData):
	pass


if __name__ == '__main__':
	rj = ReadJson()
	dbo = DBOperation()
	filePath = "./Static/Json/facility.json"
	fcyDict = rj.readJson(filePath)
	userDict = dbo.getAuthList()
	qd = Query(fcyDict)
	pd = PushSaleData()
	for userName in userDict:
		OPENID = userName[0]
		facility = userName[2]
		message = qd.querySales(facility)
		pd.push(message,OPENID)