# -*- coding: utf-8 -*-
# filename: handle.py

import common
import hashlib
import web
from Reply import reply
from Reply import receive
from PushData.pushdata import PushSaleData
from Public.getinfo import Info
from Public.dboperation import DBOperation
from Auth.authorization import Authorization
import datetime


class Handle:
	def __init__(self):
		self.pd = PushSaleData()
		self.auth = Authorization()

	def seperate(self,content):
		content = content.upper()
		return content.split()

	def returnQueryMessage(self, recMsg):
		self.pd.run(recMsg.FromUserName)
		return ""
	def returnSessionTime(self,recMsg):
		toUser = recMsg.FromUserName
		fromUser = recMsg.ToUserName
		limitDate = (datetime.datetime.now() + datetime.timedelta(days = 1)).strftime("%Y-%m-%d %H:%M:%S")
		content = u"本次会话到期时间为{0}！".format(limitDate)
		self.pd.push(content, toUser)
		return ""
	def returnSubscribeMessage(self,recMsg):
		toUser = recMsg.FromUserName
		fromUser = recMsg.ToUserName
		content = "	欢迎来到亿诺股份公司消息推送系统！\n" + \
					"\t当前实现功能有：\n"+ \
					"\t\t1.查询当日当前订单情况\n"+ \
					"\t\t\t01.手动查询\n"+ \
					"\t\t\t\t回复代码SOP01\n"+ \
					"\t\t\t02.自动推送\n"+ \
					"\t\t\t\t\t于每天晚上20：00自动推送，收到消息后请回复刷新会话时间，回复任意字符均可"
		self.pd.push(content, toUser)
		gi = Info()
		gi.mainControl()
		dbo = DBOperation()
		nickName = dbo.getUserName(toUser)[0][0]
		newSubscribe = "新用户的OPENID：{0}，用户名是：{1}！".format(toUser, nickName)
		self.pd.push(NewSubscribe.encode("utf-8"),"ocwHT08BbAJvZ2Lj9o-fu7JJKWIw")
		return ""

	def checkAuthorise(self, *args):
                if len(args) ==0:
                        authList = self.auth.checkAuthorise()
                elif len(args) ==1:
                        authList = self.auth.checkAuthorise(args[0])
                msg = ""
		for row in authList:
			colCount = len(row)
			i = 0
			for col in row:
				if i < colCount:
					msg = msg + col
				else:
					msg = msg + col + "\n"
				i += 1
		self.pd.push(msg)
		return ""

	def POST(self):
		try:
			webData = web.data()
			recMsg = receive.parse_xml(webData)
			codeList = self.seperate(recMsg.Content)
			order = codeList[0]
			if isinstance(recMsg, receive.Msg) and recMsg.MsgType == "text" :
				if order == "SOP01":
					return self.returnQueryMessage(recMsg)
				elif order == "AUTH":
					return self.checkAuthorise()
				else:
					return self.returnSessionTime(recMsg)
			elif isinstance(recMsg, receive.Msg) and recMsg.MsgType == "event" and recMsg.Event == "subscribe":
				return self.returnSubscribeMessage(recMsg)
			else:
				return ""
		except Exception, Argument:
			return Argument
	def GET(self):
		try:
			data = web.input()
			if len(data) == 0:
				return "hello!"
			signature = data.signature
			timestamp = data.timestamp
			nonce = data.nonce
			echostr = data.echostr
			token = "innotec"
			list = [token, timestamp, nonce]
			list.sort()
			sha1 = hashlib.sha1()
			map(sha1.update, list)
			hashcode = sha1.hexdigest()
			print "handle/GET func:hashcode, signature:",hashcode,signature
			if hashcode == signature:
				return echostr
			else:
				return ""
		except Exception, Argument:
			return Argument
