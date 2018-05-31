# -*- coding: utf-8 -*-
# filename: main.py

import common
import web
from Reply.handle import Handle
from PushData.querydata import TodaySaleDetails




if __name__ == '__main__':
	urls = (
			'/wx','Handle',
			"/todaySaleDetails","TodaySaleDetails"
		)
	app = web.application(urls, globals())
	app.run()