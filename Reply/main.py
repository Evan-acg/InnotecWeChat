# -*- coding: utf-8 -*-
# filename: main.py

import sys
sys.path.append("../")

import web
from Reply.handle import Handle




if __name__ == '__main__':
	urls = (
			'/wx','Handle',
		)
	app = web.application(urls, globals())

	app.run()