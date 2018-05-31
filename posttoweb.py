# -*- coding: utf-8 -*-
# filename: posttoweb.py




import urllib2
from bs4 import BeautifulSoup



def pushTo():
	url = "http://121.46.30.178/wx"
	xml = """
		<xml>
			<ToUserName>< ![CDATA[toUser] ]></ToUserName>
			<FromUserName>< ![CDATA[FromUser] ]></FromUserName>
			<CreateTime>123456789</CreateTime>
			<MsgType>< ![CDATA[event] ]></MsgType>
			<Event>< ![CDATA[subscribe] ]></Event>
		</xml>
	"""
	# soup = BeautifulSoup(xml, "xml")
	# msgType = soup.find("MsgType").text
	# content = soup.find("Content").text
	# print content
	req = urllib2.Request(url = url, data = xml)
	page = urllib2.urlopen(req).read()
	print page
if __name__ == '__main__':
	pushTo()


