# -*- coding: utf-8 -*-
# filename: common.py


import sys
import os
import inspect





def scriptAbsPath(fname = inspect.currentframe()):
	path = os.path.split(inspect.getfile(fname))[0]
	absdir = os.path.realpath(os.path.abspath(path))
	return absdir

def scriptAbsPathParent(fname = inspect.currentframe()):
	return os.path.dirname(scriptAbsPath(fname))
	
def includeDir(subdir = None, fname = inspect.currentframe()):
	p = os.path.split(inspect.getfile(fname))[0]
	incdir = os.path.realpath(os.path.abspath(p))
	if incdir not in sys.path:
		sys.path.insert(0,incdir)
	if subdir:
		incdir = os.path.realpath(os.path.abspath(os.path.join(p, subdir)))
		if incdir not in sys.path:
			sys.path.insert(0, incdir)

absdir = scriptAbsPath()

while os.path.isdir(absdir):
	pkgini = os.path.join(absdir, "__init__.py")

	if not os.path.exists(pkgini):
		break

	if os.path.isdir(pkgini):
		break

	includeDir(absdir)

	absdir = os.path.dirname(absdir)
