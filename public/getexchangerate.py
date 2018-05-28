# -*- coding: utf-8 -*-
# filename: getexchangerate.py


import urllib
from bs4 import BeautifulSoup
from dboperation import DBOperation


class GetExchangeRate(object):
	def __init__(self):
		self.addr = "https://finance.google.cn/finance/converter?a="
		self.dbo = DBOperation()

	def getEurOfCny(self):
		addr = self.addr+ "1&from=EUR&to=CNY"
		page = urllib.urlopen(addr).read()
		soup = BeautifulSoup(page,"html5lib")
		rate = soup.select(".bld")[0].string[:-4]
		self.dbo.insertExchangeRate('EUR','CNY',rate)

	def getUsdOfCny(self):
		addr = self.addr + "1&from=USD&to=CNY"
		page = urllib.urlopen(addr).read()
		soup = BeautifulSoup(page,"html5lib")
		rate = soup.select(".bld")[0].string[:-4]
		self.dbo.insertExchangeRate('USD','CNY',rate)

	def mainControl(self):
		self.getEurOfCny()
		self.getUsdOfCny()


if __name__ == '__main__':
	ger = GetExchangeRate()
	ger.getEurOfCny()
	ger.getUsdOfCny()
