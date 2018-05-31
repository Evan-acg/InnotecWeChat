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
import datetime


class Handle:
	def __init__(self):
		self.pd = PushSaleData()
	def returnQueryMessage(self):
		self.pd.run()
		return "Success!"
	def returnSessionTime(self,recMsg):
		toUser = recMsg.FromUserName
		fromUser = recMsg.ToUserName
		limitDate = (datetime.datetime.now() + datetime.timedelta(days = 1)).strftime("%Y-%m-%d %H:%M:%S")
		content = u"本次会话到期时间为{0}！".format(limitDate)
		replyMsg = reply.TextMsg(toUser,fromUser,content)
		return	replyMsg.send()
	def returnSubscribeMessage(recMsg):
		toUser = recMsg.FromUserName
		fromUser = recMsg.ToUserName
		limitDate = (datetime.datetime.now() + datetime.timedelta(days = 1)).strftime("%Y-%m-%d %H:%M:%S")
		content = u"""
				欢迎来到亿诺股份公司消息推送系统！
					当前实现功能有：
						1.查询当日当前订单情况
							01.手动查询
								回复代码SOP01
							02.自动推送
								于每天晚上20：00自动推送，收到消息后请回复刷新会话时间，回复任意字符均可
			""".format(limitDate)
		replyMsg = reply.TextMsg(toUser,fromUser,content)
		gi = Info()
		gi.mainControl()
		dbo = DBOperation()
		nickName = dbo.getUserName(toUser)[0][0]
		NewSubscribe = "新用户的OPENID：{0}，用户名是：{1}！".format(toUser, nickName)
		pd.Push(NewSubscribe)
		return	replyMsg.send()
	def POST(self):
		try:
			webData = web.data()
			print "Handle Post webdata is ",webData
			recMsg = receive.parse_xml(webData)
			if isinstance(recMsg, receive.Msg) and recMsg.MsgType == "text" and recMsg.Content.upper() == "SOP01":
				return self.returnQueryMessage()
			elif isinstance(recMsg, receive.Msg) and recMsg.MsgType == "text":
				return self.returnSessionTime(recMsg)
			elif isinstance(recMsg, receive.Msg) and recMsg.MsgType == "event" and recMsg.Event == "subscribe":
				return self.returnSubscribeMessage(recMsg)
			else:
				return "Success!"
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