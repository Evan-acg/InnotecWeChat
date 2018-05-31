# -*- coding: utf-8 -*-
# filename: posttoweb.py




import urllib2
from bs4 import BeautifulSoup



def pushTo():
	url = "http://localhost:8080/wx"
	xml = """
		<xml>
			<ToUserName><![CDATA[公众号]]></ToUserName>
			 <FromUserName><![CDATA[ocwHT08BbAJvZ2Lj9o-fu7JJKWIw]]></FromUserName>
			 <CreateTime>1460537339</CreateTime>
			 <MsgType><![CDATA[text]]></MsgType>
			 <Content><![CDATA[1]]></Content>
			 <MsgId>6272960105994287618</MsgId>
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


