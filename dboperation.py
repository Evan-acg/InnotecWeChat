# -*- coding: utf-8 -*-
# filename: dboperation.py



from dbconnection import DBConnection
from getdate import GetDate

class DBOperation(object):
	def __init__(self):
		self.dbc = DBConnection()
		self.getDate = GetDate()

	def insertAccessToken(self,accessToken):
		SQL = """INSERT INTO WECHATACTO(ACCESSTOKEN_0,CREDATTIM_0,UPDDATTIM_0,AUUID_0,CREUSR_0,UPDUSR_0) 
			VALUES(N'{0}',GETDATE(),GETDATE(),NEWID(),N'ADMIN',N'ADMIN')""".format(accessToken)
		self.dbc.execute(SQL)

	def getAccessToken(self):
		SQL = u"SELECT TOP 1 ACCESSTOKEN_0,DATEDIFF(SECOND,CREDATTIM_0,GETDATE()) EXPIRE FROM WECHATACTO ORDER BY CREDATTIM_0 DESC"
		return self.dbc.Query(SQL)

	def getUserID(self):
		SQL = u"SELECT USERID_0 FROM WECHATUSER"
		return self.dbc.Query(SQL)

	def insertUserID(self,ID, userName):
		SQL = u"""INSERT INTO WECHATUSER(USERID_0,USERNAME_0,CREDATTIM_0,UPDDATTIM_0,AUUID_0,CREUSR_0,UPDUSR_0)
			VALUES(N'{0}',N'{1}',GETDATE(),GETDATE(),NEWID(),N'ADMIN',N'ADMIN')""".format(str(ID),str(userName))
		self.dbc.execute(SQL)

	def getX3UserInfo(self,X3UserName):
		SQL = u"SELECT USR_0,NOMUSR_0 FROM AUTILIS WHERE NOMUSR_0 LIKE N'%{0}%'".format(X3UserName)
		return self.dbc.Query(SQL)
		
	def getOEMSaleTodayTotal(self,facility):
		dateRange = self.getDate.Today()
		SQL = u"""
				SELECT T3.TEXTE_0,
						CONVERT(DECIMAL(18,2),SUM(T1.ORDINVATI_0)) ORDINVATI_0,
						CONVERT(DECIMAL(18,2),SUM(ISNULL(T1.ORDINVATI_0 * T2.RATE_0,T1.ORDINVATI_0))) PRORATE_0
				FROM SORDER T1
					LEFT JOIN EXCHANGERATE T2 ON T1.CUR_0 = T2.CURRENCYFROM_0 AND T2.CREDAT_0 BETWEEN N'{1}' AND N'{2}'
					LEFT JOIN ATEXTRA T3 ON T1.CUR_0 = T3.IDENT1_0 AND T3.LANGUE_0 = N'CHI' AND T3.ZONE_0 = N'INTDES'
				WHERE T1.SALFCY_0 = N'{0}'
					AND T1.CREDAT_0 BETWEEN N'{1}' AND N'{2}'
				GROUP BY T3.TEXTE_0
			""".format(facility,dateRange["start"],dateRange["end"])
		return self.dbc.Query(SQL)
	def insertExchangeRate(self,erFrom,erTo,rate):
		dateRange = self.getDate.Today()
		SQL = u'''
				INSERT INTO EXCHANGERATE(CURRENCYFROM_0,CURRENCYTO_0,CREDAT_0,RATE_0,CREDATTIM_0,UPDDATTIM_0,AUUID_0,CREUSR_0,UPDUSR_0)
						VALUES(N'{0}',N'{1}',N'{2}',N'{3}',GETDATE(),GETDATE(),NEWID(),N'ADMIN',N'ADMIN')
				'''.format(erFrom,erTo,dateRange["start"],rate)
		self.dbc.execute(SQL)

	def getTodayQuantity(self,facility,cur):
		dateRange = self.getDate.Today()
		SQL = u"""
				SELECT T2.ZISPART_0,CONVERT(DECIMAL(18,0),SUM(T1.QTY_0)) QTY_0
				FROM SORDERQ T1
					LEFT JOIN ITMMASTER T2 ON T1.ITMREF_0 = T2.ITMREF_0
					LEFT JOIN SORDER T3 ON T1.SOHNUM_0 = T3.SOHNUM_0
					LEFT JOIN ATEXTRA T4 ON T3.CUR_0 = T4.IDENT1_0 AND T4.LANGUE_0 = N'CHI' AND T4.ZONE_0 = N'INTDES'
				WHERE T1.SALFCY_0 = N'{0}'
					AND T1.CREDAT_0 BETWEEN N'{1}' AND N'{2}'
					AND T4.TEXTE_0 = N'{3}'
				GROUP BY T4.TEXTE_0,T2.ZISPART_0
				ORDER BY T4.TEXTE_0
			""".format(facility,dateRange["start"],dateRange["end"],cur)
		return self.dbc.Query(SQL)

	def selectExchangeRate(self):
		dateRange = self.getDate.Today()
		SQL = u"""
				SELECT CURRENCYFROM_0 FROM EXCHANGERATE WHERE CREDAT_0 BETWEEN N'{0}' AND N'{1}'
			""".format(dateRange["start"],dateRange["end"])
		return self.dbc.Query(SQL)

	def getTodaySaleOrderDetails(self,facility):
		dateRange = self.getDate.Today()
		SQL = """SELECT T1.SOHNUM_0,
						CONVERT(INT,T1.SOPLIN_0),
						T1.ITMREF_0,
						CONVERT(DECIMAL(18,2),T1.QTY_0) 
				FROM SORDERQ T1
					LEFT JOIN SORDERP T2 ON T1.SOHNUM_0 = T2.SOHNUM_0 AND T1.SOPLIN_0 = T2.SOPLIN_0
				WHERE T1.CREDAT_0 BETWEEN N'{1}' AND N'{2}'
					AND T1.SALFCY_0 = N'{0}'
				ORDER BY T1.SOHNUM_0,T1.SOPLIN_0
					""".format(facility,dateRange["start"],dateRange["end"])
		return self.dbc.Query(SQL)

if __name__ == '__main__':
	dbo = DBOperation()
	print dbo.getTodaySaleOrderDetails('0201')