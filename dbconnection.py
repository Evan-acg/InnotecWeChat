# -*- coding: utf-8 -*-
# filename: dbconnection.py

import pymssql


class DBConnection(object):
	def __init__(self):
		self.datehost = '192.168.0.5'
		self.port = 1433
		# self.datehost = '121.46.26.50'
		# self.port = 4311
		self.database = 'innotec'
		self.user = 'INNO'
		self.password = 'tiger'
		self.conn = pymssql.connect(host = self.datehost, database = self.database, user = self.user, password = self.password, port = self.port)
		self.cur = self.conn.cursor()
		
	def Query(self,SQL):
		self.cur.execute(SQL)
		result = self.cur.fetchall()
		self.conn.commit()
		return result

	def execute(self,SQL):
		self.cur.execute(SQL)
		self.conn.commit()

	def disConnect(self):
		self.cur.close()
		self.conn.close()
