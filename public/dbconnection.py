# -*- coding: utf-8 -*-
# filename: dbconnection.py

import pymssql
import json

class DBConnection(object):
	def __init__(self):
		with open("../dbconnection.json","r") as jsonFile:
			dbcConfig = json.loads(jsonFile.read())
		self.datehost = dbcConfig["datehost"]
		self.port = dbcConfig["port"]
		self.database = dbcConfig["database"]
		self.user = dbcConfig["user"]
		self.password = dbcConfig["password"]
		self.conn = pymssql.connect(host = self.datehost, database = self.database, user = self.user, password = self.password, port = self.port)
		self.cur = self.conn.cursor()
		
	def Query(self,SQL):
		self.cur.execute(SQL)
		result = self.cur.fetchall()
		self.conn.commit()
		return result

	# def QueryWithColName(self,SQL):
	# 	self.cur = self.conn.cursor(as_dict = True)
	# 	self.cur.execute(SQL)
	# 	result = self.cur.fetchall()
	# 	self.conn.commit()
	# 	self.cur = self.conn.cursor(as_dict = False)
	# 	return	result

	def execute(self,SQL):
		self.cur.execute(SQL)
		self.conn.commit()

	def disConnect(self):
		self.cur.close()
		self.conn.close()
